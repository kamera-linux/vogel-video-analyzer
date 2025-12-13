# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2025-12-13

### Fixed
- **HTML Reports**: Embedded Chart.js library inline for better compatibility
  - Charts now work in HTMLPreview.github.io and offline environments
  - No external CDN dependencies required
  - Self-contained HTML files work in all browsers without internet connection
  
### Changed
- HTML report file size increased by ~80KB due to inline Chart.js (still acceptable at ~460KB)

## [0.5.0] - 2025-12-12

### Added
- **HTML Report Generation**: Interactive HTML reports with charts and visualizations
  - `--html-report PATH` CLI parameter to generate visual reports
  - Activity timeline chart showing bird detections over time
  - Species distribution bar chart (top 10 species)
  - Interactive thumbnails from detected birds (requires `--identify-species`)
  - Responsive design for desktop and mobile viewing
  - Statistics cards: total detections, unique species, average confidence, frames with birds
  - Professional gradient styling with hover effects
  - Chart.js integration for data visualization

- **HTMLReporter Module**: New `reporter.py` module for report generation
  - Generates self-contained HTML files with embedded images
  - Thumbnails encoded as base64 (no external image dependencies)
  - Configurable `--max-thumbnails` parameter (default: 50)
  - Supports single video reports (multi-video planned for future)

### Usage Examples
```bash
# Generate HTML report with species identification
vogel-analyze --identify-species --html-report report.html video.mp4

# Custom thumbnail count
vogel-analyze --identify-species --html-report report.html --max-thumbnails 100 video.mp4

# Combined JSON and HTML output
vogel-analyze --identify-species -o data.json --html-report report.html video.mp4
```

### Technical Details
- Report generation uses analysis data from `analyzer.py`
- Timeline chart uses 10-second intervals for activity visualization
- Species chart sorted by detection count (descending)
- Thumbnails extracted from best confidence detections
- Graceful fallback when species identification not enabled

## [0.4.4] - 2025-12-12

### Performance
- **GPU Batch Processing**: Implemented efficient batch processing for species identification
  - New `classify_crops_batch()` method processes all bird crops per frame in single batch
  - Eliminates sequential GPU processing (no more "pipelines sequentially on GPU" warning)
  - Pipeline configured with `batch_size=8` for parallel inference
  - Up to 8x faster species identification on multi-bird frames
  - Processes up to 8 bird crops simultaneously on GPU

- **GPU Detection**: Enhanced device information display
  - Shows GPU model name on species classifier initialization
  - Example: "🎮 Using GPU: NVIDIA GeForce RTX 2070 SUPER"
  - Automatic fallback to CPU if no CUDA device available

### Technical Details
- **Analyzer Optimization**: Refactored species identification workflow
  - `analyze_video()`: Collects all bird bounding boxes per frame, then batch processes
  - `annotate_video()`: Same batch processing for video annotation
  - Reduced GPU memory transfers (single batch vs. multiple sequential calls)
  - Better GPU utilization through parallel processing

- **Species Classifier Enhancement**:
  - `classify_crops_batch(frame, bboxes, top_k=3)`: New batch processing method
  - Returns `List[List[Dict]]` - one prediction list per bounding box
  - Maintains threshold filtering per prediction
  - Preserves original `classify_crop()` for backward compatibility

### Testing
- Added `test_batch_processing.py` for feature validation
- Confirms GPU detection and batch processing functionality
- Tests both single and batch classification methods

## [0.4.3] - 2025-11-30

### Fixed
- **Documentation**: Removed deprecated `[species]` extra from all README files
  - Installation now simply: `pip install vogel-video-analyzer`
  - All dependencies are included by default
  - Updated README.md, README.de.md, and README.ja.md

- **i18n**: Added missing translation for flag directory output
  - English: "🏴 Flag directory:"
  - German: "🏴 Flaggen-Verzeichnis:"
  - Japanese: "🏴 フラグディレクトリ："
  - Flag directory message now properly localized in all languages

### Changed
- **Security Policy**: Updated supported versions table
  - 0.4.x: ✅ Supported
  - 0.3.x: ✅ Supported
  - 0.2.x and older: ❌ Not supported

### Documentation
- Added `--flag-dir` parameter documentation to main README
- Added usage examples with PNG flag icons
- Updated features list with hybrid flag rendering
- Clarified installation instructions (removed [species] confusion)

## [0.4.2] - 2025-11-28

### Fixed
- **Internationalization**: Added missing translation for flag directory output message
  - English: "🏴 Flag directory:"
  - German: "🏴 Flaggen-Verzeichnis:"
  - Japanese: "🏴 フラグディレクトリ："
  - Console output now properly localized in all supported languages

### Changed
- **Documentation**: Removed deprecated `[species]` installation extra from all README files
  - Updated main README.md with `--flag-dir` parameter documentation
  - Added hybrid flag rendering to features list
  - Updated SECURITY.md supported versions (0.4.x now supported)
  - Simplified installation instructions across all language versions

## [0.4.2] - 2025-11-28

