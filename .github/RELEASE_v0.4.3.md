# Release v0.4.3: Internationalization & Documentation Updates

🌍 **Minor Update**: Complete internationalization and documentation improvements

---

## 🎯 Highlights

### 🌐 Complete Internationalization
- **Flag Directory Translation**: Console output now properly localized in all languages
  - 🇬🇧 English: "🏴 Flag directory:"
  - 🇩🇪 German: "🏴 Flaggen-Verzeichnis:"
  - 🇯🇵 Japanese: "🏴 フラグディレクトリ："
- **Consistent Localization**: All console messages respect language settings

### 📚 Documentation Improvements
- **Simplified Installation**: Removed deprecated `[species]` extra from all README files
- **Enhanced Parameter Docs**: Added comprehensive `--flag-dir` documentation
- **Updated Security Policy**: Version 0.4.x now officially supported

---

## 📦 What's Changed

### Fixed
- **Missing Translation**: Flag directory output message now translated in all languages
  - Previously: Hardcoded English "🏴 Flag directory:"
  - Now: Properly localized using i18n system
  - Affects: Console output during video annotation

### Changed
- **Documentation Updates**:
  - Removed `pip install vogel-video-analyzer[species]` (no longer needed)
  - Added `--flag-dir` parameter to main README
  - Updated feature list with hybrid flag rendering
  - SECURITY.md now lists 0.4.x as supported version
  - Consistent documentation across EN/DE/JA versions

---

## 🔄 Upgrade from v0.4.2

**No breaking changes** - This is a minor maintenance release.

### What's Different
```bash
# Before (v0.4.2)
🏴 Flag directory: assets/flags/

# After (v0.4.3) - Same output in English, but localized in DE/JA
🏴 Flaggen-Verzeichnis: assets/flags/  # German
🏴 フラグディレクトリ： assets/flags/   # Japanese
```

### Installation
```bash
# Standard update
pip install --upgrade vogel-video-analyzer

# Or specific version
pip install vogel-video-analyzer==0.4.3
```

---

## 💡 Usage

No changes to command-line usage - all existing commands work identically:

```bash
# Video annotation with flags (output now localized)
vogel-video-analyzer video.mp4 \
  --multilingual \
  --identify-species \
  --annotate-video \
  --flag-dir assets/flags/

# Language is auto-detected from system locale
LANGUAGE=de vogel-video-analyzer video.mp4 --annotate-video  # German output
LANGUAGE=ja vogel-video-analyzer video.mp4 --annotate-video  # Japanese output
```

---

## 📋 Complete Changes

### Code Changes
- **i18n.py**: Added `annotation_flag_directory` translation key to all languages
- **analyzer.py**: Updated to use `t('annotation_flag_directory')` instead of hardcoded string

### Documentation Changes
- **README.md**: Added `--flag-dir` examples, removed `[species]` extra
- **README.de.md**: Removed `[species]` extra
- **README.ja.md**: Removed `[species]` extra
- **SECURITY.md**: Updated supported versions table

---

## 🐛 Bug Fixes

### Internationalization Issue
**Problem**: Flag directory output was hardcoded in English  
**Impact**: Users with DE/JA locale saw mixed-language output  
**Solution**: Added proper i18n key and translations  

**Example Output:**
```bash
# German System (LANG=de_DE.UTF-8)
🎬 Erstelle annotiertes Video: video.mp4
   🏴 Flaggen-Verzeichnis: assets/flags/  # ✅ Now localized!
📁 Ausgabe: video_annotated_20251130_123456.mp4

# Japanese System (LANG=ja_JP.UTF-8)
🎬 注釈付きビデオを作成中： video.mp4
   🏴 フラグディレクトリ： assets/flags/  # ✅ Now localized!
📁 出力： video_annotated_20251130_123456.mp4
```

---

## 📚 Documentation

All documentation has been updated and synchronized:

### Main Documentation
- **README.md** (English): Added `--flag-dir` parameter documentation
- **README.de.md** (German): Synchronized with English version
- **README.ja.md** (Japanese): Synchronized with English version

### Security Policy
- **SECURITY.md**: Updated supported versions
  - ✅ 0.4.x - Supported
  - ✅ 0.3.x - Supported
  - ❌ 0.2.x - No longer supported

---

## 🔧 Technical Details

### Translation System
```python
# New translation key in i18n.py
TRANSLATIONS = {
    'en': {
        'annotation_flag_directory': '🏴 Flag directory:',
        # ...
    },
    'de': {
        'annotation_flag_directory': '🏴 Flaggen-Verzeichnis:',
        # ...
    },
    'ja': {
        'annotation_flag_directory': '🏴 フラグディレクトリ：',
        # ...
    }
}
```

### Updated Code
```python
# Before
print(f"   🏴 Flag directory: {flag_dir}")

# After
print(f"   {t('annotation_flag_directory')} {flag_dir}")
```

---

## 📊 Statistics

- **Files Changed**: 6
  - 2 code files (i18n.py, analyzer.py)
  - 4 documentation files (README.md, README.de.md, README.ja.md, SECURITY.md)
- **Lines Added**: ~20
- **Lines Removed**: ~40 (deprecated [species] references)
- **New Translations**: 3 (one per language)
- **Translation Keys**: 1 new key added

---

## 🌍 Language Support

Vogel Video Analyzer now has **complete** internationalization coverage:

| Feature | EN | DE | JA |
|---------|----|----|-----|
| Console Output | ✅ | ✅ | ✅ |
| Error Messages | ✅ | ✅ | ✅ |
| Progress Info | ✅ | ✅ | ✅ |
| Flag Directory | ✅ | ✅ | ✅ |
| Documentation | ✅ | ✅ | ✅ |

---

## 🙏 Credits

### Contributors
- **Development**: kamera-linux team
- **Testing**: Community feedback on localization
- **Documentation**: Multi-language README maintenance

---

## 🚀 Next Steps

### For Users
```bash
# 1. Upgrade to latest version
pip install --upgrade vogel-video-analyzer

# 2. Verify version
vogel-video-analyzer --version
# Should show: 0.4.3

# 3. Test localized output
LANGUAGE=de vogel-video-analyzer video.mp4 --annotate-video --flag-dir assets/flags/
```

### For Developers
- All i18n keys now complete
- Documentation synchronized across languages
- Ready for new feature development

---

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

---

## 🔗 Related Releases

- **v0.4.2** - Hybrid Flag Rendering System (2025-11-28)
- **v0.4.1** - Multilingual Species Names Fix (2025-11-24)
- **v0.4.0** - Enhanced Video Annotation (2025-11-23)

---

**Installation**:
```bash
pip install vogel-video-analyzer==0.4.3
```

**Repository**: https://github.com/kamera-linux/vogel-video-analyzer
