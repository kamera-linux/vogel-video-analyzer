# Release v0.5.6: YOLOv26 Upgrade

## 🚀 Major Upgrade: YOLOv8 → YOLOv26

This release upgrades the core object detection framework from **YOLOv8 to YOLOv26**, delivering significant performance improvements and better bird detection capabilities.

### ⚡ Performance Improvements

- **43% Faster CPU Inference** - Critical for real-time video processing on edge devices
- **Better Small Object Detection** - Improved accuracy for detecting birds at various distances
- **Smaller Model Size** - `yolo26n.pt` is only **5.3 MB** (vs larger YOLOv8 models)
- **NMS-Free Architecture** - Simplified inference pipeline without separate post-processing
- **More Stable Training** - New MuSGD optimizer (inspired by Moonshot AI's Kimi K2)

### 📝 What's Changed

#### Default Model
- Changed default detection model from `yolov8n.pt` → **`yolo26n.pt`**
- Users can still use custom YOLO models via `--model` flag

#### Dependencies
- Updated `ultralytics` → **v8.4.14+** (YOLOv26 support)

#### Documentation
All documentation has been updated to reflect YOLOv26:
- ✅ [README.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/README.md) (English)
- ✅ [README.de.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/README.de.md) (Deutsch)
- ✅ [README.ja.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/README.ja.md) (日本語)
- ✅ All code examples use `yolo26n.pt`

### 🔄 Backward Compatibility

**No breaking changes!** 
- Existing code continues to work without modifications
- The API is fully compatible with previous versions
- Users can still specify custom YOLO models

### Installation & Upgrade

```bash
# Upgrade from PyPI
pip install --upgrade vogel-video-analyzer

# Or from source
git clone https://github.com/kamera-linux/vogel-video-analyzer.git
cd vogel-video-analyzer
pip install -e .
```

### Quick Test

```python
from vogel_video_analyzer import VideoAnalyzer

# Uses YOLOv26n by default
analyzer = VideoAnalyzer()
results = analyzer.analyze_video("video.mp4")
```

### Technical Details

#### Why YOLOv26?

YOLOv26 was released on **January 14, 2026** and introduces:

1. **End-to-End NMS-Free Design**
   - Eliminates separate NMS post-processing stage
   - Faster inference in production
   - Simplified integration with edge devices

2. **Advanced Optimization**
   - MuSGD: Hybrid optimizer combining SGD + Muon algorithms
   - Inspired by LLM training advances (Moonshot AI's Kimi K2)
   - Better convergence on small objects (especially birds!)

3. **Edge Computing Focus**
   - Designed specifically for resource-constrained environments
   - 43% faster on CPU-only systems
   - Supports multiple export formats (ONNX, TFLite, CoreML, OpenVINO)

4. **Task-Specific Optimizations**
   - Improved segmentation with semantic loss + multi-scale protos
   - Better pose estimation with RLE (Residual Log-Likelihood)
   - Enhanced OBB detection with angle loss

### Performance Metrics

| Model | COCO AP | Speed (ms) | Params | FLOPs |
|-------|---------|-----------|--------|-------|
| YOLOv26n | 40.9 | 1.7 | 2.4M | 5.4B |
| YOLOv26s | 48.6 | 2.5 | 9.5M | 20.7B |
| YOLOv26m | 53.1 | 4.7 | 20.4M | 68.2B |

### Contributors

- 🙏 Thanks to the Ultralytics team for YOLOv26 development
- 🐦 Vogel-Kamera-Linux team for integration & testing

### Links

- 📖 [YOLOv26 Documentation](https://docs.ultralytics.com/models/yolo26/)
- 🔗 [Ultralytics YOLOv26 GitHub](https://github.com/ultralytics/ultralytics)
- 📦 [PyPI Package](https://pypi.org/project/vogel-video-analyzer/)
- 🐛 [Issue Tracker](https://github.com/kamera-linux/vogel-video-analyzer/issues)

---

**Release Date:** 2026-02-22  
**Version:** 0.5.6  
**License:** MIT
