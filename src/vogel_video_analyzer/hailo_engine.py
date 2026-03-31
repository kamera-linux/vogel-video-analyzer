"""
Hailo NPU inference engine for Raspberry Pi AI HAT+

Supports Hailo-8 (26 TOPS) and Hailo-8L (13 TOPS) via the HailoRT Python API.
Returns ultralytics-compatible result objects so the existing VideoAnalyzer
pipeline works without changes.

Hardware requirements:
  - Raspberry Pi 5 with AI HAT+ (Hailo-8 or Hailo-8L)
  - HailoRT >= 4.17.0 installed (hailo-all metapackage on Raspberry Pi OS)

Software install (on the Raspberry Pi):
  sudo apt install hailo-all        # installs hailo_platform Python bindings
  # verify:
  python3 -c "import hailo_platform; print('Hailo OK')"

──────────────────────────────────────────────────────────────────────────────
Using yolov26n.pt (or any custom .pt) on the Hailo AI HAT+
──────────────────────────────────────────────────────────────────────────────
The Hailo chip executes compiled HEF binaries, not .pt files directly.
The workflow involves two steps, of which step 1 can be done on the Pi:

Step 1 – Export .pt → .onnx  (runs on any machine with ultralytics)

  # CLI:
  vogel-analyze --export-onnx yolov26n.pt

  # Python:
  from vogel_video_analyzer.hailo_engine import export_to_onnx
  export_to_onnx("yolov26n.pt", output_path="yolov26n.onnx")

Step 2 – Compile .onnx → .hef  (requires Hailo Dataflow Compiler on x86 PC)

  # Install DFC (x86 only, not on the Pi itself):
  pip install hailo-dataflow-compiler   # requires Hailo developer license

  # Compile:
  hailo compiler --hw-arch hailo8 yolov26n.onnx
  # → produces yolov26n.hef

  # Alternative: Hailo Model Zoo CLI (recommended for standard YOLO variants):
  # https://github.com/hailo-ai/hailo_model_zoo

Step 3 – Copy yolov26n.hef to the Raspberry Pi and run:

  vogel-analyze --engine hailo --hef-model yolov26n.hef video.mp4

Note: If you used a custom YOLOv26n trained only on bird data (e.g. 1 class),
add --hailo-num-classes 1 and adjust --threshold and target class accordingly.

For pre-compiled standard HEF files (YOLOv8n / YOLOv5 / YOLOv10):
  https://github.com/hailo-ai/hailo_model_zoo
──────────────────────────────────────────────────────────────────────────────

Usage:
  from vogel_video_analyzer.hailo_engine import HailoDetector, HAILO_AVAILABLE
"""

import numpy as np
import cv2
from pathlib import Path
from .i18n import t

# ──────────────────────────────────────────────────────────────────────────────
# Optional HailoRT import
# ──────────────────────────────────────────────────────────────────────────────


