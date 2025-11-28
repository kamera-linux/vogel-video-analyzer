# Release v0.4.2: Hybrid Flag Rendering System

🎨 **Major Enhancement**: Flexible flag rendering with PNG/JPG image support and automatic fallback

---

## 🎯 Highlights

### 🏴 Hybrid Flag Rendering System
- **Multiple Input Methods**: Support for PNG/JPG files, emoji strings, country codes, PIL Images, and NumPy arrays
- **High-Quality Flags**: Includes Public Domain flag images (DE, GB, JP) from Wikimedia Commons
- **Automatic Fallback**: Seamlessly falls back to pixel rendering if image files not available
- **Custom Flag Directories**: New `--flag-dir` parameter to specify custom flag image locations

### ✨ Enhanced Display Quality
- **Sharp Flag Icons**: Uses high-quality PNG images (150x90px, 150x75px, 150x100px) with LANCZOS resampling
- **Fixed Japanese Text**: Properly displays Japanese characters (シジュウカラ) with CJK font support
- **Flexible Configuration**: Choose between bundled flags or provide custom flag images

---

## 📦 What's New

### Added
- **`render_flag_from_file()`**: Load and resize flag images from PNG/JPG files
- **`render_flag_icon()`**: Unified hybrid rendering function with 5 input types
- **`--flag-dir PATH`**: CLI parameter to specify custom flag image directory
- **Flag Assets**: Bundled DE, GB, JP flags in `assets/flags/` (Public Domain)
- **Comprehensive Documentation**: 
  - `docs/FLAG_RENDERING.md`: Complete usage guide
  - `assets/flags/README.md`: Flag usage instructions
  - `tests/test_flag_rendering.py`: Test suite for all methods

### Fixed
- **Japanese Text Rendering**: Fixed missing シジュウカラ characters
  - Solution: Install CJK fonts with `sudo apt-get install fonts-noto-cjk`
- **Flag Loading**: Changed from emoji strings to country codes for proper PNG loading
- **Automatic Detection**: Flag directory auto-detection from module location

---

## 💡 Usage Examples

### Basic Usage with Bundled Flags
```bash
# Uses bundled PNG flags automatically
vogel-video-analyzer video.mp4 --multilingual --identify-species --annotate-video
```

### Custom Flag Directory
```bash
# Specify custom flag directory
vogel-video-analyzer video.mp4 \
  --flag-dir /path/to/flags/ \
  --multilingual \
  --identify-species \
  --annotate-video
```

### Programmatic Usage
```python
from vogel_video_analyzer.analyzer import render_flag_icon

# Load from file
icon = render_flag_icon('assets/flags/de.png', size=24)

# Load by country code
icon = render_flag_icon('de', size=24, flag_dir='assets/flags/')

# Automatic fallback to pixel rendering
icon = render_flag_icon('🇩🇪', size=24)  # Works even without files
```

---

## 🎨 Flag Rendering Methods

The hybrid system supports **5 input types**:

1. **Emoji String**: `'🇩🇪'` → Pixel rendering (fallback)
2. **File Path**: `'assets/flags/de.png'` → Load PNG/JPG
3. **Country Code**: `'de'` + `flag_dir='assets/flags/'` → Auto-find file
4. **PIL Image**: Pre-loaded Image object → Direct resize
5. **NumPy Array**: OpenCV image array → Convert and resize

**Rendering Priority**: PNG/JPG file → Emoji fallback → Pixel rendering → None

---

## 📋 Requirements

### For Japanese Text Display
```bash
# Install CJK fonts on Debian/Ubuntu/Raspbian
sudo apt-get install fonts-noto-cjk

# On Arch Linux
sudo pacman -S noto-fonts-cjk

# On macOS (included by default)
# On Windows (included by default)
```

### Python Dependencies
No new dependencies! All functionality uses existing libraries:
- PIL/Pillow (already required)
- OpenCV (already required)
- NumPy (already required)

---

## 📁 Included Flag Assets

Located in `assets/flags/`:
- `de.png` - Germany (150x90px, 316 bytes)
- `gb.png` - United Kingdom (150x75px, 871 bytes)
- `jp.png` - Japan (150x100px, 1026 bytes)

