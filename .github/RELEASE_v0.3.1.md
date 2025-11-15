# 🐦 vogel-video-analyzer v0.3.1

**Release Date:** November 15, 2025

## 🎉 What's New

### ✂️ Summary Video Feature

Create compressed videos by automatically skipping segments without bird activity while preserving perfect audio synchronization!

**Key Features:**
- **Smart Segment Detection** - Analyzes video frame-by-frame to identify bird activity periods
- **Audio Preservation** - Maintains perfect audio sync (no pitch/speed changes)
- **Configurable Thresholds** - Fine-tune compression vs. content preservation
- **Fast Processing** - Uses ffmpeg concat (no re-encoding required)
- **Automatic Path Generation** - Saves as `<original>_summary.mp4`
- **Batch Processing** - Process multiple videos at once

### 🚀 New CLI Parameters

```bash
--create-summary              # Enable summary video creation
--summary-output PATH         # Custom output location (optional)
--skip-empty-seconds FLOAT    # Min duration of bird-free segments to skip (default: 3.0)
--min-activity-duration FLOAT # Min duration of bird activity to keep (default: 2.0)
```

### 📊 Usage Examples

**Basic summary with default settings:**
```bash
vogel-analyze --create-summary video.mp4
# Output: video_summary.mp4
```

**Custom thresholds for more aggressive compression:**
```bash
vogel-analyze --create-summary \
  --skip-empty-seconds 5.0 \
  --min-activity-duration 1.0 \
  video.mp4
```

**Batch process multiple videos:**
```bash
vogel-analyze --create-summary *.mp4
# Creates: video1_summary.mp4, video2_summary.mp4, etc.
```

**Combine with faster processing:**
```bash
vogel-analyze --create-summary \
  --sample-rate 10 \
  video.mp4
```

### 🎯 How It Works

1. Analyzes video frame-by-frame using existing YOLO bird detection
2. Identifies continuous segments with/without bird activity
3. Filters segments based on configurable duration thresholds
4. Concatenates active segments using ffmpeg (with audio)
5. Returns compression statistics

### 📈 Example Output

```
🔍 Analyzing video for bird activity: video.mp4...
   📊 Analyzing 18000 frames at 30.0 FPS...
   ✅ Analysis complete - 1250 frames with birds detected

📊 Bird activity segments identified
   📊 Segments to keep: 8
   ⏱️  Original duration: 0:10:00
   ⏱️  Summary duration: 0:02:45
   📉 Compression: 72.5% shorter

🎬 Creating summary video: video_summary.mp4...
   ✅ Summary video created successfully
   📁 video_summary.mp4
```

## 🌍 Internationalization

Full i18n support added for summary feature:
- 🇬🇧 English
- 🇩🇪 German (Deutsch)
- 🇯🇵 Japanese (日本語)

## 🔧 Technical Details

- Uses **ffmpeg concat demuxer** for efficient video concatenation
- **No re-encoding** required (uses `-c copy` for fast processing)
- Temporary segment files automatically cleaned up
- Compatible with both single and batch video processing
- Configurable thresholds allow fine-tuning results

## 📦 Installation

```bash
# Install/upgrade from PyPI
pip install --upgrade vogel-video-analyzer

# With species identification support
pip install --upgrade vogel-video-analyzer[species]

# Install ffmpeg (required for summary feature)
sudo apt install ffmpeg  # Ubuntu/Debian
```

## 📚 Documentation

- **CHANGELOG:** [CHANGELOG.md](../CHANGELOG.md)
- **README:** [README.md](../README.md)
- **German README:** [README.de.md](../README.de.md)
- **Japanese README:** [README.ja.md](../README.ja.md)

## 🔗 Links

- **PyPI Package:** https://pypi.org/project/vogel-video-analyzer/
- **GitHub Repository:** https://github.com/kamera-linux/vogel-video-analyzer
- **Issues:** https://github.com/kamera-linux/vogel-video-analyzer/issues

## 💡 Use Cases

Perfect for:
- 📹 **Wildlife Monitoring** - Compress hours of footage to minutes of bird activity
- 🔬 **Research** - Focus on relevant segments while preserving complete audio
- 💾 **Storage Optimization** - Reduce file sizes by 50-90% depending on activity
- 🎬 **Content Creation** - Quick highlights of bird visits to your feeder

## 🙏 Acknowledgments

Thank you to all users providing feedback and suggestions for this feature!

---

**Full Changelog:** https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.3.0...v0.3.1
