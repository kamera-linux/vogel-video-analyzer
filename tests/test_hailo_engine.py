"""
Tests for the Hailo post-processing (no Hailo hardware needed).
"""

from types import SimpleNamespace

import numpy as np
import pytest

from vogel_video_analyzer.hailo_engine import HailoDetector, letterbox


def _detector(num_classes=80, input_size=(640, 640), output_names=("out",)):
    det = HailoDetector.__new__(HailoDetector)
    det.num_classes = num_classes
    det._input_h, det._input_w = input_size
    det._output_names = list(output_names)
    det._pipeline = None
    det._stack = None
    det._device = None
    return det


# ── letterbox ────────────────────────────────────────────────────────────────

def test_letterbox_preserves_aspect_ratio_and_maps_back():
    frame = np.zeros((480, 1280, 3), dtype=np.uint8)
    padded, scale, pad_x, pad_y = letterbox(frame, (640, 640))
    assert padded.shape == (640, 640, 3)
    assert scale == pytest.approx(0.5)
    assert pad_x == 0 and pad_y == 200
    # model-input point (320, 320) is the centre of the original frame
    assert ((320 - pad_x) / scale, (320 - pad_y) / scale) == (640.0, 240.0)


# ── output format detection ─────────────────────────────────────────────────

def test_detect_nms_by_format_order():
    info = SimpleNamespace(shape=(80, 5, 100), format=SimpleNamespace(order="FormatOrder.HAILO_NMS_BY_CLASS"))
    assert HailoDetector._detect_nms_output([info]) is True


def test_detect_legacy_nms_and_raw():
    legacy = SimpleNamespace(shape=(100, 6), format=SimpleNamespace(order="FormatOrder.NHWC"))
    raw = SimpleNamespace(shape=(80, 80, 144), format=SimpleNamespace(order="FormatOrder.NHWC"))
    assert HailoDetector._detect_nms_output([legacy]) is True
    assert HailoDetector._detect_nms_output([raw, raw, raw]) is False


# ── NMS parsing ─────────────────────────────────────────────────────────────

def test_parse_hailo_nms_by_class_format():
    det = _detector(num_classes=80)
    per_class = [np.zeros((0, 5), dtype=np.float32) for _ in range(80)]
    # [y_min, x_min, y_max, x_max, score] normalised
    per_class[14] = np.array([[0.25, 0.5, 0.75, 1.0, 0.8]], dtype=np.float32)
    result = det._parse_nms_output({"out": [per_class]})
    assert len(result) == 1
    x1, y1, x2, y2, conf, cls_id = result[0]
    assert (x1, y1, x2, y2) == pytest.approx((320, 160, 640, 480))
    assert conf == pytest.approx(0.8) and cls_id == 14


def test_parse_nms_respects_num_classes():
    det = _detector(num_classes=1)
    per_class = [np.array([[0, 0, 0.5, 0.5, 0.9]], dtype=np.float32),
                 np.array([[0, 0, 0.5, 0.5, 0.9]], dtype=np.float32)]
    result = det._parse_nms_output({"out": [per_class]})
    assert [r[5] for r in result] == [0]


def test_parse_legacy_nms_tensor():
    det = _detector(num_classes=80)
    raw = np.array([[[0.0, 0.0, 0.5, 0.5, 0.7, 14], [0, 0, 1, 1, 0.0, 3], [0, 0, 1, 1, 0.9, 99]]],
                   dtype=np.float32)
    result = det._parse_nms_output({"out": raw})
    assert len(result) == 1
    assert result[0][5] == 14


# ── raw output decoding ─────────────────────────────────────────────────────

def test_parse_raw_dfl_output_decodes_box():
    """YOLOv8 DFL head: 64 box channels + num_classes, one stride."""
    nc = 2
    det = _detector(num_classes=nc, input_size=(64, 64), output_names=("p3",))
    grid = 8  # stride 8
    pred = np.full((1, grid, grid, 64 + nc), -10.0, dtype=np.float32)
    # One confident cell at (gx=3, gy=2), class 1, distances l,t,r,b = 1,1,2,2 grid units
    cell = pred[0, 2, 3]
    cell[:64] = -10.0
    for side, dist in enumerate([1, 1, 2, 2]):
        cell[side * 16 + dist] = 10.0
    cell[64 + 1] = 5.0  # logit -> sigmoid ~0.99

    result = det._parse_multi_output({"p3": pred})
    assert len(result) == 1
    x1, y1, x2, y2, conf, cls_id = result[0]
    # centre = (3.5, 2.5) * 8 = (28, 20)
    assert (x1, y1, x2, y2) == pytest.approx((20, 12, 44, 36), abs=0.1)
    assert cls_id == 1 and conf > 0.9


def test_parse_raw_split_box_and_class_tensors():
    """Hailo often splits each stride into a box tensor and a class tensor."""
    nc = 1
    det = _detector(num_classes=nc, input_size=(32, 32), output_names=("cls", "box"))
    box = np.full((1, 4, 4, 64), -10.0, dtype=np.float32)
    cls = np.full((1, 4, 4, nc), 0.0, dtype=np.float32)  # already sigmoid'ed probabilities
    for side in range(4):
        box[0, 1, 1, side * 16 + 1] = 10.0
    cls[0, 1, 1, 0] = 0.95
    result = det._parse_multi_output({"cls": cls, "box": box})
    assert len(result) == 1
    assert result[0][4] == pytest.approx(0.95)
    # stride 8, centre (1.5, 1.5) * 8 = 12, distance 1 * 8
    assert result[0][:4] == pytest.approx((4, 4, 20, 20), abs=0.1)


def test_closed_detector_raises():
    det = _detector()
    with pytest.raises(RuntimeError):
        det(np.zeros((10, 10, 3), dtype=np.uint8))
    det.close()  # idempotent, no device
