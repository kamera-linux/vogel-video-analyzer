# Release v0.4.1 - Multilingual Species Names Fix

**Release Date:** November 24, 2025

A critical bugfix release that corrects English bird name translations in multilingual video annotations.

---

## 🐛 Bug Fixes

### Multilingual Species Names Correction

**Problem:** The multilingual annotation feature was displaying scientific Latin names (e.g., "Parus Major") instead of proper English common names (e.g., "Great Tit") in video annotations.

**Solution:** 
- ✅ Added `ENGLISH_NAMES` dictionary with correct English common names for all 8 species
- ✅ Updated video annotation rendering to use proper English names
- ✅ Corrected German translation: "Grünling" → "Grünfink" (European Greenfinch)

**Affected Species (kamera-linux/german-bird-classifier):**
1. **Great Tit** (was: "Parus Major") - Kohlmeise - シジュウカラ
2. **Blue Tit** (was: "Blue Tit") - Blaumeise - アオガラ
3. **Marsh Tit** (was: "Marsh Tit") - Sumpfmeise - ヨーロッパコガラ
4. **Eurasian Nuthatch** (was: "Eurasian Nuthatch") - Kleiber - ゴジュウカラ
5. **European Greenfinch** (was: "European Greenfinch") - Grünfink - アオカワラヒワ
6. **Hawfinch** (was: "Hawfinch") - Kernbeißer - シメ
7. **House Sparrow** (was: "House Sparrow") - Haussperling - イエスズメ
8. **European Robin** (was: "European Robin") - Rotkehlchen - ヨーロッパコマドリ

### Before & After

**Before (v0.4.0):**
```
🇬🇧 Parus Major
🇩🇪 Kohlmeise
🇯🇵 シジュウカラ
```

**After (v0.4.1):**
```
🇬🇧 Great Tit
🇩🇪 Kohlmeise
🇯🇵 シジュウカラ
```

---

## 📦 Installation

### Upgrade from v0.4.0

```bash
# Upgrade to v0.4.1
pip install --upgrade vogel-video-analyzer

# With species identification support
pip install --upgrade vogel-video-analyzer[species]
```

### Fresh Installation

```bash
# Basic installation
pip install vogel-video-analyzer==0.4.1

# With species identification
pip install vogel-video-analyzer[species]==0.4.1
```

---

## 🔧 Technical Details

### Files Modified

1. **`species_classifier.py`**
   - Added `ENGLISH_NAMES` dictionary mapping scientific names to English common names
   - Updated `get_multilingual_name()` to return German name only (rendering code handles multilingual display)

2. **`analyzer.py`**
   - Updated import to include `ENGLISH_NAMES`
   - Modified English name generation to use `ENGLISH_NAMES.get()` instead of title-case formatting
   - Maintains proper flag icon rendering with correct names

3. **`BIRD_NAME_TRANSLATIONS`**
   - Updated German translation for European Greenfinch: "Grünling" → "Grünfink"

### Backward Compatibility

✅ Fully backward compatible with v0.4.0
✅ No changes to CLI arguments or Python API
✅ Existing scripts and workflows continue to work unchanged

---

## 📖 Usage Examples

### Multilingual Video Annotation

```bash
# Analyze video with corrected multilingual labels
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --multilingual \
  --annotate-video \
  --font-size 16 \
  video.mp4
```

Output will now show:
- 🇬🇧 **Great Tit** (correct English common name)
- 🇩🇪 **Kohlmeise** (German name)
- 🇯🇵 **シジュウカラ** (Japanese name)

### Without Multilingual Mode

```bash
# Default behavior (German names only)
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --annotate-video \
  video.mp4
```

---

## 🔗 Links

- **GitHub Repository:** [vogel-video-analyzer](https://github.com/kamera-linux/vogel-video-analyzer)
- **PyPI Package:** [vogel-video-analyzer](https://pypi.org/project/vogel-video-analyzer/)
- **Documentation:** [README.md](../README.md)
- **Changelog:** [CHANGELOG.md](../CHANGELOG.md)
- **Training Tool:** [vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)

---

## 🙏 Acknowledgments

Thanks to all users who reported the scientific name display issue. Your feedback helps improve the accuracy and usability of vogel-video-analyzer!

---

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for the complete version history.

---

**Previous Release:** [v0.4.0](RELEASE-v0.4.0.md) - Enhanced Video Annotation  
**Next Release:** TBD
