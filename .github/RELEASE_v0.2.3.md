# Release v0.2.3 - Japanese Language Support & Documentation Improvements

**Release Date:** November 9, 2025

## 🎯 Highlights

- 🇯🇵 **Japanese Language Support** - Full internationalization for Japanese users
- 📚 **Documentation Updates** - Fixed deprecated parameter usage in READMEs
- 🌐 **Trilingual Support** - English, German, and Japanese now fully supported

---

## 🆕 What's New

### Japanese Language Support

Complete i18n support for Japanese-speaking users:

```bash
# Use Japanese language output
vogel-analyze --language ja video.mp4

# Auto-detection from system locale (ja_JP)
export LANG=ja_JP.UTF-8
vogel-analyze video.mp4
```

**Added:**
- ✅ Complete Japanese translations for all CLI messages
- ✅ Japanese README (README.ja.md) with full documentation
- ✅ Auto-detection of Japanese system locale
- ✅ Language selector in all README files

**Translated Elements:**
- Analysis reports and statistics
- Error messages and warnings
- Species identification output
- Deletion confirmations
- Progress indicators

---

## 📝 Documentation Improvements

### Fixed Deprecated Parameter Usage

Updated all README files to use current CLI parameters:

**Before (Deprecated):**
```bash
vogel-analyze --delete archive/**/*.mp4
```

**After (Current):**
```bash
# Delete only video files
vogel-analyze --delete-file archive/**/*.mp4

# Delete entire folders
vogel-analyze --delete-folder archive/**/*.mp4
```

### Updated Sections
- ✅ Archive Management examples
- ✅ Quality Control use cases
- ✅ Batch processing workflows

---

## 🌐 Language Support

### Available Languages

| Language | Code | README | CLI Support | Auto-Detection |
|----------|------|--------|-------------|----------------|
| English | `en` | ✅ README.md | ✅ | ✅ |
| German | `de` | ✅ README.de.md | ✅ | ✅ |
| Japanese | `ja` | ✅ README.ja.md | ✅ | ✅ |

### Usage Examples

```bash
# Explicit language selection
vogel-analyze --language en video.mp4  # English
vogel-analyze --language de video.mp4  # German
vogel-analyze --language ja video.mp4  # Japanese

# Auto-detection (uses system locale)
vogel-analyze video.mp4
```

### Environment Variables

```bash
# Set language via environment
export VOGEL_LANG=ja
vogel-analyze video.mp4

# Or via system locale
export LANG=ja_JP.UTF-8
export LC_ALL=ja_JP.UTF-8
vogel-analyze video.mp4
```

---

## 🔄 Changes Summary

### Added
- Japanese language translations (100+ strings)
- README.ja.md with complete documentation
- `ja` option to `--language` CLI parameter
- Japanese language auto-detection

### Changed
- Updated archive management examples in all READMEs
- Replaced `--delete` with `--delete-file` and `--delete-folder`
- Language selector now shows 🇯🇵 flag in all READMEs
- MANIFEST.in includes README.ja.md for PyPI

### Fixed
- Deprecated parameter usage in documentation
- Language choices in CLI help text
- Consistency across trilingual documentation

---

## 📦 Installation

No changes to installation process:

```bash
# Basic installation
pip install vogel-video-analyzer

# With species identification
pip install vogel-video-analyzer[species]

# Training tools (separate package)
pip install vogel-model-trainer
```

---

## 🗂️ Documentation

### README Files

- **English:** [README.md](README.md)
- **German:** [README.de.md](README.de.md)
- **Japanese:** [README.ja.md](README.ja.md)

### Other Resources

- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Training Guide:** [vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)
- **Issues:** [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)

---

## 🔗 Related Projects

- **vogel-model-trainer:** https://github.com/kamera-linux/vogel-model-trainer
- **Parent Project:** https://github.com/kamera-linux/vogel-kamera-linux

---

## ⚠️ Breaking Changes

None. This release is fully backward compatible.

---

## 📈 Language Support Roadmap

Future language additions are welcome! Community contributions for additional languages are encouraged.

**Potential Future Languages:**
- French 🇫🇷
- Spanish 🇪🇸
- Dutch 🇳🇱
- Polish 🇵🇱

To contribute translations, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🙏 Contributors

- **kamera-linux team** - Development, maintenance, and documentation
- **Community** - Feedback and feature requests

---

## 🎉 Thank You!

Special thanks to our international user base for requesting multi-language support!

---

**Enjoy the new release!** 🎉

For issues or questions, please visit: https://github.com/kamera-linux/vogel-video-analyzer/issues
