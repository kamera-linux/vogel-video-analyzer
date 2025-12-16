# Examples

This directory contains example outputs from vogel-video-analyzer.

## HTML Report Example

**File:** [html_report_example.html](html_report_example.html)

Interactive HTML report demonstrating the visualization features of v0.5.0+:
- Activity timeline chart showing bird detections over time
- Species distribution bar chart
- Thumbnail gallery with best detection screenshots
- Multilingual support (EN/DE/JA)

### Generated with:

```bash
vogel-analyze --language en \
  --identify-species \
  --species-model kamera-linux/german-bird-classifier-v2 \
  --species-threshold 0.80 \
  --html-report report.html \
  --sample-rate 15 \
  --max-thumbnails 12 \
  video.mp4
```

### Features Demonstrated:
- ✅ Species name translation (German model → English display)
- ✅ Interactive Chart.js visualizations
- ✅ Responsive design for all devices
- ✅ Self-contained HTML (no external dependencies)
- ✅ Professional gradient styling
- ✅ Thumbnail gallery with confidence scores

---

**[🌐 View Online](https://htmlpreview.github.io/?https://github.com/kamera-linux/vogel-video-analyzer/blob/main/examples/html_report_example.html)**

**Note:** To view locally, download and open `html_report_example.html` in your web browser.
