# Release v0.1.1 - Safer Deletion & Improved Documentation 🛡️

## 🎉 What's New

This release improves deletion safety with explicit control over what gets deleted, and enhances documentation for better user experience.

## 📋 Changes

### ✨ Added
- **`--delete-file`** - Delete only video files with 0% bird content (safer option)
- **`--delete-folder`** - Delete entire parent folders with 0% bird content  
- **Virtual Environment Setup** - Installation instructions including venv setup for Debian/Ubuntu
- **Downloads Badge** - Added download statistics badge to README

### 🔧 Changed
- **Improved Deletion Safety** - Explicit flags give users better control
- **Enhanced Documentation** - Clearer usage examples in README and CLI help
- **Better Badge Display** - Improved README badge formatting

### ⚠️ Deprecated
- **`--delete`** - Use `--delete-file` or `--delete-folder` instead
  - Still works for backward compatibility but shows deprecation warning
  - Defaults to `--delete-folder` behavior

### 🐛 Fixed
- License format in `pyproject.toml` updated to SPDX standard
- Badge formatting in README for consistent display

## 📦 Installation

```bash
pip install vogel-video-analyzer==0.1.1
```

Or with virtual environment (recommended):
```bash
# Install venv if needed (Debian/Ubuntu)
sudo apt install python3-venv

# Create and activate virtual environment
python3 -m venv ~/venv-vogel
source ~/venv-vogel/bin/activate

# Install package
pip install vogel-video-analyzer
```

## 🚀 New Usage Examples

### Safer Deletion Options

```bash
# Delete only video files (keeps folder structure)
vogel-analyze --delete-file --sample-rate 5 *.mp4

# Delete entire folders (more aggressive cleanup)
vogel-analyze --delete-folder --sample-rate 5 ~/Videos/*/*.mp4

# Old way (deprecated but still works)
vogel-analyze --delete ~/Videos/**/*.mp4  # Shows deprecation warning
```

## 🔄 Migration Guide

If you're using `--delete`:

**Before (v0.1.0):**
```bash
vogel-analyze --delete *.mp4
```

**After (v0.1.1):**
```bash
# Choose the appropriate option:
vogel-analyze --delete-file *.mp4     # Delete only files
# OR
vogel-analyze --delete-folder *.mp4   # Delete folders
```

The old `--delete` flag still works but will show a deprecation warning.

## 📚 Documentation

Full documentation: [README.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/README.md)

## 🔗 Links

- **PyPI:** https://pypi.org/project/vogel-video-analyzer/0.1.1/
- **Changelog:** [CHANGELOG.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/CHANGELOG.md)
- **Issues:** https://github.com/kamera-linux/vogel-video-analyzer/issues
- **Discussions:** https://github.com/kamera-linux/vogel-video-analyzer/discussions

## 🙏 Acknowledgments

Special thanks to:
- **Ultralytics** for the YOLOv8 framework
- **OpenCV** community for the computer vision library
- All contributors to the **Vogel-Kamera-Linux** project

---

**Full Changelog:** https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.1.0...v0.1.1

**Made with ❤️ by the Vogel-Kamera-Linux Team**