def export_to_onnx(model_path: str, output_path: str = None,
                   input_size: int = 640, opset: int = 12) -> str:
    """
    Export a YOLO .pt model to ONNX format as the first step towards Hailo HEF.

    This step runs on any machine (including the Raspberry Pi).
    The resulting ONNX file then needs to be compiled to HEF with the
    Hailo Dataflow Compiler on an x86 PC.

    Args:
        model_path:  Path to the YOLO .pt model file (e.g. "yolov26n.pt").
        output_path: Output path for the .onnx file.  Defaults to the same
                     directory as model_path with the .onnx extension.
        input_size:  ONNX input image size (default 640).  Hailo requires a
                     fixed square input; 640 matches most YOLO HEF variants.
        opset:       ONNX opset version (default 12, Hailo DFC compatible).

    Returns:
        Absolute path to the exported ONNX file.

    Raises:
        ImportError:     ultralytics is not installed.
        FileNotFoundError: .pt model file does not exist.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        raise ImportError(t('hailo_onnx_not_installed'))

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(t('hailo_model_not_found').format(path=model_path))

    if output_path is None:
        output_path = model_path.with_suffix(".onnx")
    output_path = Path(output_path)

    print(f"\U0001f4e6 {t('hailo_export_start').format(model=model_path.name, output=output_path)}")
    print(f"   {t('hailo_export_input_size').format(size=input_size)}")
    print(f"   {t('hailo_export_opset').format(opset=opset)}")
    print(f"   {t('hailo_export_hint')}")

    model = YOLO(str(model_path), task="detect")
    model.export(
        format="onnx",
        imgsz=input_size,
        opset=opset,
        simplify=True,   # onnxsim → removes unsupported ops for Hailo DFC
        dynamic=False,   # Hailo requires static shapes
    )

    # ultralytics writes the ONNX file next to the .pt file
    default_onnx = model_path.with_suffix(".onnx")
    if default_onnx.exists() and default_onnx != output_path:
        import shutil
        shutil.move(str(default_onnx), str(output_path))

    print(f"\n\u2705 {t('hailo_export_complete').format(path=output_path.resolve())}")
    print(f"\n\U0001f4cb {t('hailo_export_next_steps')}")
    print(f"   {t('hailo_export_step1').format(file=output_path.name)}")
    print(f"   {t('hailo_export_step2').format(file=output_path.name)}")
    print(f"   {t('hailo_export_step3')}")
    print(f"   {t('hailo_export_step4').format(stem=output_path.stem)}")
    print(f"\n   {t('hailo_export_dfc_link')}")
    print(f"   {t('hailo_export_zoo_link')}")

    return str(output_path.resolve())


# ──────────────────────────────────────────────────────────────────────────────
# Optional HailoRT import
# ──────────────────────────────────────────────────────────────────────────────
try:
    from hailo_platform import (
        HEF,
        VDevice,
        HailoStreamInterface,
        InferVStreams,
        ConfigureParams,
        InputVStreamParams,
        OutputVStreamParams,
        FormatType,
    )
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────────────
# Ultralytics-compatible mock objects
# ──────────────────────────────────────────────────────────────────────────────

class _TensorLike:
    """
    Numpy-backed stub with .cpu().numpy() interface to match ultralytics tensors.
    Supports indexing so box.cls[0] and box.xyxy[0] work as expected.
    """

    def __init__(self, data):
        self._data = np.asarray(data, dtype=np.float32)

    def __getitem__(self, idx):
        return _TensorLike(self._data[idx])

    def cpu(self):
        return self

    def numpy(self):
        return self._data

    def __float__(self):
        return float(self._data.flat[0])

    def __int__(self):
        return int(self._data.flat[0])

    def __repr__(self):
        return f"_TensorLike({self._data})"


class _MockBox:
    """
    Single detection box that mimics the ultralytics Boxes element API:
      box.cls[0]            -> class id
      box.conf[0]           -> confidence
      box.xyxy[0].cpu().numpy() -> [x1, y1, x2, y2] in pixel coordinates
    """

    def __init__(self, x1: float, y1: float, x2: float, y2: float,
                 conf: float, cls_id: int):
        self.cls = _TensorLike([float(cls_id)])
        self.conf = _TensorLike([float(conf)])
        self.xyxy = _TensorLike([[float(x1), float(y1), float(x2), float(y2)]])


class _MockBoxes:
    """Collection of _MockBox objects mimicking ultralytics Boxes."""

    def __init__(self, boxes: list):
        self._boxes = boxes

    def __iter__(self):
        return iter(self._boxes)

    def __len__(self):
        return len(self._boxes)


class _MockResult:
    """Detection result mimicking ultralytics Results with a .boxes attribute."""

    def __init__(self, boxes: list):
        self.boxes = _MockBoxes(boxes)


# ──────────────────────────────────────────────────────────────────────────────
# Main Hailo detector class
# ──────────────────────────────────────────────────────────────────────────────

class HailoDetector:
    """
    YOLO object detector running on the Hailo-8 NPU (Raspberry Pi AI HAT+).

    The detector emulates the ultralytics YOLO callable interface:
        results = detector(frame, verbose=False)
    so it can be used as a drop-in replacement for ``self.model`` in VideoAnalyzer.

    Two output modes are supported automatically:
      * NMS-integrated HEF  – single output tensor (N, 6): x1,y1,x2,y2,conf,cls
        (coordinates normalised 0-1)
      * Raw feature-map HEF – three output tensors at strides 8/16/32 with
        anchor-free YOLOv8 encoding; soft NMS applied in Python.

    Most Hailo Model Zoo HEF files use NMS-integrated mode.
    """

    # Standard COCO resolution used by most Hailo-compiled YOLO models
    DEFAULT_INPUT_SIZE = (640, 640)  # (height, width)

    def __init__(self, hef_path: str, input_size=None, num_classes: int = 80):
        """
        Initialise the Hailo inference engine.

        Args:
            hef_path:    Path to the compiled HEF model file.
            input_size:  Override model input (height, width).  Auto-detected
                         from the HEF when None.
            num_classes: Number of output classes.  80 for standard COCO;
                         adjust when using a custom-trained model.

        Raises:
            RuntimeError:    hailo_platform is not installed.
            FileNotFoundError: HEF file does not exist.
        """
        if not HAILO_AVAILABLE:
            raise RuntimeError(t('hailo_not_installed'))

        self.hef_path = Path(hef_path)
        if not self.hef_path.exists():
            raise FileNotFoundError(t('hailo_hef_not_found').format(name=hef_path))

        self.num_classes = num_classes

        # ── Load the compiled model ──────────────────────────────────────────
        self._hef = HEF(str(self.hef_path))
        self._device = VDevice()

        configure_params = ConfigureParams.create_from_hef(
            hef=self._hef,
            interface=HailoStreamInterface.PCIe,
        )
        network_groups = self._device.configure(self._hef, configure_params)
        self._network_group = network_groups[0]
        self._network_group_params = self._network_group.create_params()

        # ── Stream params (uint8 input, float32 output) ──────────────────────
        self._input_params = InputVStreamParams.make(
            self._network_group, format_type=FormatType.UINT8
        )
        self._output_params = OutputVStreamParams.make(
            self._network_group, format_type=FormatType.FLOAT32
        )

        # ── Resolve input shape ──────────────────────────────────────────────
        input_info = self._hef.get_input_vstream_infos()[0]
        self._input_name = input_info.name
        shape = input_info.shape  # (H, W, C) from HailoRT

        if input_size is not None:
            self._input_h, self._input_w = input_size
        else:
            self._input_h = int(shape[0]) if len(shape) >= 1 else self.DEFAULT_INPUT_SIZE[0]
            self._input_w = int(shape[1]) if len(shape) >= 2 else self.DEFAULT_INPUT_SIZE[1]

        # ── Detect output mode ───────────────────────────────────────────────
        output_infos = self._hef.get_output_vstream_infos()
        self._output_names = [o.name for o in output_infos]
        self._has_nms_output = self._detect_nms_output(output_infos)

        mode = t('hailo_nms_mode') if self._has_nms_output else t('hailo_raw_mode')
        print(
            f"   \u26a1 {t('hailo_engine_info').format(model=self.hef_path.name, w=self._input_w, h=self._input_h, mode=mode)}"
        )

    # ── Public interface ─────────────────────────────────────────────────────

    def __call__(self, frame: np.ndarray, verbose: bool = False, **kwargs):
        """
        Run inference on a single BGR frame.

        Args:
            frame:   numpy array (H, W, 3) in BGR format (OpenCV default).
            verbose: ignored – present only for API compatibility.

        Returns:
            List[_MockResult] – one element, mimicking ultralytics output.
        """
        frame_h, frame_w = frame.shape[:2]

        # Preprocess: resize + keep as uint8 (HailoRT expects uint8 NHWC)
        resized = cv2.resize(frame, (self._input_w, self._input_h))
        input_arr = resized[np.newaxis]  # (1, H, W, 3)

        input_data = {self._input_name: input_arr}

        # Run on Hailo NPU
        with self._network_group.activate(self._network_group_params):
            with InferVStreams(
                self._network_group,
                self._input_params,
                self._output_params,
            ) as pipeline:
                output_data = pipeline.infer(input_data)

        # Post-process
        if self._has_nms_output:
            detections = self._parse_nms_output(output_data, frame_w, frame_h)
        else:
            detections = self._parse_multi_output(output_data, frame_w, frame_h)

        return [_MockResult(detections)]

    # ── Private helpers ──────────────────────────────────────────────────────

    def _detect_nms_output(self, output_infos) -> bool:
        """
        Heuristic: a single output whose last dimension is 6 indicates
        an NMS-integrated model with format [x1, y1, x2, y2, conf, cls].
        """
        if len(output_infos) == 1:
            shape = output_infos[0].shape
            if len(shape) >= 2 and shape[-1] == 6:
                return True
        return False

    def _parse_nms_output(self, output_data: dict,
                          orig_w: int, orig_h: int) -> list:
        """
        Parse NMS-integrated output (shape: (1, N, 6) or (N, 6)).
        Coordinates are normalised to [0, 1].
        """
        raw = output_data[self._output_names[0]]
        if raw.ndim == 3:
            raw = raw[0]  # remove batch dim → (N, 6)

        detections = []
        for det in raw:
            x1_n, y1_n, x2_n, y2_n, conf, cls_id = det
            if conf <= 0.0:
                continue
            x1 = int(np.clip(x1_n * orig_w, 0, orig_w))
            y1 = int(np.clip(y1_n * orig_h, 0, orig_h))
            x2 = int(np.clip(x2_n * orig_w, 0, orig_w))
            y2 = int(np.clip(y2_n * orig_h, 0, orig_h))
            detections.append(_MockBox(x1, y1, x2, y2, float(conf), int(cls_id)))

        return detections

    def _parse_multi_output(self, output_data: dict,
                             orig_w: int, orig_h: int) -> list:
        """
        Decode raw YOLOv8 anchor-free multi-scale outputs (3 tensors at
        strides 8, 16, 32) and apply NMS.

        Each tensor has shape (1, H, W, 4 + num_classes) where the first
        4 channels are the box regression (cx, cy, w, h in grid units).

        Note: For best Hailo performance prefer an NMS-integrated HEF.
        """
        STRIDES = [8, 16, 32]
        IOU_THRESH = 0.45
        CONF_THRESH = 0.01

        all_boxes: list = []
        all_scores: list = []
        all_classes: list = []

        for name, stride in zip(sorted(self._output_names), STRIDES):
            if name not in output_data:
                continue
            pred = output_data[name]
            if pred.ndim == 4:
                pred = pred[0]  # remove batch dim → (H, W, C)

            grid_h, grid_w = pred.shape[:2]

            box_pred = pred[..., :4]       # cx, cy, w, h – grid-unit
            cls_pred = pred[..., 4:]       # raw class logits

            cls_scores = 1.0 / (1.0 + np.exp(-cls_pred))  # sigmoid
            cls_ids = np.argmax(cls_scores, axis=-1)
            cls_confs = np.max(cls_scores, axis=-1)

            xs = np.arange(grid_w, dtype=np.float32)
            ys = np.arange(grid_h, dtype=np.float32)
            grid_x, grid_y = np.meshgrid(xs, ys)

            # Anchor-free decode
            cx = (grid_x + box_pred[..., 0]) * stride
            cy = (grid_y + box_pred[..., 1]) * stride
            w = np.exp(np.clip(box_pred[..., 2], -10, 10)) * stride
            h = np.exp(np.clip(box_pred[..., 3], -10, 10)) * stride

            # Normalise to [0, 1]
            x1 = (cx - w / 2) / self._input_w
            y1 = (cy - h / 2) / self._input_h
            x2 = (cx + w / 2) / self._input_w
            y2 = (cy + h / 2) / self._input_h

            mask = cls_confs > CONF_THRESH
            if not np.any(mask):
                continue

            all_boxes.append(np.stack([x1[mask], y1[mask], x2[mask], y2[mask]], axis=-1))
            all_scores.append(cls_confs[mask])
            all_classes.append(cls_ids[mask])

        if not all_boxes:
            return []

        boxes_norm = np.concatenate(all_boxes)
        scores = np.concatenate(all_scores)
        classes = np.concatenate(all_classes)

        # Scale to original frame pixels for NMS
        boxes_px = boxes_norm * np.array([orig_w, orig_h, orig_w, orig_h],
                                          dtype=np.float32)
        # cv2.dnn.NMSBoxes expects [x, y, w, h]
        boxes_xywh = [
            [float(b[0]), float(b[1]),
             float(b[2] - b[0]), float(b[3] - b[1])]
            for b in boxes_px
        ]

        indices = cv2.dnn.NMSBoxes(
            boxes_xywh, scores.tolist(), CONF_THRESH, IOU_THRESH
        )
        if len(indices) == 0:
            return []

        indices = [int(i) for i in np.array(indices).flatten()]
        detections = []
        for idx in indices:
            x1 = int(np.clip(boxes_px[idx, 0], 0, orig_w))
            y1 = int(np.clip(boxes_px[idx, 1], 0, orig_h))
            x2 = int(np.clip(boxes_px[idx, 2], 0, orig_w))
            y2 = int(np.clip(boxes_px[idx, 3], 0, orig_h))
            detections.append(
                _MockBox(x1, y1, x2, y2, float(scores[idx]), int(classes[idx]))
            )

        return detections

    def __del__(self):
        """Release Hailo device resources."""
        try:
            if hasattr(self, "_device"):
                del self._device
        except Exception:
            pass
