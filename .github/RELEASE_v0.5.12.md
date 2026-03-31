# Release v0.5.12 - Raspberry Pi AI HAT+ / Hailo-8 NPU Support

**Release Date:** 2026-03-31

---

## 🎯 Overview

v0.5.12 is a **feature release** that adds **hardware-accelerated inference** on the **Raspberry Pi 5 with AI HAT+** (Hailo-8, 26 TOPS). A new `--engine hailo` backend enables drop-in NPU inference without changing the existing analysis workflow. Additionally, an ONNX export CLI allows converting `.pt` model files for Hailo Dataflow Compiler compilation. All new strings are fully translated in EN, DE, and JA.

---

## ✨ What's New

### ⚡ Raspberry Pi AI HAT+ / Hailo-8 NPU Backend
- **New `--engine hailo` flag**: Drop-in NPU inference backend for `vogel-analyze`
- **`HailoDetector` class** (`hailo_engine.py`): Works as a transparent replacement for ultralytics YOLO objects; no code changes required in analysis pipeline
- **NMS-integrated output support**: Detects HEF output format automatically (single output with shape `[-1, 6]` = NMS mode)
- **Raw feature-map output support**: Applies `_parse_multi_output()` for YOLOv5/v8/v26-style raw outputs
- **`--hef-model PATH`**: Specify a compiled `.hef` file for inference
- **`--hailo-num-classes N`**: Number of classes for custom models (default: 80 COCO)
- **`--engine auto`** (default): Falls back to ultralytics when `hailo_platform` is not installed

### 📦 ONNX Export CLI
- **`--export-onnx MODEL_PATH`**: Converts `.pt` → `.onnx` with correct settings for Hailo DFC
- **`--export-onnx-output PATH`**: Custom output path (default: same folder as input)
- Prints full step-by-step next-steps guide after export (copy to x86, compile, copy back, run)
- Tested with `yolov8n.pt` and `yolov26n.pt`

### 🌐 i18n: Full Hailo Translation Coverage
All Hailo strings are now translated in **EN, DE, JA**:
`loading_hailo_model`, `hailo_engine_info`, `hailo_nms_mode`, `hailo_raw_mode`,
`hailo_not_installed`, `hailo_hef_required`, `hailo_hef_not_found`,
`hailo_export_start`, `hailo_export_input_size`, `hailo_export_opset`,
`hailo_export_hint`, `hailo_export_complete`, `hailo_export_next_steps`,
`hailo_export_step1`–`step4`, `hailo_export_dfc_link`, `hailo_export_zoo_link`,
`hailo_onnx_not_installed`, `hailo_model_not_found`

---

## 📋 Testing

✅ **Local Testing Complete:**
- Import test: `from src.vogel_video_analyzer.hailo_engine import export_to_onnx` → OK
- `export_to_onnx` parameter signature verified
- `hailo_platform` absence correctly raises `RuntimeError` with i18n message
- `--engine auto` falls back to ultralytics on non-Hailo systems without error

```bash
# Test ONNX export (no Hailo hardware required):
vogel-analyze --export-onnx yolov8n.pt

# Test Hailo engine (Raspberry Pi 5 + AI HAT+):
vogel-analyze --engine hailo --hef-model yolov8n.hef bird_video.mp4

# Test custom class count:
vogel-analyze --engine hailo --hef-model custom.hef --hailo-num-classes 182 video.mp4

# Test auto fallback on non-Hailo system:
vogel-analyze --engine auto video.mp4
```

---

## 📝 Changes Summary

### New Files
- **`src/vogel_video_analyzer/hailo_engine.py`**
  - `HAILO_AVAILABLE`: bool, True if `hailo_platform` is importable
  - `export_to_onnx(model_path, output_path, input_size, opset)`: `.pt` → `.onnx` export
  - `HailoDetector(hef_path, num_classes)`: ultralytics-compatible inference wrapper
    - `_detect_nms_output()`: heuristic to detect NMS vs raw output mode
    - `_parse_nms_output()`: processes NMS-integrated HEF output
    - `_parse_multi_output()`: processes raw feature-map HEF output
  - `_MockBox`, `_TensorLike`, `_MockResult`: mock objects mimicking ultralytics result shapes

### Modified Files
- **`src/vogel_video_analyzer/analyzer.py`**
  - `VideoAnalyzer.__init__`: new params `engine="auto"`, `hef_model=None`, `hailo_num_classes=80`
  - `_init_hailo_engine(hef_model, num_classes)`: Hailo engine initialization with i18n error messages
  - `_find_hef_model(hef_name)`: HEF file search in CWD and script directory

