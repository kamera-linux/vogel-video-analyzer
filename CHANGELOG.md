# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-11-07

### Added
- Multilingual output support (English and German)
- `--language` parameter to manually set output language (en/de)
- Auto-detection of system language via LANG and VOGEL_LANG environment variables
- German README (`README.de.md`) for local community
- Language switcher in README files
- Internationalization (i18n) module for translations

### Changed
- All CLI output now respects system language settings
- Analysis reports translated to English/German
- Error messages and status updates localized
- Summary tables with translated headers

## [0.1.1] - 2025-11-07

### Added
- `--delete-file` option to delete only video files with 0% bird content
- `--delete-folder` option to delete entire parent folders with 0% bird content
- Virtual environment installation instructions in README (including venv setup for Debian/Ubuntu)
- Downloads badge from pepy.tech to README

### Changed
- Improved deletion safety with explicit `--delete-file` and `--delete-folder` options
- Updated README with clearer usage examples for deletion features
- Enhanced CLI help text with new deletion examples

### Deprecated
- `--delete` flag (use `--delete-file` or `--delete-folder` instead)
  - Still works for backward compatibility but shows deprecation warning

### Fixed
- License format in pyproject.toml updated to SPDX standard
- Badge formatting in README for better display

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

[0.1.1]: https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/kamera-linux/vogel-video-analyzer/releases/tag/v0.1.0