### Added
- **Hybrid Flag Rendering System**: New flexible flag icon rendering with multiple input methods
  - Support for PNG/JPG flag image files via `--flag-dir` parameter
  - Automatic fallback to pixel-rendered flags if image files not available
  - Five input methods: emoji strings, file paths, country codes, PIL Images, NumPy arrays
  - Included high-quality Public Domain flag images for DE, GB, JP from Wikimedia Commons
  - Flag images (150x90px, 150x75px, 150x100px) in `assets/flags/` directory
  - Auto-detection of flag directory (uses `module_dir/assets/flags/` if not specified)
  - Maintains 3:2 aspect ratio with LANCZOS resampling for quality

- **New Functions**:
  - `render_flag_from_file()`: Load and resize flag images from PNG/JPG files
  - `render_flag_icon()`: Unified hybrid rendering function supporting multiple input types
  - Enhanced `put_unicode_text()` with `flag_dir` parameter for custom flag paths
  - Extended `annotate_video()` with `flag_dir` parameter and auto-detection

- **CLI Enhancement**:
  - New `--flag-dir PATH` parameter to specify custom flag image directory
  - Usage: `vogel-video-analyzer video.mp4 --flag-dir assets/flags/ --multilingual --annotate-video`

- **Documentation**:
  - `docs/FLAG_RENDERING.md`: Complete guide for hybrid flag rendering system
  - `assets/flags/README.md`: Usage instructions and examples
  - `assets/flags/LICENSE`: Public Domain license documentation for included flags
  - `tests/test_flag_rendering.py`: Comprehensive test suite for all rendering methods

- **Package Distribution**:
  - Updated `MANIFEST.in` to include flag assets in distribution
  - Flag images bundled with package for immediate use

### Fixed
- **Japanese Text Rendering**: Fixed missing Japanese characters (シジュウカラ) in annotations
  - Requires CJK font installation: `sudo apt-get install fonts-noto-cjk`
  - Multi-font system properly selects CJK font for Japanese text
  - Auto-detection of CJK characters in text

- **Flag Icon Display**: Changed from emoji strings to country codes for hybrid rendering
  - Now uses country codes ('gb', 'de', 'jp') instead of emoji strings ('🇬🇧', '🇩🇪', '🇯🇵')
  - Enables automatic PNG loading when flag images available
  - Seamless fallback to pixel rendering when images not found

### Technical Details
- Flag rendering priority: PNG/JPG file → emoji fallback → pixel rendering → None
- Supported image formats: PNG, JPG, JPEG
- Flag sources: Wikimedia Commons (Public Domain)
- Path resolution: Absolute and relative paths supported
- Transparent integration with existing annotation pipeline

## [0.4.1] - 2025-11-24

### Fixed
- **Multilingual Species Names**: Corrected English bird names to use proper common names instead of scientific names
  - Example: "Great Tit" instead of "Parus Major"
  - Added `ENGLISH_NAMES` dictionary with correct English common names for all 8 species from kamera-linux/german-bird-classifier
  - Species: Great Tit, Blue Tit, Marsh Tit, Eurasian Nuthatch, European Greenfinch, Hawfinch, House Sparrow, European Robin
- **German Translation**: Corrected "European Greenfinch" translation from "Grünling" to "Grünfink"
- **Video Annotation**: Fixed multilingual rendering to properly use English common names with flag icons

### Technical Details
- Added `ENGLISH_NAMES` lookup dictionary in `species_classifier.py`
- Updated `analyzer.py` to import and use `ENGLISH_NAMES` for proper English name display
- Maintained backward compatibility with existing translation system

## [0.4.0] - 2025-11-23

### Added
- **Enhanced Video Annotation Features**
  - Configurable font size with `--font-size` parameter (default: 20, range: 12-32)
  - Timestamped output filenames to prevent overwriting (`video_annotated_YYYYMMDD_HHMMSS.mp4`)
  - Flag icons for multilingual labels (🇬🇧 🇩🇪 🇯🇵) using custom-rendered flag designs
  - Accurate flag representations:
    - 🇩🇪 Germany: Black-Red-Gold horizontal stripes
    - 🇬🇧 UK: Simplified Union Jack with crosses
    - 🇯🇵 Japan: Red circle on white background
  - Label positioning changed from above to right side of detected bird
  - Semi-transparent label backgrounds (70% opacity) for better visibility
  - Synchronized font sizes for species labels and frame info

- **Species Classification Improvements**
  - Fixed `--species-threshold` bug where low-confidence predictions were shown despite threshold setting
  - Detections below threshold are now properly skipped (no fallback to best prediction)
  - Improved confidence filtering for cleaner annotation outputs

- **CJK Font Support**
  - Added Japanese language support with proper rendering
  - Multi-font system: DejaVu/Noto for Latin text, NotoSansCJK for Japanese characters
  - Automatic font fallback for unsupported characters

### Fixed
- Species threshold now correctly filters predictions (previously always showed best match)
- Flag colors now render correctly (RGB/BGR conversion issues resolved)
- Japanese characters now display properly in video annotations

### Changed
- Label box position moved from above bird to right side for better visibility
- Label background changed to semi-transparent (70% opacity)
- Frame info text size now synchronized with species label size

### Technical Details
- Flag rendering using numpy arrays with OpenCV drawing primitives
- Proper color space handling between PIL (RGB) and OpenCV (BGR)
- Multi-font rendering with PIL.ImageFont for Unicode support
- Custom flag designs rendered at runtime (no external image files needed)

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
