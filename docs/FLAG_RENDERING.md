# Hybrid Flag Rendering System (v0.4.2+)

## 🎨 Overview

The hybrid flag rendering system provides flexible support for displaying country flags in video annotations. It combines built-in pixel rendering with external image file support.

## 🚀 Features

### Built-in Support (No files needed)
- 🇩🇪 Germany - Pixel-rendered (Black/Red/Gold stripes)
- 🇬🇧 United Kingdom - Pixel-rendered (Union Jack)
- 🇯🇵 Japan - Pixel-rendered (Red circle on white)

### External Image Support
- PNG, JPG, JPEG files
- Any country/region flag
- Custom flag designs
- High-quality rendering

## 📝 Usage

### Method 1: Emoji (Default)
```python
from vogel_video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer()
analyzer.annotate_video(
    'video.mp4',
    'output.mp4',
    multilingual=True  # Uses built-in pixel flags
)
```

### Method 2: Custom Flag Directory
```bash
# CLI with custom flags
vogel-analyze --identify-species \
  --annotate-video \
  --multilingual \
  --flag-dir assets/flags/ \
  video.mp4
```

```python
# Python API
analyzer.annotate_video(
    'video.mp4',
    'output.mp4',
    multilingual=True,
    flag_dir='assets/flags/'  # Use PNG/JPG files
)
```

### Method 3: Programmatic Rendering
```python
from vogel_video_analyzer.analyzer import render_flag_icon

# Emoji
icon = render_flag_icon('🇩🇪', size=24)

# File path
icon = render_flag_icon('assets/flags/de.png', size=24)

# Country code + directory
icon = render_flag_icon('de', size=24, flag_dir='assets/flags/')

# PIL Image
from PIL import Image
img = Image.open('flag.png')
icon = render_flag_icon(img, size=24)

# NumPy array (BGR format from OpenCV)
import cv2
array = cv2.imread('flag.png')
icon = render_flag_icon(array, size=24)
```

## 📁 Flag Directory Structure

```
assets/flags/
├── de.png          # Germany
├── gb.png          # United Kingdom (Great Britain)
├── jp.png          # Japan
├── us.png          # United States (optional)
├── fr.png          # France (optional)
└── ...
```

**Requirements:**
- Format: PNG, JPG, or JPEG
- Recommended size: 90x60px or larger
- Aspect ratio: 3:2 (standard flag ratio)
- Transparent background preferred

## 🔄 Fallback Behavior

The system follows this priority order:

1. **Custom flag file** (if `flag_dir` provided and file exists)
2. **Built-in pixel rendering** (for 🇩🇪 🇬🇧 🇯🇵)
3. **Gray placeholder** (if no match found)

Example:
```python
# With flag directory
render_flag_icon('de', flag_dir='assets/flags/')
# → Tries: assets/flags/de.png, de.jpg, de.jpeg
# → Falls back to: 🇩🇪 pixel rendering
# → Last resort: Gray square

# Without flag directory
render_flag_icon('de')
# → Not recognized as emoji
# → Returns: None (no rendering)

render_flag_icon('🇩🇪')
# → Built-in pixel rendering
# → Always works (no files needed)
```

## 🎯 CLI Examples

### Basic (Built-in flags)
```bash
vogel-analyze --identify-species \
  --annotate-video \
  --multilingual \
  video.mp4
```

### Custom flags from directory
```bash
vogel-analyze --identify-species \
  --annotate-video \
  --multilingual \
  --flag-dir /path/to/flags/ \
  video.mp4
```

### Custom flags with species model
```bash
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --annotate-video \
  --multilingual \
  --flag-dir assets/flags/ \
  video.mp4
```

## 🧪 Testing

Run the test script to verify all rendering methods:

```bash
python tests/test_flag_rendering.py
```

Output shows:
- ✅ Successfully rendered flags
- ⚠️  Fallback cases
- ❌ Errors (with details)

## 📦 Adding New Flags

1. **Download flag image:**
   - [Flagpedia](https://flagpedia.net/) - High quality
   - [Twemoji](https://github.com/twitter/twemoji) - Twitter style
   - [OpenMoji](https://openmoji.org/) - Open source

2. **Prepare image:**
   ```bash
   # Resize to 90x60px (3:2 ratio)
   convert input.png -resize 90x60 de.png
   
   # Or with ImageMagick
   magick convert input.png -resize 90x60 de.png
   ```

3. **Place in flag directory:**
   ```bash
   cp de.png assets/flags/
   ```

4. **Use with country code:**
   ```python
   render_flag_icon('de', flag_dir='assets/flags/')
   ```

## 🔧 Advanced Usage

### Custom Flag Mapping

```python
# Create mapping for non-standard codes
flag_map = {
    'germany': 'assets/flags/de.png',
    'britain': 'assets/flags/gb.png',
    'japan': 'assets/flags/jp.png',
}

# Use in rendering
for code, path in flag_map.items():
    icon = render_flag_icon(path, size=24)
```

### Dynamic Flag Selection

```python
def get_flag_for_language(lang_code):
    """Map language code to flag"""
    mapping = {
        'de': '🇩🇪',
        'en': '🇬🇧',
        'ja': '🇯🇵',
        'en-US': '🇺🇸',
        'fr': '🇫🇷',
    }
    return render_flag_icon(mapping.get(lang_code, '🏴'))
```

### Batch Processing

```python
# Process multiple videos with custom flags
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
flag_dir = 'assets/flags/'

for video in videos:
    output = video.replace('.mp4', '_annotated.mp4')
    analyzer.annotate_video(
        video,
        output,
        multilingual=True,
        flag_dir=flag_dir
    )
```

## 🐛 Troubleshooting

### PIL Not Available
```
WARNING: PIL not available, using cv2.putText fallback
```
**Solution:** Install Pillow
```bash
pip install Pillow
```

### Flag File Not Found
```
⚠️  Flag directory not found: assets/flags/
```
**Solution:** Create directory and add flag files
```bash
mkdir -p assets/flags
# Download flags or use built-in pixel rendering
```

### Poor Quality Flags
**Solution:** Use higher resolution source images
```bash
# Recommended minimum: 90x60px
# Better: 150x100px or larger
```

## 📊 Performance

| Method | Speed | Quality | Files Needed |
|--------|-------|---------|--------------|
| Pixel rendering | ⚡⚡⚡ Fast | Good | None |
| PNG files | ⚡⚡ Medium | Excellent | Required |
| Large PNG | ⚡ Slower | Best | Required |

**Recommendation:** Use pixel rendering for real-time processing, PNG files for highest quality.

## 🔒 License

Flag images should comply with their respective licenses. Most country flags are public domain, but verify before commercial use.
