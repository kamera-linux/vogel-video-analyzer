# Release v0.1.0 - Initial Release 🎉

## 🎉 What's New

**Vogel Video Analyzer** is now available! This is the first official release of our YOLOv8-based video analysis tool for automated bird content detection and quantification.

## 📋 Changes

### ✨ Added
- **YOLOv8-powered Detection** - Accurate bird detection using state-of-the-art models
- **Command-line Interface** - Easy-to-use `vogel-analyze` CLI tool
- **Python Library API** - `VideoAnalyzer` class for programmatic integration
- **Configurable Sample Rate** - Process every Nth frame for faster analysis
- **Segment Detection** - Identify continuous time periods with bird presence
- **JSON Export** - Generate structured reports for archival and further analysis
- **Auto-Delete Feature** - Automatically remove videos without bird content
- **Structured Logging** - Comprehensive logs for batch processing workflows
- **Multi-directory Model Search** - Flexible model file location
- **Batch Processing** - Analyze multiple videos in one command
- **Progress Indicators** - Visual feedback during analysis
- **Formatted Console Reports** - Clear, readable output

### 📚 Technical Details
- Python 3.8+ support (tested on 3.8 through 3.13)
- OpenCV integration for video processing
- Ultralytics YOLOv8 for object detection
- Modern `pyproject.toml` package structure
- MIT License
- Comprehensive documentation with examples

## 📦 Installation

```bash
pip install vogel-video-analyzer==0.1.0
```

## 🚀 Quick Start

```bash
# Analyze a single video
vogel-analyze video.mp4

# Faster analysis (every 5th frame)
vogel-analyze --sample-rate 5 video.mp4

# Export to JSON
vogel-analyze --output report.json video.mp4
```

## 📚 Documentation

Full documentation: [README.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/README.md)

## 🔗 Links

- **PyPI:** https://pypi.org/project/vogel-video-analyzer/0.1.0/
- **Changelog:** [CHANGELOG.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/CHANGELOG.md)
- **Issues:** https://github.com/kamera-linux/vogel-video-analyzer/issues
- **Discussions:** https://github.com/kamera-linux/vogel-video-analyzer/discussions

## 🙏 Acknowledgments

Special thanks to:
- **Ultralytics** for the YOLOv8 framework
- **OpenCV** community for the computer vision library
- All contributors to the **Vogel-Kamera-Linux** project

---

**Made with ❤️ by the Vogel-Kamera-Linux Team**
