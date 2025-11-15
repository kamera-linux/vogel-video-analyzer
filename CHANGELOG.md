# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2025-11-14

### Added
- **Summary Video Feature** - Create compressed videos by skipping segments without bird activity
  - New `--create-summary` CLI flag to enable summary video creation
  - New `--summary-output PATH` for custom output location (optional)
  - New `--skip-empty-seconds FLOAT` to control minimum duration of bird-free segments to skip (default: 3.0)
  - New `--min-activity-duration FLOAT` to control minimum duration of bird activity to keep (default: 2.0)
  - Automatic output path generation: saves as `<original>_summary.mp4` in same directory
  - Intelligent segment detection using existing YOLO bird detection
  - Frame-by-frame analysis to identify continuous bird activity segments
  - Audio preservation with synchronous cutting (no pitch/speed changes)
  - Compression statistics: original duration, summary duration, compression ratio
  - Progress indicator during analysis and processing
  - Works with any video format supported by OpenCV/ffmpeg
  
- **i18n Support for Summary Feature**
  - Translations in English, German, and Japanese
  - Messages: summary_analyzing, summary_segments_found, summary_creating, summary_complete
  - Multi-video handling messages: summary_multiple_custom_path, summary_using_auto_path, summary_skip_multiple

### Technical Details
- Uses `ffmpeg concat demuxer` for efficient video concatenation
- No re-encoding required (uses `-c copy` for fast processing)
- Temporary segment files automatically cleaned up after processing
- Configurable thresholds allow fine-tuning of compression vs. content preservation
- Compatible with both single and multiple video batch processing

### Usage Examples
```bash
# Create summary with default settings (skip 3+ seconds, keep 2+ seconds)
vogel-video-analyzer --create-summary video.mp4

# Custom thresholds: skip 5+ seconds without birds, keep 1+ seconds with birds
vogel-video-analyzer --create-summary --skip-empty-seconds 5.0 --min-activity-duration 1.0 video.mp4

# Custom output path
vogel-video-analyzer --create-summary --summary-output /path/to/output.mp4 video.mp4

# Batch process multiple videos
vogel-video-analyzer --create-summary video1.mp4 video2.mp4 video3.mp4
```

## [0.3.0] - 2025-11-14

### Added
- **Video Annotation Feature** - Create annotated videos with bounding boxes and species labels
  - New `--annotate-video` CLI parameter (auto-generates output path)
  - New `--annotate-output PATH` for custom output location
  - Automatic output path generation: saves as `<original>_annotated.mp4` in same directory
  - Support for processing multiple videos at once
  - New `annotate_video()` method in VideoAnalyzer class
  - Bounding boxes around detected birds (green boxes, 3px width)
  - **Multilingual species labels** with `--multilingual` flag
  - Large, high-contrast text (34pt/38pt, black on white background)
  - Text positioned above bird to avoid covering subject
  - Timestamp and frame information display
  - Real-time progress indicator during processing
  - Audio preservation from original video (automatic ffmpeg merge)
  - Maintains original video resolution and framerate
  - Detection caching to prevent flickering bounding boxes
  
- **Multilingual Bird Names** - Species identification in multiple languages
  - English and German translations for all species
  - Japanese translations available (39 species total)
  - Format: "EN: Hawfinch / DE: Kernbeißer / 75%"
  - Three-line display for better readability
  - Unicode text rendering using PIL/Pillow
  - Support for German bird classifier model (kamera-linux/german-bird-classifier)
  - Reverse mapping: German labels → English keys → translations
  
- **Enhanced Bird Species Database**
  - Complete translations for 8 German model birds:
    - Blaumeise (Blue Tit / アオガラ)
    - Grünling (European Greenfinch / アオカワラヒワ)
    - Haussperling (House Sparrow / イエスズメ)
    - Kernbeißer (Hawfinch / シメ)
    - Kleiber (Eurasian Nuthatch / ゴジュウカラ)
    - Kohlmeise (Parus Major / シジュウカラ)
    - Rotkehlchen (European Robin / ヨーロッパコマドリ)
    - Sumpfmeise (Marsh Tit / ヨーロッパコガラ)
  - Total: 39 bird species with full EN/DE/JA translations
  
### Changed
- **Enhanced i18n Support** - Added German translations for all annotation messages
  - annotation_creating: "Erstelle annotiertes Video"
  - annotation_output: "Ausgabe"
  - annotation_video_info: "{width}x{height}, {fps} FPS, {frames} Frames"
  - annotation_processing: "Verarbeite jeden {n}. Frame..."
  - annotation_frames_processed: "Verarbeitete Frames: {processed}/{total}"
  - annotation_birds_detected: "Erkannte Vögel gesamt: {count}"
  - annotation_merging_audio: "Füge Audio vom Original-Video hinzu..."
  - annotation_audio_merged: "Audio erfolgreich hinzugefügt"
  - annotation_complete: "Annotiertes Video erfolgreich erstellt"
  
