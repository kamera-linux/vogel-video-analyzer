# Release v0.1.4 - Hotfix: Fix --log Functionality

**Release Date:** 2025-11-07  
**Type:** Hotfix

## 🚨 Critical Fix

This is a **hotfix release** that fixes the `--log` flag which was creating empty log directories but not actually writing any output to log files.

## 🐛 Fixed Issues

### Broken --log Flag
Versions 0.1.0 through 0.1.3 had a bug where the `--log` flag would:
- ✅ Create the log directory structure (`/var/log/vogel-kamera-linux/YYYY/KWXX/`)
- ✅ Print the log file path
- ❌ **NOT** write any content to the log file

The log file would be created as an empty file or not created at all, making the logging feature completely non-functional.

## ✅ What Was Fixed

- **Complete logging implementation**: Output is now properly redirected to log files
- **Tee functionality**: Console output is written to both terminal and log file simultaneously
- **Proper cleanup**: File handles are properly closed even when exceptions occur
- **Stream restoration**: stdout/stderr are correctly restored after logging

## 🔧 Technical Changes

### Before (v0.1.0-v0.1.3)
```python
# Created log file path but never wrote to it
log_file = log_dir / f'{timestamp}_analyze.log'
print(f"📝 Log file: {log_file}\n")
# ❌ No file writing implementation
```

### After (v0.1.4)
```python
# Open log file and redirect output
log_file = open(log_file_path, 'w', encoding='utf-8')

# Tee class writes to both console and file
class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush()

# Redirect stdout/stderr to both console and file
sys.stdout = Tee(original_stdout, log_file)
sys.stderr = Tee(original_stderr, log_file)

# Proper cleanup in finally block
finally:
    if log_file:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        log_file.close()
```

## 🧪 Testing

```bash
# Test logging functionality
vogel-analyze --log video.mp4

# Check that log file was created with content
cat /var/log/vogel-kamera-linux/$(date +%Y)/KW$(date +%V)/*_analyze.log
```

**Expected Result:** Log file contains all console output from the analysis.

## 📦 Migration from v0.1.3

Simply upgrade to get working log functionality:

```bash
pip install --upgrade vogel-video-analyzer
```

**Previous users:** If you used `--log` in v0.1.0-v0.1.3, you'll now get actual log files with content!

## 🔍 Impact

- **Low severity** for most users (optional feature)
- **High severity** for users relying on log files for automation/monitoring
- No breaking changes - purely a bug fix

## 📋 Changelog

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/vogel-video-analyzer/0.1.4/
- **GitHub Repository**: https://github.com/kamera-linux/vogel-video-analyzer
- **Issue Tracker**: https://github.com/kamera-linux/vogel-video-analyzer/issues

---

**Full Changelog**: https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.1.3...v0.1.4
