# Release v0.5.7: YOLO Model Auto-Download Improvements

## 🔧 Improved Model Loading & Download Handling

This release improves the YOLO model loading pipeline with better error handling, auto-download support, and enhanced diagnostics for common issues.

### ✨ Improvements

- **Better Auto-Download Support** - Automatically downloads `yolo26n.pt` from Ultralytics Hub if not locally available
- **Enhanced Error Handling** - Clear error messages when model loading fails
- **Diagnostic Information** - Helpful troubleshooting steps included in error messages
- **Clearer Feedback** - Better user feedback during the model loading process
- **Offline/Online Support** - Works seamlessly whether models are pre-cached or need downloading

### 🐛 Fixed Issues

- **FileNotFoundError for Missing Models** - Fixed `[Errno 2] No such file or directory: 'yolo26n.pt'` error
- **Ultralytics Hub Download** - Model now properly triggers automatic download when missing locally
- **Download Path Detection** - Improved YOLO model detection for automatic Ultralytics Hub access

### 📝 What's Changed

#### Enhanced Model Loading
- Improved `_find_model()` method with better YOLO model detection
- Explicit download notifications when models need to be fetched
- Better error handling in `VideoAnalyzer.__init__()`

#### Better Error Messages
When model loading fails, users now get:
```
❌ error_loading_model: [Errno 2] No such file or directory: 'yolo26n.pt'

🔧 Troubleshooting steps:
   1. Ensure internet connection (for auto-download)
   2. Update Ultralytics: pip install --upgrade 'ultralytics>=8.4.14'
   3. Check disk space (~50MB for yolo26n.pt model)
   4. Verify YOLO cache directory: ls -la ~/.cache/yolo/ (Linux/Mac)
   
   Alternatively, manually download from:
   https://github.com/ultralytics/assets/releases/
```

#### Clearer Download Flow
Model loading now clearly indicates when automatic download is attempting:
```
🤖 Lade YOLO-Modell: yolo26n.pt
   ℹ️  Model 'yolo26n.pt' not found locally
      Attempting automatic download from Ultralytics...
```

### 🔄 Backward Compatibility

**Fully backward compatible!**
- No changes to public API
- Existing code works without modification
- Improved reliability for edge cases

### Installation & Upgrade

```bash
# Upgrade from PyPI
pip install --upgrade vogel-video-analyzer

# Or from source
git clone https://github.com/kamera-linux/vogel-video-analyzer.git
cd vogel-video-analyzer
pip install -e .
```

### Using v0.5.7

```bash
# Works seamlessly with automatic model download
vogel-analyze video.mp4

# With species identification
vogel-analyze --identify-species video.mp4

# With custom settings
vogel-analyze --identify-species --sample-rate 10 --html-report report.html video.mp4
```

### Technical Details

#### Model Loading Priority

Models are searched in this order:
1. `models/` directory (local)
2. `config/models/` directory (local)
3. Current directory
4. **Ultralytics Hub** (automatic download on first use)

#### Download Behavior

- **First Run**: Model automatically downloads (~5-50 MB depending on YOLOv26 variant)
- **Cached**: Subsequent runs use locally cached model
- **Manual Override**: Can specify custom model with `--model /path/to/model.pt`

#### YOLO Cache Locations

- **Linux/macOS**: `~/.cache/yolo/`
- **Windows**: `C:\Users\<username>\AppData\Local\yolo\`

#### Requirements

Ensure you have:
- `ultralytics>=8.4.14` - Provides YOLOv26 support
- `torch>=2.0.0` - Deep learning framework
- **Internet connection** - For first-run model download (or pre-cache locally)
- **~50 MB disk space** - For model storage

### Troubleshooting

#### "No such file or directory: 'yolo26n.pt'"

1. ✅ Check internet connection
2. ✅ Update Ultralytics: `pip install --upgrade 'ultralytics>=8.4.14'`
3. ✅ Check YOLO cache permissions: `ls -la ~/.cache/yolo/`
4. ✅ Verify disk space: `df -h`

#### "Failed to load model"

Run with verbose output:
```bash
vogel-analyze --log video.mp4
```

This generates detailed logs to help diagnose the issue.

### Known Limitations

- First model download requires internet connectivity
- Model download speed depends on network bandwidth (typically 30-60 seconds)
- Ultralytics Hub must be accessible (no proxy limitations expected)

### Contributes To

This release improves reliability for:
- 🌐 Cloud deployments with automatic dependency resolution
- 📦 Docker containers that fetch models at runtime
- 🔄 CI/CD pipelines with model caching strategies
- 👥 Automated batch processing workflows

### Support

For issues or questions:
- 📘 [Documentation](https://github.com/kamera-linux/vogel-video-analyzer)
- 🐛 [Report Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- 💬 [Discussions](https://github.com/kamera-linux/vogel-video-analyzer/discussions)

### Changelog

Full changelog: [`v0.5.6...v0.5.7`](https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.5.6...v0.5.7)
