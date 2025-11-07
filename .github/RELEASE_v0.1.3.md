# Release v0.1.3 - Hotfix: Complete i18n Implementation

**Release Date:** 2025-11-07  
**Type:** Hotfix

## 🚨 Critical Fix

This is a **hotfix release** that fixes critical issues in v0.1.2 where translation keys were missing from the i18n module, causing the multilingual feature to not work correctly.

## 🐛 Fixed Issues

### Missing Translation Keys
v0.1.2 introduced multilingual support but had an incomplete `TRANSLATIONS` dictionary in the i18n module. Many translation keys used in `analyzer.py` and `cli.py` were not defined, causing the application to fall back to displaying the key names instead of translated text.

### What Was Fixed
- ✅ Complete rewrite of `i18n.py` with all 55+ translation keys
- ✅ All analyzer output messages now properly translated
- ✅ All CLI messages and errors now properly translated
- ✅ Format string support for dynamic translations (e.g., `{model_name}`, `{path}`)
- ✅ Verified translations work in both English and German

## 📝 Complete Translation Coverage

### Added Translation Keys
- `loading_model`, `model_not_found`
- `analyzing`, `video_not_found`, `cannot_open_video`
- `video_info`, `frames`, `analyzing_every_nth`
- `analysis_complete`, `analysis_interrupted`
- `report_*` keys (title, file, duration, segments, status)
- `summary_*` keys (title, overview, statistics)
- `delete_*` keys (files, folders, success, error)
- `log_*` keys (file, permissions, hints)
- `error`, `error_analyzing`, `report_saved`

All keys are available in both **English** and **German**.

## 🧪 Testing

```bash
# Test English output
vogel-analyze --language en video.mp4

# Test German output  
vogel-analyze --language de video.mp4

# Auto-detect from system (default)
vogel-analyze video.mp4
```

## 📦 Migration from v0.1.2

If you installed v0.1.2, simply upgrade:

```bash
pip install --upgrade vogel-video-analyzer
```

**v0.1.2 users:** Please upgrade immediately to v0.1.3 for working multilingual support.

## 🔍 Technical Details

### Before (v0.1.2)
```python
# Only ~20 translation keys defined
# Many keys missing → fallback to key names
print(t('loading_model'))  # Output: "loading_model" ❌
```

### After (v0.1.3)
```python
# All 55+ translation keys properly defined
print(t('loading_model'))  # Output: "Loading YOLO model:" ✅
print(t('loading_model'))  # Output: "Lade YOLO-Modell:" ✅ (de)
```

## 📋 Changelog

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/vogel-video-analyzer/0.1.3/
- **GitHub Repository**: https://github.com/kamera-linux/vogel-video-analyzer
- **Issue Tracker**: https://github.com/kamera-linux/vogel-video-analyzer/issues

---

**Full Changelog**: https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.1.2...v0.1.3
