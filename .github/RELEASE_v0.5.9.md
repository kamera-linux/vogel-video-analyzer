# Release v0.5.9: Dynamic Version in HTML Reports

**Release Date:** February 22, 2026

## 🎯 Highlights

This release improves **HTML report generation** by automatically including the current application version in generated reports, ensuring accurate version tracking.

## ✅ What's New

### Enhancement: Dynamic Version Number in HTML Reports

#### Before (v0.5.8):
```html
<p>Generated with vogel-video-analyzer v0.5.0</p>
```
- Version was hardcoded to v0.5.0 in HTML template
- Didn't reflect actual application version
- Misleading when viewing older reports

#### After (v0.5.9):
```html
<p>Generated with vogel-video-analyzer v0.5.9</p>
```
- Version automatically reflects current app version
- `__version__` imported from `__init__.py` and used dynamically
- Reports always show accurate generation version

### Technical Changes

#### Modified Files

1. **`src/vogel_video_analyzer/reporter.py`**
   - Added import: `from . import __version__`
   - Updated HTML template to use: `{t('html_footer')} v{__version__}`
   - Removed hardcoded version string

2. **`examples/html_report_example.html`**
   - Updated example report footer from `v0.5.0` to `v0.5.8`

### Benefits

✅ **Accurate Version Tracking** - HTML reports show the exact version that generated them
✅ **Better Debugging** - Easy to identify which version created a report
✅ **Professional Output** - Consistent versioning across all generated documents
✅ **Future-Proof** - No need to update template for every new release

### 📝 Example Output

When users generate a report with v0.5.9:

```bash
vogel-analyze --html-report report.html video.mp4
```

The generated `report.html` footer will automatically display:
```
Generated with vogel-video-analyzer v0.5.9
```

### Testing

Verify the feature works correctly:

```bash
# Generate HTML report
vogel-analyze --html-report /tmp/test_report.html --sample-rate 10 video.mp4

# Check the footer contains current version
grep "Generated with" /tmp/test_report.html
# Should output: Generated with vogel-video-analyzer v0.5.9
```

### Backward Compatibility

✅ **Fully compatible** - No breaking changes
- Existing reports continue to work as expected
- No database or format changes
- Output quality unchanged

### 🚀 Upgrade

```bash
# Fresh install
pip install vogel-video-analyzer

# Upgrade from v0.5.8 or earlier
pip install --upgrade vogel-video-analyzer
```

Or install explicitly:

```bash
pip install vogel-video-analyzer==0.5.9
```

### 📋 Files Modified Summary

- `src/vogel_video_analyzer/reporter.py` - Dynamic version import and template update
- `examples/html_report_example.html` - Example footer updated

---

**Recommended update:** ✅ Yes (improved reporting accuracy)

**Migration needed:** ❌ No (fully backward compatible)