- **`src/vogel_video_analyzer/cli.py`**
  - `--engine {auto,hailo}`: engine selection flag
  - `--hef-model PATH`: compiled HEF file path
  - `--hailo-num-classes N`: class count for custom models
  - `--export-onnx MODEL_PATH`: triggers ONNX export and exits
  - `--export-onnx-output PATH`: custom ONNX output path

- **`src/vogel_video_analyzer/i18n.py`**
  - 19 new keys added to all 3 language sections (EN, DE, JA)

- **`src/vogel_video_analyzer/__init__.py`**
  - Version: `0.5.11` → `0.5.12`

- **`pyproject.toml`**
  - Added `[hailo]` optional dependency group with apt install instructions

- **`CHANGELOG.md`**
  - Added v0.5.12 release notes

- **`README.md`**, **`README.de.md`**, **`README.ja.md`**
  - Added Hailo-8 NPU feature bullet (all 3 languages)
  - Added Hailo Quick Start CLI examples (all 3 languages)

---

## 🔄 Compatibility

- ✅ Backward compatible with v0.5.11
- ✅ Hailo dependencies installed separately via `sudo apt install hailo-all`
- ✅ `--engine auto` (default) silently skips Hailo when not installed
- ✅ All existing workflows unaffected
- ✅ No new PyPI dependencies added

---

## 🚀 Installation

### Update from v0.5.11

```bash
pip install --upgrade vogel-video-analyzer
```

### Enable Hailo NPU Support (Raspberry Pi only)

```bash
# Install HailoRT driver and Python package
sudo apt install hailo-all   # Debian Trixie / Bookworm

# Verify
python3 -c "import hailo_platform; print('Hailo OK')"

# Export .pt → .onnx (on Raspberry Pi)
vogel-analyze --export-onnx yolov8n.pt

# Compile .onnx → .hef (on x86 PC with Hailo Dataflow Compiler)
hailo compiler --hw-arch hailo8 yolov8n.onnx

# Run inference on Raspberry Pi with Hailo NPU
vogel-analyze --engine hailo --hef-model yolov8n.hef video.mp4
```

### Verify Installation

```bash
vogel-analyze --version  # Should show: 0.5.12
```

---

## 📊 Impact

| Feature | Status |
|---------|--------|
| Hailo-8 NPU inference | ✅ New |
| ONNX export | ✅ New |
| i18n coverage | ✅ Complete (EN/DE/JA) |
| Backward compatibility | ✅ Full |
| PyPI dependencies | ✅ None added |
| Performance (CPU path) | ✅ No impact |

---

## 🔧 Hailo Hardware Requirements

| Component | Version |
|-----------|---------|
| Raspberry Pi | 5 (PCIe required) |
| AI HAT+ | Hailo-8 (26 TOPS) |
| HailoRT | ≥ 4.17.0 (tested: 4.23.0) |
| TAPPAS Core | 5.1.0 |
| hailo-all metapackage | 5.1.1 |
| OS | Debian Trixie / Bookworm |

---

## 🐛 Known Issues

- `hailo_platform` is not available on PyPI — must be installed via `sudo apt install hailo-all` on Raspberry Pi
- HEF compilation requires Hailo Dataflow Compiler (x86 only, free registration at hailo.ai)
- Pylance reports `Import "hailo_platform" could not be resolved` — expected, import is wrapped in `try/except`

---

## 🔗 Related Resources

- [Hailo Dataflow Compiler](https://hailo.ai/developer-zone/)
- [Hailo Model Zoo (pre-compiled HEFs)](https://github.com/hailo-ai/hailo_model_zoo)
- [HailoRT documentation](https://github.com/hailo-ai/hailort)
- [vogel-kamera-linux parent project](https://github.com/kamera-linux/vogel-kamera-linux)

---

## ✅ Release Checklist

- [x] `hailo_engine.py` created and tested
- [x] `analyzer.py` extended with Hailo engine abstraction
- [x] `cli.py` extended with Hailo and ONNX export flags
- [x] `i18n.py` updated (EN, DE, JA) for all Hailo strings
- [x] Version bumped to 0.5.12
- [x] `CHANGELOG.md` updated
- [x] `README.md` updated (EN)
- [x] `README.de.md` updated (DE)
- [x] `README.ja.md` updated (JA)
- [x] `RELEASE_v0.5.12.md` created
- [ ] Git tag created: `git tag -a v0.5.12 -m "Release v0.5.12: Raspberry Pi AI HAT+ / Hailo-8 NPU Support"`
- [ ] Push to GitHub: `git push origin v0.5.12`
- [ ] GitHub Release published
- [ ] PyPI auto-published (via GitHub Actions)

---