- **CLI Improvements**
  - `--annotate-video` is now a flag (no required argument)
  - Optional `--annotate-output PATH` for custom output location
  - Automatic path generation when no custom output specified
  - Support for batch processing multiple videos
  - Warning when using custom path with multiple videos (falls back to auto-path)

### Fixed
- **Unicode Rendering Issues** - Emoji and special character display
  - Replaced OpenCV cv2.putText with PIL/Pillow rendering for Unicode support
  - Fixed emoji rendering issues (removed emojis due to font compatibility)
  - Proper German umlaut support (ä, ö, ü, ß)
  - DejaVuSans font for Latin characters
  - No more box characters (□□□□□□) in video output
  
- **Text Visibility** - High contrast and proper positioning
  - Changed to black text (0,0,0) on white background (255,255,255)
  - Larger text box: 550px wide, 45px line height, 12px padding
  - Positioned above bird bounding box (10px gap) to avoid covering subject
  - Increased font sizes: 34pt (species names), 38pt (confidence)
  
- **Detection Flickering** - Smooth animation
  - Implemented detection caching with last_detections list
  - Bounding boxes preserved across frames without re-detection
  - Smoother video playback with consistent annotations

### Technical
- Uses OpenCV VideoWriter with 'mp4v' codec for video output
- PIL/Pillow for Unicode text rendering (RGB↔BGR conversion)
- ffmpeg integration for audio preservation
- Frame-by-frame processing with YOLO inference
- Optional species classification per detection (--species-threshold)
- Configurable sample rate for performance optimization
- Detection caching prevents flickering
- Automatic output path generation with pathlib
- Support for glob patterns in video paths

### Documentation
- **Updated READMEs** - All language variants now include v0.3.0 features
  - New "Video Annotation (v0.3.0+)" section with usage examples
  - Multilingual species identification documentation
  - Performance tips for faster processing
  - Batch processing examples
  - Audio preservation notes
  - Complete feature descriptions

### Requirements
- opencv-python for video processing
- PIL/Pillow for Unicode text rendering (installed with [species] extras)
- ffmpeg for audio merging (system package)
- transformers and torch for species classification (optional)

### Migration Notes
- Old syntax: `--annotate-video OUTPUT input.mp4`
- New syntax: `--annotate-video input.mp4` (auto-generates output)
- Custom output: `--annotate-video --annotate-output OUTPUT input.mp4`
- Multiple videos: `--annotate-video *.mp4` (each gets `*_annotated.mp4`)

## [0.2.3] - 2025-11-09

### Added
- **Japanese Language Support** - Full i18n support for Japanese users
  - Complete Japanese translations in i18n module
  - New `--language ja` CLI option
  - Japanese README (README.ja.md) with full documentation
  - Auto-detection of Japanese system locale

### Changed
- **Documentation Improvements** - Updated all README files
  - Fixed deprecated `--delete` parameter usage in archive examples
  - Updated to use `--delete-file` and `--delete-folder` parameters
  - Added language selector for Japanese in all READMEs
  - Clarified deletion options in use case examples

### Fixed
- **CLI Help Text** - Language choices now include Japanese (`en`, `de`, `ja`)
- **MANIFEST.in** - Now includes README.ja.md for PyPI distribution

## [0.2.2] - 2025-11-08

### Changed
- **Training Scripts Moved to Standalone Package** - Replaced `training/` directory with `vogel-model-trainer` package
  - Training tools now available via `pip install vogel-model-trainer`
  - Added `vogel-model-trainer` as Git submodule for development
  - Updated README to reference new training package
  - Cleaner separation of concerns between analysis and training

### Added
- **New CLI Parameter** - `--species-threshold` for fine-tuning species classification confidence
  - Default: 0.3 (balanced)
  - Range: 0.0-1.0 (lower = more detections, higher = more certain)
  - Example: `vogel-analyze --identify-species --species-threshold 0.5 video.mp4`
- **GitHub Actions Workflow** - Automated PyPI publishing
  - Automatic PyPI release on GitHub release creation
  - Manual TestPyPI deployment via workflow_dispatch
  - Automatic creation of GitHub release assets (wheel + tar.gz)
- **Improved Documentation** - Added threshold guidelines and usage examples

### Fixed
- **Critical Training Bug** - Fixed preprocessing inconsistency between training and inference
  - Training now uses `AutoImageProcessor` directly instead of manual transforms
  - Ensures consistent preprocessing between training and test/production
  - Resolves issue where trained models gave incorrect predictions
  - Mean pixel value difference reduced from 0.83 to 0.0

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
