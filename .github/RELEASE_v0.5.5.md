# Release v0.5.5 - Security Hardening Update

**Release Date:** February 15, 2026

## 🔒 Highlights

This release focuses on **security hardening** and updated security documentation across all README language variants.

## ✅ What's New

### Security Fixes

1. **GitHub GraphQL timeout added**
   - Added explicit request timeout in `github_sync.py`
   - Reduces risk of hanging network calls and improves robustness

2. **Chart.js download validation hardened**
   - Added strict URL validation in `reporter.py`
   - Enforces `https` scheme and allowlisted host (`cdn.jsdelivr.net`)
   - Bandit warning `B310` is now mitigated and documented

3. **Dependency floor updated**
   - Raised minimum `pillow` version to `>=12.1.1`

## 📊 Security Audit Results (2026-02-15)

### Code Security (Bandit)

- **Scan target:** `src/vogel_video_analyzer`
- **Total lines scanned:** 3,561
- **Findings:**
  - High: 0 ✅
  - Medium: 0 ✅
  - Low: 16

### Dependency Security (pip-audit)

- **Result:** No known vulnerabilities found ✅

## 📚 Documentation Updates

Security audit sections added/updated in:

- `README.md` (English)
- `README.de.md` (Deutsch)
- `README.ja.md` (日本語)
- `SECURITY.md`
- `CHANGELOG.md`

## 🧩 Version Updates

- Package version bumped to **0.5.5** in:
  - `src/vogel_video_analyzer/__init__.py`

## 🛠️ Files of Interest

- `src/vogel_video_analyzer/github_sync.py`
- `src/vogel_video_analyzer/reporter.py`
- `pyproject.toml`
- `CHANGELOG.md`
- `README.md`
- `README.de.md`
- `README.ja.md`
- `SECURITY.md`

## 🚀 Upgrade

```bash
pip install --upgrade vogel-video-analyzer
```

Or install this version explicitly:

```bash
pip install vogel-video-analyzer==0.5.5
```

---

**Recommended update:** ✅ Yes (security hardening release)
