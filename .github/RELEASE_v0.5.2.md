# Release v0.5.2 - Code Quality & Testing Improvements 🧪

**Release Date:** January 27, 2026

## 🎯 Overview

This maintenance release focuses on improving code quality, maintainability, and testing infrastructure. No new user-facing features, but significant improvements for developers and library users.

## ✨ What's New

### 📐 Module Constants (Public API)

Magic numbers have been replaced with named constants for better code clarity and maintainability:

```python
from vogel_video_analyzer import (
    COCO_CLASS_BIRD,              # 14 - COCO dataset class for birds
    DEFAULT_DETECTION_THRESHOLD,   # 0.3 - Bird detection confidence
    DEFAULT_SPECIES_THRESHOLD,     # 0.3 - Species classification confidence
    DEFAULT_SAMPLE_RATE,           # 5 - Frame sampling rate
    DEFAULT_FLAG_SIZE,             # 24 - Flag icon size in pixels
    DEFAULT_FONT_SIZE              # 20 - Annotation font size
)
```

**Benefits:**
- ✅ Better code documentation
- ✅ Easier to customize defaults
- ✅ Type-safe configuration
- ✅ IDE autocomplete support

**Example Usage:**
```python
from vogel_video_analyzer import VideoAnalyzer, DEFAULT_DETECTION_THRESHOLD

# Use default
analyzer = VideoAnalyzer(threshold=DEFAULT_DETECTION_THRESHOLD)

# Or customize with reference
analyzer = VideoAnalyzer(threshold=DEFAULT_DETECTION_THRESHOLD * 1.5)
```

### 🧪 Enhanced Test Suite

New pytest-compatible test infrastructure:

```bash
# Run with pytest
pytest tests/ -v

# Or standalone
python tests/test_version.py
```

**New Tests:**
- `test_version_format()` - Validates semantic versioning
- `test_module_imports()` - Verifies all exports
- `test_video_analyzer_class()` - Checks class structure
- `test_cli_main()` - Confirms CLI entry point
- `test_constants_exist()` - Validates module constants

**Test Coverage:**
- Improved from 8% to 13%
- All 6 tests passing ✅
- Full CI/CD integration ready

### 📚 Test Documentation

New `tests/README.md` with:
- pytest usage examples
- Standalone script instructions
- Test file descriptions
- Requirements and setup guide

### 🔧 Submodule Update

Training submodule updated to **v0.1.25**:
- New classifier, deduplicator, and evaluator modules
- Enhanced extractor with 16,000+ lines of improvements
- Japanese README translation (日本語)
- 25+ new release notes and documentation
- Comprehensive testing suite

## 📊 Technical Details

### Code Quality Improvements

**Before:**
```python
def __init__(self, model_path="yolov8n.pt", threshold=0.3, target_class=14):
    # Magic numbers scattered throughout code
```

**After:**
```python
def __init__(self, model_path="yolov8n.pt", 
             threshold=DEFAULT_DETECTION_THRESHOLD, 
             target_class=COCO_CLASS_BIRD):
    # Clear, documented constants
```

### Module Exports

All constants are now part of the public API:

```python
__all__ = [
    "VideoAnalyzer",
    "main",
    "__version__",
    "COCO_CLASS_BIRD",
    "DEFAULT_DETECTION_THRESHOLD",
    "DEFAULT_SPECIES_THRESHOLD",
    "DEFAULT_SAMPLE_RATE",
    "DEFAULT_FLAG_SIZE",
    "DEFAULT_FONT_SIZE"
]
```

## 🚀 Installation

```bash
# Upgrade to v0.5.2
pip install --upgrade vogel-video-analyzer

# With development dependencies
pip install --upgrade "vogel-video-analyzer[dev]"
```

## 🔄 Migration Guide

### For End Users
**No changes required!** This release is 100% backward compatible.

```bash
# Everything works exactly as before
vogel-analyze video.mp4
vogel-analyze --identify-species --html-report report.html video.mp4
```

### For Developers & Library Users

You can now use constants instead of hard-coded values:

```python
# Old way (still works)
analyzer = VideoAnalyzer(threshold=0.3, target_class=14)

# New way (recommended)
from vogel_video_analyzer import (
    VideoAnalyzer, 
    DEFAULT_DETECTION_THRESHOLD, 
    COCO_CLASS_BIRD
)
analyzer = VideoAnalyzer(
    threshold=DEFAULT_DETECTION_THRESHOLD, 
    target_class=COCO_CLASS_BIRD
)
```

## 📦 What's Included

### Files Changed
- ✅ `src/vogel_video_analyzer/__init__.py` - Version bump + exports
- ✅ `src/vogel_video_analyzer/analyzer.py` - Constants added
- ✅ `tests/test_version.py` - New pytest tests
- ✅ `tests/README.md` - Test documentation
- ✅ `training/` - Submodule update to v0.1.25
- ✅ `CHANGELOG.md` - Release notes

### No Breaking Changes
- All existing code continues to work
- All CLI commands unchanged
- All API signatures backward compatible
- All configuration options preserved

## 🧪 Testing

Run the test suite to verify your installation:

```bash
# With pytest (recommended)
pip install pytest pytest-cov
pytest tests/ -v

# Standalone
python tests/test_version.py
python tests/test_flag_rendering.py
```

Expected output:
```
================================================= 6 passed in 3.36s ==================================================
```

## 📝 Notes for Developers

### Using Constants in Your Code

```python
from vogel_video_analyzer import (
    VideoAnalyzer,
    COCO_CLASS_BIRD,
    DEFAULT_DETECTION_THRESHOLD,
    DEFAULT_SAMPLE_RATE
)

# Example: Custom analyzer with stricter threshold
strict_analyzer = VideoAnalyzer(
    threshold=DEFAULT_DETECTION_THRESHOLD + 0.2,  # 0.5 instead of 0.3
    target_class=COCO_CLASS_BIRD,
)

# Example: Fast analysis with higher sample rate
fast_stats = strict_analyzer.analyze_video(
    'video.mp4', 
    sample_rate=DEFAULT_SAMPLE_RATE * 2  # Every 10th frame
)
```

### Testing Your Integration

```python
import pytest
from vogel_video_analyzer import COCO_CLASS_BIRD

def test_my_custom_analyzer():
    """Ensure constants are available"""
    assert COCO_CLASS_BIRD == 14
    # Your tests here
```

## 🐛 Bug Fixes

No bugs fixed in this release (focused on quality improvements).

## 🔗 Related Resources

- **Full Changelog:** [CHANGELOG.md](../CHANGELOG.md)
- **Test Documentation:** [tests/README.md](../tests/README.md)
- **Training Tools:** [vogel-model-trainer v0.1.25](https://github.com/kamera-linux/vogel-model-trainer)
- **Previous Release:** [v0.5.1](RELEASE_v0.5.1.md)

## 💬 Feedback

Found an issue or have a suggestion? 
- 🐛 [Report a Bug](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- 💡 [Request a Feature](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- 📧 Email: kamera-linux@mailbox.org

---

**Thank you for using vogel-video-analyzer!** 🐦✨
