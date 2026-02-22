# Release v0.5.8: Critical Dependency Fix for YOLOv26 Support

## 🔧 Bug Fix: Ultralytics Dependency Constraint

This release fixes a critical dependency issue where the v0.5.7 release could not automatically download YOLOv26 models due to incompatible ultralytics version constraints.

### ⚡ What Was Fixed

- **Issue**: v0.5.7 introduced YOLOv26 support but specified `ultralytics>=8.0.0`
- **Problem**: YOLOv26 requires `ultralytics>=8.4.14` to function correctly
- **Result**: Users with older ultralytics versions got `FileNotFoundError: [Errno 2] No such file or directory: 'yolo26n.pt'`
- **Solution**: Updated pyproject.toml to require `ultralytics>=8.4.14`

### 📝 What's Changed

#### Dependency Update
- Changed `ultralytics>=8.0.0` → **`ultralytics>=8.4.14`**
- Ensures automatic download of YOLOv26 models works for all new installations
- Backward compatible with existing code

#### Why This Matters

When users install vogel-video-analyzer 0.5.7+ without explicitly upgrading ultralytics:
- **Before (v0.5.7)**: Could install ultralytics 8.3.x → Model auto-download fails ❌
- **After (v0.5.8)**: pip automatically installs ultralytics 8.4.14+ → Model auto-download works ✅

### 🚀 Benefits

- ✅ **Zero-Friction Setup**: First-time users don't need manual ultralytics upgrades
- ✅ **Automatic Model Download**: yolo26n.pt downloads and caches on first use
- ✅ **Better Error Messages**: Clear diagnostics if something still goes wrong
- ✅ **Production Ready**: Reliable for CI/CD pipelines and Docker containers

### Installation & Upgrade

```bash
# Fresh install (gets ultralytics 8.4.14+ automatically)
pip install vogel-video-analyzer

# Upgrade from v0.5.7 or earlier
pip install --upgrade vogel-video-analyzer

# From source
git clone https://github.com/kamera-linux/vogel-video-analyzer.git
cd vogel-video-analyzer
pip install -e .
```

### Quick Test

After upgrade, YOLOv26 should work automatically:

```bash
# Works immediately - no manual setup needed
vogel-analyze video.mp4

# With species identification
vogel-analyze --identify-species video.mp4
```

### Verify You Have the Fix

```bash
pip show ultralytics | grep Version
# Output should be: Version: 8.4.14 or higher
```

### Known Issues (Now Fixed)

#### Error in v0.5.7:
```
❌ error_loading_model: [Errno 2] No such file or directory: 'yolo26n.pt'
```

#### Solution in v0.5.8:
Simply upgrade:
```bash
pip install --upgrade vogel-video-analyzer
```

The dependency constraint now ensures you get the right ultralytics version.

### Technical Details

#### Dependency Chain

```
vogel-video-analyzer 0.5.8
  └── ultralytics>=8.4.14
      ├── torch>=2.0.0
      ├── opencv-python>=4.6.0
      └── numpy>=1.24.0
```

#### Model Auto-Download Flow

1. User runs `vogel-analyze video.mp4`
2. VideoAnalyzer searches for `yolo26n.pt` locally
3. If not found, YOLO()'s auto-download triggers
4. **ultralytics 8.4.14+** has full YOLOv26 support
5. Model downloads from GitHub releases (~50MB)
6. Model cached in `~/.cache/yolo/` for future runs

#### Why This Is Important

- **v0.5.6**: YOLOv8 → YOLOv26 upgrade (performance)
- **v0.5.7**: Auto-download support (convenience)
- **v0.5.8**: Dependency fix (reliability) ← **You are here**

### Troubleshooting

#### Still Getting FileNotFoundError?

Verify upgraded ultralytics:
```bash
pip install --upgrade 'ultralytics>=8.4.14'
vogel-analyze --version  # Should show v0.5.8+
```

#### Check Your Installation
```bash
python -c "from ultralytics import YOLO; print(YOLO('yolo26n.pt'))"
# Should show model loading without errors
```

#### Still Issues?

Check:
1. Internet connection (for model download)
2. Disk space: `df -h` (need ~50MB)
3. Cache permissions: `ls -la ~/.cache/yolo/` (should be writable)

### Impact

| Scenario | v0.5.7 | v0.5.8 |
|----------|--------|--------|
| Fresh pip install | ❌ May fail | ✅ Works |
| Docker container | ❌ May fail | ✅ Works |
| CI/CD pipeline | ❌ May fail | ✅ Works |
| Manual upgrade | ✅ Works | ✅ Works |
| Existing venv | ⚠️ Depends | ✅ Works |

### Changelog

Full changelog: [`v0.5.7...v0.5.8`](https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.5.7...v0.5.8)

### Support

For issues or questions:
- 📘 [Documentation](https://github.com/kamera-linux/vogel-video-analyzer)
- 🐛 [Report Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- 💬 [Discussions](https://github.com/kamera-linux/vogel-video-analyzer/discussions)

---

**Recommendation**: All users should upgrade to v0.5.8 for reliable YOLOv26 support.
