# Release v0.1.2 - Multilingual Support

**Release Date:** 2025-11-07

## 🌍 Multilingual Output Support

This release adds comprehensive multilingual support to vogel-video-analyzer, making it accessible to both international and German-speaking users.

## ✨ New Features

### Language Support
- **Automatic Language Detection**: Detects system language from `LANG` environment variable
- **Manual Language Override**: New `--language` parameter (en/de)
- **German Translation**: Complete German localization of all output
- **Environment Variable**: `VOGEL_LANG` for persistent language preference

### Documentation
- **German README**: Full German translation (`README.de.md`)
- **Language Switcher**: Easy navigation between English and German docs
- **Internationalization Module**: Clean i18n architecture for future languages

## 🔧 Technical Changes

### New Command-Line Option
```bash
# Use German output
vogel-analyze --language de video.mp4

# Use English output
vogel-analyze --language en video.mp4

# Auto-detect from system
vogel-analyze video.mp4
```

### Translated Components
- Video analysis reports
- Error messages and warnings
- Summary tables and statistics
- Deletion confirmations
- Log messages
- Status indicators

### Language Auto-Detection Priority
1. `--language` command-line parameter
2. `VOGEL_LANG` environment variable
3. System `LANG` environment variable
4. Fallback to English

## 📚 Updated Documentation

- ✅ README.md - Added language switcher and --language parameter docs
- ✅ README.de.md - Complete German translation
- ✅ CHANGELOG.md - v0.1.2 entry

## 💡 Example Usage

```bash
# English (default on English systems)
$ vogel-analyze bird.mp4
🤖 Loading YOLO model: yolov8n.pt
📹 Analyzing: bird.mp4
   ✅ Analysis complete!

🎬 Video Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: bird.mp4
🐦 Bird Frames: 45 (75.0%)
✅ Status: Significant bird activity detected
```

```bash
# German (with --language de or on German systems)
$ vogel-analyze --language de bird.mp4
🤖 Lade YOLO-Modell: yolov8n.pt
📹 Analysiere: bird.mp4
   ✅ Analyse abgeschlossen!

🎬 Videoanalyse-Bericht
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Datei: bird.mp4
🐦 Vogel-Frames: 45 (75.0%)
✅ Status: Signifikante Vogelaktivität erkannt
```

## 🌐 Community Focus

This release strengthens our commitment to the German Vogel-Kamera-Linux community while maintaining international accessibility. All features work seamlessly in both languages.

## 📦 Installation

```bash
# Install or upgrade from PyPI
pip install --upgrade vogel-video-analyzer

# Or with virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install vogel-video-analyzer
```

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/vogel-video-analyzer/
- **GitHub Repository**: https://github.com/kamera-linux/vogel-video-analyzer
- **Documentation**: [README.md](../README.md) | [README.de.md](../README.de.md)
- **Issue Tracker**: https://github.com/kamera-linux/vogel-video-analyzer/issues

## 🙏 Acknowledgments

Special thanks to the Vogel-Kamera-Linux community for their feedback and support in making this tool more accessible to German-speaking users.

---

**Full Changelog**: https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.1.1...v0.1.2
