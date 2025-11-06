# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-06

### Added
- Initial release of vogel-video-analyzer
- YOLOv8-based bird detection in videos
- Command-line interface (`vogel-analyze`)
- Python library API (`VideoAnalyzer` class)
- Configurable sample rate for performance optimization
- Segment detection for continuous bird presence
- JSON export functionality
- Auto-delete feature for videos without bird content
- Structured logging support
- Model search in multiple directories
- Comprehensive documentation and examples

### Features
- Frame-by-frame video analysis
- Bird content percentage calculation
- Detailed statistics generation
- Multiple video batch processing
- Progress indicators
- Formatted console reports

### Technical
- Python 3.8+ support
- OpenCV integration
- Ultralytics YOLOv8 integration
- MIT License
- PyPI package structure with modern pyproject.toml

---

[0.1.0]: https://github.com/kamera-linux/vogel-video-analyzer/releases/tag/v0.1.0
