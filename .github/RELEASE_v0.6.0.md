# Release v0.6.0 - Safer Deletion, Correct Species Colours & Hailo Overhaul

**Release Date:** 2026-11-06

---

## 🎯 Overview

v0.6.0 is a **quality and safety release** based on a full review of the code base. It makes `--delete-folder` safe, fixes several bugs that produced wrong results (species classification colours, summary videos, bird segments, high-FPS annotation), reworks the Hailo NPU engine and adds a CI test suite (131 tests).

This is a **minor version bump** because of changes that can affect existing setups. Please read [⚠️ Breaking Changes](#️-breaking-changes) before upgrading.

---

## ⚠️ Breaking Changes

- **Python ≥ 3.10 required.** Pillow 12 and current PyTorch no longer support Python 3.8/3.9.
- **Exit code 1 if a video fails.** `vogel-analyze` used to return 0 even when every video failed. Scripts and cron jobs that check the exit code may react differently.
- **`--delete-folder` is stricter.** A folder is only deleted if *every* video in it was analyzed and none contains birds. Folders with other, not analyzed videos are skipped. The current directory (and its parents), the home directory and `/` are never deleted.
- **Unreadable videos are never deleted.** Videos from which no frame could be read used to count as "0% birds".
- **`VideoAnalyzer` default species model** is now `chriamue/bird-species-classifier` (same as the CLI; it used to be `dima806/bird_species_image_detection`).
- **`BirdSpeciesClassifier`** raises `RuntimeError` when the model cannot be loaded. It used to fail silently and return no species.

---

## ✨ What's New

### 🗑️ Safe Deletion
- **`--dry-run`**: shows what `--delete-file` / `--delete-folder` would delete, without deleting anything
- Skipped folders are listed with the reason (mixed content, unreadable video, protected directory, not analyzed videos)

```bash
vogel-analyze --delete-folder --dry-run ~/Videos/*/*.mp4
```

### ⚡ Hailo-8 Engine Overhaul (Raspberry Pi AI HAT+)
- RGB input and letterbox pre-processing (same as ultralytics)
- Support for the HailoRT **NMS-by-class** output format used by Hailo Model Zoo HEFs
- YOLOv8 **DFL** raw-output decoding; split box/class tensors are grouped per stride
- Inference pipeline is opened **once** instead of per frame (much faster)
- `--hailo-num-classes` is now actually used; with `1` the bird class ID is automatically `0`

> These changes are covered by unit tests but still need to be validated on real Hailo hardware. Feedback is welcome.

### 🚀 Performance
- Annotation: fonts and flag icons are cached; text is drawn only in its region instead of converting the whole frame
- Summary video and HTML thumbnails read frames sequentially instead of seeking for every frame

---

## 🐛 Bug Fixes

- **Species identification**: crops were passed to the model in BGR instead of RGB (red and blue swapped)
- **`--create-summary`**: counted *any* detected object (people, cars, …) as bird activity
- **`--create-summary`**: failed with `FileNotFoundError` after a successful run
- **Bird segments**: max. gap is 2 s (was `2 × sample_rate` seconds, e.g. 10 s)
- **Annotated videos > 60 FPS**: were written in slow motion with truncated audio
- **`--log`**: crashed in libraries that call `isatty()`, `encoding` or `fileno()`
- **`python -m vogel_video_analyzer`** always returned exit code 0
- **HTML report**: thumbnails were one frame off; names are now HTML-escaped
- Division by zero for videos without FPS / frame count; `--sample-rate 0` and thresholds outside 0–1 are rejected
- Pixel fallback flag for `gb` was rendered grey
- **GitHub sync**: `/issues/1` matched `/issues/12`; links to other repositories selected the wrong issue; pull requests were imported as issues; project board was limited to 100 items
- **Issue board**: a corrupt storage file was overwritten (now backed up as `*.corrupt-<timestamp>`); writes are atomic
- Language detection respects `LANGUAGE` / `LC_ALL` / `LC_MESSAGES`; deprecated `locale.getdefaultlocale()` removed

---

## 🔒 Security

- HTML report: video and species names are escaped; Chart.js 4.4.0 is **bundled** (no runtime download, works offline)
- GitHub token setup: hidden input (`getpass`), config file created with mode `0600`; warning for `--github-token` on the command line
- Release script no longer uses `shell=True`
- GitHub Actions pinned to commit SHAs; PyPI publishing prepared for **Trusted Publishing (OIDC)**

---

## 🌐 i18n

42 new messages, all translated in **EN, DE, JA** (169 keys per language). Previously hard-coded English messages in the analyzer are now translated.

---

## 📋 Testing

✅ **131 tests** (previously 35), run in CI on Python 3.10–3.13 together with ruff:
- Synthetic videos and a fake YOLO model: segments, summary video, annotation frame rate, deletion rules
- Hailo post-processing without hardware (letterbox, NMS formats, DFL decoding)
- GitHub sync matching, token file permissions, issue board storage, HTML escaping, translations

✅ End-to-end check with the real `yolo26n.pt`: analysis, JSON/HTML report, annotation, summary, `--delete-folder --dry-run`

```bash
pip install -e ".[dev,github,species]" --extra-index-url https://download.pytorch.org/whl/cpu
pytest
```

---

## 📦 Installation

```bash
pip install --upgrade vogel-video-analyzer
```

---

## 🔧 Infrastructure

- New workflow `tests.yml` (ruff + pytest)
- `yolo26n.pt` removed from the repository (downloaded automatically by ultralytics)
- `test_yolov26_upgrade.py` moved to `scripts/check_yolov26_upgrade.py`
- `release_checklist.sh` reads the version from `__init__.py`
- `py.typed` marker added

---

**Full Changelog:** https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.5.12...v0.6.0
