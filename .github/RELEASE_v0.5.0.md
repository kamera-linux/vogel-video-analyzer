# Release v0.5.0 - Interactive HTML Reports 📊

**Release Date:** December 12, 2025

## 🎉 What's New

### HTML Report Generation
Transform your video analysis results into beautiful, interactive HTML reports!

**Key Features:**
- 📊 **Activity Timeline Chart** - Visualize bird detections over time (10-second intervals)
- 🐦 **Species Distribution Chart** - Bar chart showing top 10 detected species
- 📸 **Thumbnail Gallery** - Best detection screenshots with confidence scores
- 📈 **Statistics Dashboard** - Total detections, unique species, average confidence
- 🎨 **Professional Design** - Gradient styling, responsive layout, hover effects
- 📱 **Mobile Friendly** - Works on desktop and mobile devices
- 💾 **Self-Contained** - Single HTML file with embedded images (no external dependencies)

### Usage

```bash
# Example with all features
vogel-analyze --language en --identify-species --species-model kamera-linux/german-bird-classifier --species-threshold 0.80 --html-report report.html --sample-rate 15 --max-thumbnails 12 video.mp4

# Basic HTML report
vogel-analyze --identify-species --html-report report.html video.mp4

# Custom thumbnail count
vogel-analyze --identify-species --html-report report.html --max-thumbnails 100 video.mp4

# Combined JSON + HTML output
vogel-analyze --identify-species -o data.json --html-report report.html video.mp4
```

**[🔗 View Example Report](https://htmlpreview.github.io/?https://github.com/kamera-linux/vogel-video-analyzer/blob/main/examples/html_report_example.html)**

### Example Report

The generated HTML report includes:

1. **Header Section**
   - Video filename and generation timestamp
   - Professional gradient header design

2. **Statistics Cards**
   - Total Detections
   - Unique Species
   - Average Confidence
   - Frames with Birds

3. **Activity Timeline**
   - Interactive Chart.js line chart
   - 10-second interval grouping
   - Shows detection density over time

4. **Species Distribution**
   - Bar chart of top 10 species
   - Sorted by detection count
   - Color-coded for visual clarity

5. **Thumbnail Gallery**
   - Grid layout with responsive design
   - Species name and confidence score
   - Timestamp and frame number
   - Hover effects for better UX

### Technical Details

**New Module:** `src/vogel_video_analyzer/reporter.py`
- `HTMLReporter` class for report generation
- Chart.js 4.4.0 for data visualization
- Base64 encoding for embedded thumbnails
- Responsive CSS grid layout
- Professional gradient color scheme

**CLI Parameters:**
- `--html-report PATH` - Generate HTML report at specified path
- `--max-thumbnails N` - Limit thumbnail count (default: 50)

**Dependencies:**
- No additional dependencies required
- Uses Chart.js from CDN
- Pure Python HTML generation

### Report Structure

```
report.html
├── CSS Styling (embedded)
├── Header
│   ├── Video name
│   └── Timestamp
├── Statistics Cards
│   ├── Total detections
│   ├── Unique species
│   ├── Average confidence
│   └── Frames with birds
├── Activity Timeline Chart
├── Species Distribution Chart
└── Thumbnail Gallery
    └── Individual thumbnails with metadata
```

### Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers

### Limitations

- Currently supports single video reports only
- Thumbnails require `--identify-species` flag
- Chart.js loaded from CDN (requires internet for first load)

## 📦 Installation

```bash
# Update to v0.5.0
pip install --upgrade vogel-video-analyzer

# Or with species identification
pip install --upgrade vogel-video-analyzer[species]
```

## 🔄 Migration from v0.4.4

No breaking changes! All existing functionality remains unchanged.

New features are opt-in via CLI parameters:
- `--html-report` - Generate HTML reports
- `--max-thumbnails` - Configure thumbnail count

## 📚 Documentation

- [README.md](../README.md) - Full documentation
- [CHANGELOG.md](../CHANGELOG.md) - Complete version history
- [Example Report](https://github.com/kamera-linux/vogel-video-analyzer/examples/report.html) - Sample HTML report

## 🐛 Bug Fixes

No bugs fixed in this release (pure feature addition).

## 🎯 Future Plans (v0.6.0+)

- Multi-video aggregate reports
- Export reports to PDF
- Customizable chart types
- Dark mode theme option
- Video playback integration

## 📝 Full Changelog

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

---

**Enjoy the new HTML reports!** 🎉

For questions or feedback, please open an issue on GitHub.