**License**: Public Domain (Wikimedia Commons)
- Free to use, modify, and distribute
- No attribution required
- Sources documented in `assets/flags/LICENSE`

---

## 🔧 Technical Details

### New Functions
```python
def render_flag_from_file(flag_path, size=24):
    """Load flag icon from PNG/JPG file"""
    
def render_flag_icon(source, size=24, flag_dir=None):
    """Flexible flag rendering with multiple input types"""
    
def put_unicode_text(..., flag_dir=None):
    """Enhanced with flag_dir parameter"""
    
def annotate_video(..., flag_dir=None):
    """Auto-detects flag directory if not specified"""
```

### Auto-Detection Logic
1. Check if `flag_dir` parameter provided
2. If not, use `module_dir/assets/flags/`
3. Look for country code files: `{code}.png`, `{code}.jpg`, `{code}.jpeg`
4. Fallback to pixel rendering if file not found

### Quality Settings
- **Aspect Ratio**: 3:2 (standard flag ratio)
- **Resampling**: LANCZOS (high quality)
- **Color Mode**: RGB (automatic conversion)

---

## 📚 Documentation

- **Usage Guide**: `docs/FLAG_RENDERING.md`
- **Flag README**: `assets/flags/README.md`
- **License Info**: `assets/flags/LICENSE`
- **Test Suite**: `tests/test_flag_rendering.py`
- **Main README**: Updated with `--flag-dir` examples

---

## 🐛 Bug Fixes

### Japanese Text Not Displaying
**Problem**: シジュウカラ characters missing from annotations  
**Cause**: No CJK fonts installed on system  
**Solution**: Install `fonts-noto-cjk` package  

### PNG Flags Not Loading
**Problem**: Pixel-rendered flags used despite PNG files present  
**Cause**: Emoji strings ('🇩🇪') forced pixel rendering  
**Solution**: Changed to country codes ('de') for automatic PNG loading  

---

## 🔄 Upgrade Notes

### From v0.4.1 to v0.4.2

**No Breaking Changes** - Fully backward compatible!

- Existing code works without modifications
- Pixel rendering still available as fallback
- Optional flag images enhance quality when present
- New `--flag-dir` parameter is optional

### Recommended Actions
1. Install CJK fonts for Japanese text support
2. Test with bundled flags: `--multilingual --annotate-video`
3. Customize flag images if needed via `--flag-dir`

---

## 🙏 Credits

### Flag Images
- **Source**: Wikimedia Commons
- **License**: Public Domain
- **Countries**: Germany, United Kingdom, Japan
- **Quality**: High-resolution PNG (150px width)

### Contributors
- **Development**: kamera-linux team
- **Testing**: Community feedback on flag rendering
- **Documentation**: Comprehensive guides and examples

---

## 📊 Statistics

- **New Functions**: 2 (render_flag_from_file, render_flag_icon)
- **Enhanced Functions**: 2 (put_unicode_text, annotate_video)
- **New CLI Parameters**: 1 (--flag-dir)
- **Documentation Files**: 3 (FLAG_RENDERING.md, flags/README.md, flags/LICENSE)
- **Test Files**: 1 (test_flag_rendering.py)
- **Flag Assets**: 3 PNG files (1.2 KB total)
- **Lines of Code**: ~150 new, ~20 modified
- **Supported Languages**: English, German, Japanese (with proper fonts)

---

## 🚀 Next Steps

### For Users
```bash
# 1. Install CJK fonts (one-time setup)
sudo apt-get install fonts-noto-cjk

# 2. Try the new features
vogel-video-analyzer your_video.mp4 \
  --multilingual \
  --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --annotate-video

# 3. Check the output for high-quality flags and Japanese text!
```

### For Developers
- Explore `docs/FLAG_RENDERING.md` for API details
- Run `tests/test_flag_rendering.py` to test all methods
- Add custom flag images to `assets/flags/` directory
- Use `render_flag_icon()` in your own projects

---

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

---

**Installation**:
```bash
pip install vogel-video-analyzer==0.4.2
```

**Repository**: https://github.com/kamera-linux/vogel-video-analyzer
