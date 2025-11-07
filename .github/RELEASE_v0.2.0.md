# Release v0.2.0 - Bird Species Identification 🦜

**Release Date:** 2025-11-07

---

## 🎉 Major New Feature: Bird Species Identification

This release introduces **optional bird species identification** using state-of-the-art machine learning models from Hugging Face! Now you can not only detect birds in your videos but also identify what species they are.

### ✨ What's New

#### Bird Species Classification
- **Automatic species identification** for detected birds
- Uses pre-trained Hugging Face models (`chriamue/bird-species-classifier`)
- Shows species names with detection counts and confidence scores
- Completely **optional** - doesn't affect existing installations

#### New CLI Flag
```bash
# Enable species identification
vogel-analyze --identify-species video.mp4

# Works with all existing options
vogel-analyze --identify-species --sample-rate 10 --log *.mp4
```

#### Enhanced Reports
Species detection results are now shown in analysis reports:

```
🦜 Detected Species:
   3 species detected

  • Parus major (Great Tit)
    45 detections (avg confidence: 0.89)
  • Turdus merula (Blackbird)
    18 detections (avg confidence: 0.85)
  • Erithacus rubecula (European Robin)
    9 detections (avg confidence: 0.82)
```

---

## 📦 Installation

### Basic Installation (Bird Detection Only)
```bash
pip install vogel-video-analyzer
```

### With Species Identification Support
```bash
pip install vogel-video-analyzer[species]
```

**Note:** Species identification requires additional dependencies (~500MB):
- `transformers` - Hugging Face transformers library
- `torch` - PyTorch deep learning framework
- `torchvision` - Computer vision utilities for PyTorch
- `pillow` - Image processing library

On first use, the species classifier model (~100-300MB) will be downloaded automatically and cached locally for future use.

---

## 🔧 Technical Details

### Architecture
1. **YOLOv8** detects birds and their bounding boxes in video frames
2. **Species Classifier** analyzes each bird crop and identifies the species
3. **Results Aggregation** collects species statistics across all frames

### Features
- ✅ Graceful degradation - works without species dependencies installed
- ✅ Import guards prevent errors when optional packages missing
- ✅ Automatic model download and caching
- ✅ Offline-capable after initial model download
- ✅ Multilingual support (English/German)
- ✅ Integration with existing YOLO detection pipeline

### New Python API
```python
from vogel_video_analyzer import VideoAnalyzer

# Enable species identification
analyzer = VideoAnalyzer(
    model_path="yolov8n.pt",
    threshold=0.3,
    identify_species=True  # NEW parameter
)

stats = analyzer.analyze_video("bird_video.mp4")

# Access species statistics
if 'species_stats' in stats:
    for species, data in stats['species_stats'].items():
        print(f"{species}: {data['count']} detections")
```

---

## 📚 Documentation Updates

- ✅ Updated README.md with species identification examples
- ✅ Updated README.de.md with German translations
- ✅ Added installation instructions for `[species]` extras
- ✅ CLI help text updated with `--identify-species` flag
- ✅ New species-related translation keys (en/de)

---

## 🔄 Changes

### Added
- `--identify-species` CLI argument
- `BirdSpeciesClassifier` class in new `species_classifier.py` module
- Optional dependencies group `[species]` in `pyproject.toml`
- Species statistics in analysis output
- Species-related i18n translations
- Comprehensive documentation for species identification

### Changed
- `VideoAnalyzer.__init__()` accepts new `identify_species` parameter (default: `False`)
- Analysis reports include species section when enabled
- Package description mentions species identification

### Technical
- New module: `src/vogel_video_analyzer/species_classifier.py`
- Import guards: `SPECIES_AVAILABLE` flag
- Error handling for missing dependencies
- Species detection integrated into bird detection loop
- Bounding box extraction and crop classification
- Species statistics aggregation

---

## 🐛 Bug Fixes

No bug fixes in this release.

---

## ⚠️ Breaking Changes

**None** - This release is fully backward compatible. Species identification is completely optional and doesn't affect existing functionality.

---

## 🚀 Upgrade Instructions

### Existing Users (Bird Detection Only)
```bash
pip install --upgrade vogel-video-analyzer
```

Your existing code will continue to work exactly as before.

### New Users Wanting Species Identification
```bash
pip install vogel-video-analyzer[species]
```

### Upgrading to Add Species Support
```bash
pip install vogel-video-analyzer[species]
```

---

## 📊 Example Output Comparison

### Before (v0.1.4)
```
🎬 Video Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: bird_video.mp4
🐦 Bird Frames: 72 (80.0%)
✅ Status: Significant bird activity detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### After (v0.2.0 with --identify-species)
```
🎬 Video Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: bird_video.mp4
🐦 Bird Frames: 72 (80.0%)
✅ Status: Significant bird activity detected

🦜 Detected Species:
   3 species detected

  • Parus major (Great Tit)
    45 detections (avg confidence: 0.89)
  • Turdus merula (Blackbird)
    18 detections (avg confidence: 0.85)
  • Erithacus rubecula (European Robin)
    9 detections (avg confidence: 0.82)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🙏 Credits

- **Bird Species Model:** [chriamue/bird-species-classifier](https://huggingface.co/chriamue/bird-species-classifier) on Hugging Face
- **YOLOv8:** [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- **Transformers:** [Hugging Face Transformers](https://github.com/huggingface/transformers)

---

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

---

## 🔗 Links

- **PyPI:** https://pypi.org/project/vogel-video-analyzer/0.2.0/
- **GitHub:** https://github.com/kamera-linux/vogel-video-analyzer
- **Documentation:** [README.md](../README.md)
- **German Docs:** [README.de.md](../README.de.md)

---

**Thank you for using Vogel Video Analyzer! 🐦**
