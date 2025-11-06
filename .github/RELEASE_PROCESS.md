# Release Process Guide

This document describes the process for creating and publishing a new release of vogel-video-analyzer.

## Pre-Release Checklist

- [ ] All tests pass
- [ ] Documentation is up-to-date
- [ ] CHANGELOG.md is updated with new version
- [ ] Version number updated in `pyproject.toml`
- [ ] All changes committed and pushed to main

## Release Steps

### 1. Update Version Number

Edit `pyproject.toml`:
```toml
[project]
version = "X.Y.Z"
```

### 2. Update CHANGELOG.md

Add a new section following the [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature 1

### Changed
- Changed feature 1

### Fixed
- Bug fix 1
```

Don't forget to add the version link at the bottom:
```markdown
[X.Y.Z]: https://github.com/kamera-linux/vogel-video-analyzer/compare/vX.Y.Z-1...vX.Y.Z
```

### 3. Commit Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to X.Y.Z"
git push origin main
```

### 4. Create Git Tag

```bash
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

### 5. Build Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build
```

This creates:
- `dist/vogel_video_analyzer-X.Y.Z-py3-none-any.whl`
- `dist/vogel-video-analyzer-X.Y.Z.tar.gz`

### 6. Check Package

```bash
# Check package for errors
twine check dist/*

# Optional: Test upload to TestPyPI first
twine upload --repository testpypi dist/*
```

### 7. Upload to PyPI

```bash
twine upload dist/*
```

You'll need PyPI credentials. Consider using API tokens stored in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN
```

### 8. Create GitHub Release

1. Go to: https://github.com/kamera-linux/vogel-video-analyzer/releases/new
2. Select the tag `vX.Y.Z`
3. Title: `Release vX.Y.Z`
4. Copy content from `.github/RELEASE_TEMPLATE.md` and fill in details
5. Or use the prepared release notes from `.github/RELEASE_vX.Y.Z.md`
6. Attach build artifacts (optional)
7. Click "Publish release"

### 9. Verify Release

- [ ] Package appears on PyPI: https://pypi.org/project/vogel-video-analyzer/
- [ ] Installation works: `pip install vogel-video-analyzer==X.Y.Z`
- [ ] GitHub release is published
- [ ] Badges in README.md show correct version

## Version Numbering (Semantic Versioning)

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

Examples:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.0` → `0.2.0`: New feature
- `0.9.0` → `1.0.0`: First stable release or breaking change

## Hotfix Process

For urgent fixes on a released version:

1. Create a branch from the tag: `git checkout -b hotfix/vX.Y.Z vX.Y.Z`
2. Make the fix
3. Update version to X.Y.Z+1
4. Follow steps 2-9 above
5. Merge back to main if needed

## Rollback

If a release has issues:

1. Yank the release on PyPI (doesn't delete, but marks as bad)
2. Create a new patch version with fixes
3. Document the issue in CHANGELOG.md

## Automation (Future)

Consider using GitHub Actions for automated releases:
- Trigger on tag push
- Automatic PyPI upload
- Automatic GitHub release creation
