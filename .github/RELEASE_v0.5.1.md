# Release v0.5.1 - Enhanced HTML Report Compatibility 🔧

**Release Date:** December 13, 2025

## 🔧 Bug Fixes & Improvements

### HTML Report Compatibility
This patch release fixes a critical issue where HTML reports didn't display charts correctly in certain environments (e.g., HTMLPreview.github.io, offline viewing).

**What's Fixed:**
- ✅ **Embedded Chart.js**: Chart.js library is now embedded inline instead of loaded from CDN
- ✅ **Offline Support**: HTML reports work without internet connection
- ✅ **HTMLPreview Compatible**: Reports display correctly on https://htmlpreview.github.io
- ✅ **Universal Browser Support**: No external dependencies required

### Technical Details

**Before (v0.5.0):**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```
- ❌ Required internet connection
- ❌ Blocked by some preview services
- ❌ Failed in restricted environments

**After (v0.5.1):**
```html
<script>
/* Chart.js v4.4.0 embedded inline (~200KB) */
!function(t,e){"object"==typeof exports...
</script>
```
- ✅ Works offline
- ✅ No external dependencies
- ✅ Universal compatibility

### File Size Impact
- HTML report file size: +~80KB (377KB → 459KB)
- Still very reasonable for self-contained reports
- Trade-off: Size vs. compatibility (compatibility wins!)

## 📊 Example Report

**[🌐 View Online](https://htmlpreview.github.io/?https://github.com/kamera-linux/vogel-video-analyzer/blob/main/examples/html_report_example.html)**

The example report now displays correctly with:
- Activity Timeline Chart ✅
- Species Distribution Chart ✅
- Thumbnail Gallery ✅
- All interactive features working ✅

## 🚀 Usage

```bash
# Generate HTML report with all features
vogel-analyze --language en --identify-species --species-model kamera-linux/german-bird-classifier --species-threshold 0.80 --html-report report.html --sample-rate 15 --max-thumbnails 12 video.mp4

# Basic HTML report
vogel-analyze --identify-species --html-report report.html video.mp4
```

## 📦 Installation

```bash
pip install --upgrade vogel-video-analyzer
```

## 🔄 Upgrade from v0.5.0

If you're using v0.5.0, simply upgrade and regenerate your HTML reports:

```bash
pip install --upgrade vogel-video-analyzer
vogel-analyze --identify-species --html-report new_report.html video.mp4
```

Old reports from v0.5.0 will still work locally but may not display charts in HTMLPreview. Regenerate them with v0.5.1 for full compatibility.

## 📝 Notes

- No breaking changes
- All v0.5.0 features remain unchanged
- Only improvement: Better compatibility through inline Chart.js
- Recommended for all users generating HTML reports

---

**Full Changelog:** [CHANGELOG.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/CHANGELOG.md)
