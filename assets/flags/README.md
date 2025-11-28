# Flag Icons for Multilingual Annotations

This directory contains flag icon images used for multilingual video annotations.

## 📁 Directory Structure

```
assets/flags/
├── de.png          # Germany (Deutschland)
├── gb.png          # United Kingdom (Great Britain)
├── jp.png          # Japan
├── us.png          # United States (optional)
├── fr.png          # France (optional)
└── ...
```

## 🎨 Icon Requirements

- **Format**: PNG (transparent background preferred)
- **Size**: Any size (will be auto-resized)
- **Aspect Ratio**: 3:2 (standard flag ratio)
- **Recommended**: 90x60px or 150x100px minimum

## 📝 Usage

### Method 1: Emoji (Default - No files needed)
```python
# Built-in pixel rendering for DE, GB, JP
icon = render_flag_icon('🇩🇪', size=24)
```

### Method 2: File Path
```python
# Direct path to flag file
icon = render_flag_icon('assets/flags/de.png', size=24)
```

### Method 3: Country Code + Directory
```python
# Auto-detect from directory
icon = render_flag_icon('de', size=24, flag_dir='assets/flags/')
```

### Method 4: PIL Image
```python
# Use existing PIL Image
img = Image.open('custom_flag.png')
icon = render_flag_icon(img, size=24)
```

### Method 5: NumPy Array
```python
# From OpenCV/NumPy array (BGR format)
flag_array = cv2.imread('flag.png')
icon = render_flag_icon(flag_array, size=24)
```

## 🔄 Fallback Behavior

1. If flag file exists → use file
2. If emoji recognized (🇩🇪, 🇬🇧, 🇯🇵) → pixel rendering
3. Otherwise → gray placeholder

## 🌍 Adding New Flags

1. Download flag image (e.g., from [Flagpedia](https://flagpedia.net/))
2. Save as `{country_code}.png` (e.g., `fr.png` for France)
3. Place in `assets/flags/` directory
4. Use with country code:
   ```python
   icon = render_flag_icon('fr', size=24, flag_dir='assets/flags/')
   ```

## 🎯 Recommended Flag Sources

- [Flagpedia](https://flagpedia.net/) - High-quality flag images
- [Flag Icons](https://www.flaticon.com/packs/flags) - Free flag icons
- [Twemoji](https://github.com/twitter/twemoji) - Twitter emoji flags
- [OpenMoji](https://openmoji.org/) - Open-source emoji flags

## 📦 Integration with Video Annotation

The `annotate_video()` method automatically uses this hybrid system:

```python
# In multilingual mode, flags are rendered next to species names
analyzer.annotate_video(
    'video.mp4',
    multilingual=True,
    flag_dir='assets/flags/'  # Optional: use custom flag images
)
```

## 🔧 Technical Details

- **Input formats**: PNG, JPG, JPEG, SVG (if PIL supports)
- **Color space**: RGB (auto-converted from RGBA/grayscale)
- **Resampling**: LANCZOS for high quality
- **Output**: PIL Image (RGB mode)
- **Size**: Auto-scaled maintaining 3:2 aspect ratio

## 📄 License

Flag images should comply with their respective licenses. Most country flags are in the public domain, but verify before commercial use.
