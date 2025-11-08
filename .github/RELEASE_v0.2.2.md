# Release v0.2.2 - Training Tools Separation & Species Threshold

**Release Date:** November 8, 2025

## 🎯 Highlights

- **Training Tools Separated** - `vogel-model-trainer` is now a standalone PyPI package
- **New CLI Parameter** - `--species-threshold` for fine-tuned species classification
- **Critical Bug Fix** - Fixed preprocessing inconsistency in training pipeline
- **Automated PyPI Publishing** - GitHub Actions workflow for seamless releases

---

## 🆕 What's New

### Standalone Training Package

The training scripts have been moved to a separate package for better modularity:

```bash
pip install vogel-model-trainer
```

**Benefits:**
- ✅ Cleaner separation between analysis and training
- ✅ Independent versioning and releases
- ✅ Easier maintenance and updates
- ✅ Reduced dependencies for core analyzer

The `training/` directory is now a Git submodule pointing to [vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer).

### New `--species-threshold` Parameter

Fine-tune species classification confidence:

```bash
# Lower threshold = more predictions (less certain)
vogel-analyze --identify-species --species-threshold 0.1 video.mp4

# Higher threshold = fewer predictions (more certain)
vogel-analyze --identify-species --species-threshold 0.7 video.mp4

# Default: 0.3 (balanced)
vogel-analyze --identify-species video.mp4
```

**Use Cases:**
- **Low threshold (0.1-0.2):** Exploratory analysis, maximize detections
- **Medium threshold (0.3-0.5):** General use, balanced accuracy
- **High threshold (0.6-0.9):** High-confidence only, minimize false positives

---

## 🐛 Bug Fixes

### Critical: Training Preprocessing Bug

**Problem:** Trained models produced incorrect predictions due to inconsistent preprocessing between training and inference.

**Root Cause:** 
- Training used manual transforms (`Resize` → `CenterCrop` → `ToTensor` → `Normalize`)
- Inference used `AutoImageProcessor` with different resize behavior
- Mean difference of 0.83 in normalized pixel values!

**Fix:** Training now uses `AutoImageProcessor` directly, ensuring identical preprocessing in both training and inference.

**Impact:** Custom-trained models will now work correctly! Previous models may need retraining.

---

## 🔄 Changes

### Training Workflow

**Before:**
```bash
# Scripts in vogel-video-analyzer/training/
python training/extract_birds.py video.mp4
python training/organize_dataset.py
python training/train_custom_model.py
```

**After:**
```bash
# Standalone package with CLI
pip install vogel-model-trainer

vogel-trainer extract video.mp4 --bird kohlmeise
vogel-trainer organize --source ~/data
vogel-trainer train
```

### Documentation Updates

- README now references `vogel-model-trainer` package
- Removed outdated training script paths
- Added installation instructions for training tools
- Updated workflow examples

---

## 🚀 New Features

### GitHub Actions Workflow

Automated PyPI publishing:
- ✅ Triggers on GitHub release creation
- ✅ Builds and validates package
- ✅ Publishes to PyPI automatically
- ✅ Creates release assets (wheel + tar.gz)
- ✅ Manual TestPyPI deployment via `workflow_dispatch`

---

## 📦 Installation

### Analyzer Only
```bash
pip install vogel-video-analyzer
```

### With Species Identification
```bash
pip install vogel-video-analyzer[species]
```

### Training Tools
```bash
pip install vogel-model-trainer
```

---

## 🔗 Related Projects

- **vogel-model-trainer:** https://github.com/kamera-linux/vogel-model-trainer
- **Parent Project:** https://github.com/kamera-linux/vogel-kamera-linux

---

## 📝 Full Changelog

### Added
- `--species-threshold` CLI parameter for species classification confidence tuning
- GitHub Actions workflow for automated PyPI publishing
- Git submodule for `vogel-model-trainer` at `training/`

### Changed
- Training scripts moved to standalone `vogel-model-trainer` package
- README updated to reference new training package
- Training preprocessing now uses `AutoImageProcessor` for consistency

### Fixed
- **Critical:** Fixed preprocessing inconsistency between training and inference
- Training transforms now match inference preprocessing exactly

### Removed
- Training scripts from `training/` directory (now in separate package)

---

## 🙏 Contributors

- **kamera-linux team** - Development and maintenance

---

## 📚 Documentation

- **Main README:** [README.md](README.md)
- **German README:** [README.de.md](README.de.md)
- **Full Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Training Guide:** [vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)

---

## ⚠️ Breaking Changes

None. The changes are backward compatible. Existing installations continue to work.

The `training/` directory scripts are still accessible via the submodule for development purposes.

---

## 🔮 What's Next (v0.3.0)

- Multi-threaded video processing
- Batch processing improvements
- Enhanced species classification models
- Performance optimizations

---

**Enjoy the new release!** 🎉

For issues or questions, please visit: https://github.com/kamera-linux/vogel-video-analyzer/issues
