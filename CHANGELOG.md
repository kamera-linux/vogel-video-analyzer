# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-11-07

### Added
- **German Translations** - Full i18n support for species names and UI messages
  - 30+ bird species names translated to German (Kohlmeise, Blaumeise, etc.)
  - All species-related UI messages now available in German
  - Automatic language detection from system locale
- **Custom Model Support** - Load locally trained models for species classification
  - Species classifier now accepts local file paths in addition to Hugging Face model IDs
  - Enables training custom models on specific bird species
- **Training Scripts** - New `training/` directory with tools for custom model training
  - `extract_birds.py` - Extract bird crops from videos for dataset creation
  - `organize_dataset.py` - Organize images into train/val splits
  - `train_custom_model.py` - Train custom EfficientNet-based classifier
  - `test_model.py` - Test trained models on validation data
  - Complete training documentation in `training/README.md`

### Changed
- **Default Species Model** - Changed from `dima806/bird_species_image_detection` to `chriamue/bird-species-classifier`
  - Higher confidence scores (0.3-0.6 vs 0.01-0.06)
  - Smaller model size (8.5M vs 86M parameters)
  - Better overall performance in testing
- **Default Confidence Threshold** - Increased from 0.1 to 0.3
  - Reduces false positives
  - Better aligned with chriamue model's confidence distribution

### Fixed
- **Critical:** Fixed species detection aggregation error ("unhashable type: 'list'")
- Species statistics are now correctly extracted from bird detections
- Improved error messages for species classification debugging

### Documentation
- Added experimental warning in species classifier docstring
- Noted that pre-trained models may misidentify European garden birds
- Documented custom model training workflow

### Technical
- Extract species detections from bird_detections before aggregation
- Changed bbox coordinate extraction to use individual array indexing
- Added Path-based detection for local model loading
- Added `format_species_name()` method with translation support
- Added `get_language()` function to i18n module

**Note:** Pre-trained models often misidentify European garden birds as exotic species. For best results with local bird species, consider training a custom model using the provided training scripts.

## [0.2.0] - 2025-11-07

### Added
- **Bird Species Identification** - New optional feature to identify bird species using Hugging Face models
- `--identify-species` CLI flag to enable species classification
- `BirdSpeciesClassifier` class using transformers library and pre-trained models
- Species statistics in analysis reports showing detected species with counts and confidence
- Optional dependencies group `[species]` for machine learning packages (transformers, torch, torchvision, pillow)
- Species-related translations in i18n module (en/de)
- Species detection examples in README.md and README.de.md
- Automatic model download and caching (~100-300MB on first use)

### Changed
- `VideoAnalyzer.__init__()` now accepts optional `identify_species` parameter
- Analysis reports now include detected species section when species identification is enabled
- Documentation updated with species identification installation and usage examples
- Package description updated to mention species identification capability

### Technical
- Species classifier uses chriamue/bird-species-classifier model from Hugging Face
- Graceful degradation when species dependencies are not installed
- Import guards prevent errors when optional dependencies missing
- Species classification integrated into YOLO bird detection pipeline
- Bounding box crops extracted and classified for each detected bird
- Aggregated species statistics with average confidence scores

**Installation:**
```bash
# Basic installation (bird detection only)
pip install vogel-video-analyzer

# With species identification support
pip install vogel-video-analyzer[species]
```

**Usage:**
```bash
vogel-analyze --identify-species video.mp4
```

## [0.1.4] - 2025-11-07

### Fixed
- **Critical:** Fixed `--log` functionality - output is now actually written to log files
- Log files are now properly created with console output redirected to both terminal and file
- Added proper cleanup with `finally` block to restore stdout/stderr and close log file

### Technical
- Implemented `Tee` class to write output to both console and log file simultaneously
- Proper file handle management with cleanup in exception cases

**Note:** `--log` flag in v0.1.0-v0.1.3 created empty log directories but didn't write any content.

## [0.1.3] - 2025-11-07

### Fixed
- **Critical:** Fixed missing translation keys in i18n module
- All CLI output and reports now properly translated in English and German
- Completed TRANSLATIONS dictionary with all required keys
- Fixed `model_not_found`, `video_not_found`, `cannot_open_video` translations
- Fixed all analyzer and CLI translation keys

### Technical
- Complete rewrite of i18n.py with comprehensive translation coverage
- All 55+ translation keys now properly defined for both languages

**Note:** v0.1.2 had incomplete translations and is superseded by this hotfix.

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
