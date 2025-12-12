# Release v0.4.0 - Enhanced Video Annotation

**Release Date:** 2025-11-23

## 🎉 What's New

### Enhanced Video Annotation Features

- **Configurable Font Sizes** - New `--font-size` parameter (default: 20, range: 12-32) for optimal readability
- **Timestamped Outputs** - Automatic timestamp in filenames to prevent overwriting (`video_annotated_YYYYMMDD_HHMMSS.mp4`)
- **Flag Icons** - Beautiful flag representations for multilingual labels:
  - 🇩🇪 Germany: Black-Red-Gold horizontal stripes
  - 🇬🇧 UK: Simplified Union Jack with crosses
  - 🇯🇵 Japan: Red circle on white background
- **Improved Label Positioning** - Labels now positioned to the right of detected birds
- **Semi-Transparent Backgrounds** - Label boxes with 70% opacity for better visibility
- **Synchronized Font Sizes** - Species labels and frame info now use consistent sizing

### Species Classification Improvements

- **Fixed Species Threshold Bug** - `--species-threshold` now correctly filters predictions
  - Previously: Always showed best match regardless of threshold
  - Now: Only shows predictions meeting the confidence threshold
- **Better Confidence Filtering** - Cleaner annotation outputs with proper threshold enforcement

### CJK Font Support

- **Japanese Language Support** - Full support for Japanese bird names with proper rendering
- **Multi-Font System** - Automatic font fallback (DejaVu/Noto for Latin, NotoSansCJK for Japanese)
- **Unicode Rendering** - Proper display of all characters across languages

## 🐛 Bug Fixes

- Fixed species threshold ignoring low-confidence predictions
- Fixed flag color rendering issues (RGB/BGR conversion)
- Fixed Japanese character display in video annotations

## 🔧 Technical Improvements

- Custom flag rendering using numpy arrays and OpenCV primitives
- Proper color space handling between PIL (RGB) and OpenCV (BGR)
- Multi-font rendering with PIL.ImageFont for Unicode support
- Runtime flag generation (no external image files needed)

## 📦 Installation

```bash
pip install vogel-video-analyzer==0.4.0

# With species identification support
pip install vogel-video-analyzer[species]==0.4.0
```

## 📖 Usage Examples

### Basic annotation with all new features
```bash
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --species-threshold 0.5 \
  --multilingual \
  --annotate-video \
  --font-size 16 \
  video.mp4
```

### Batch processing with custom styling
```bash
vogel-analyze --identify-species \
  --multilingual \
  --annotate-video \
  --font-size 18 \
  --species-threshold 0.6 \
  *.mp4
```

## 🔗 Links

- [Full CHANGELOG](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/CHANGELOG.md)
- [Documentation](https://github.com/kamera-linux/vogel-video-analyzer#readme)
- [Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)

## 👥 Contributors

Thank you to everyone who contributed to this release!
