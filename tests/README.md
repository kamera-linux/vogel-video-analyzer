# Tests

This directory contains test files for vogel-video-analyzer.

## Running Tests

### Using pytest (recommended)

```bash
# Run all tests with coverage
pytest tests/ -v

# Run specific test file
pytest tests/test_version.py -v

# Run without coverage
pytest tests/ -v --no-cov
```

### Using standalone scripts

```bash
# Version and module tests
python tests/test_version.py

# Flag rendering tests
python tests/test_flag_rendering.py
```

## Test Files

### test_version.py
Tests for module version, imports, and constants:
- `test_version_format()` - Validates semantic versioning format
- `test_module_imports()` - Checks module exports
- `test_video_analyzer_class()` - Verifies class structure
- `test_cli_main()` - Confirms CLI entry point
- `test_constants_exist()` - Validates module constants

### test_flag_rendering.py
Tests for flag rendering system:
- Emoji rendering (🇩🇪 🇬🇧 🇯🇵)
- File path rendering
- Country code + directory
- PIL Image objects
- NumPy arrays

### conftest.py
Shared fixtures: synthetic MP4 videos (`write_video`) and a `FakeModel` that
mimics ultralytics YOLO, so the pipeline runs without downloading model weights.

### test_analyzer.py
Bird segments, summary segments/video, annotation frame rate, `put_unicode_text`,
font caching, flag fallback, Hailo parameter wiring.

### test_cli.py
Argument validation, `Tee` logging, exit codes, and the safety rules of
`--delete-file` / `--delete-folder` / `--dry-run`.

### test_species_classifier.py
BGR → RGB conversion of crops, load errors, translation tables.

### test_hailo_engine.py
Letterbox, output format detection, NMS / raw (DFL) decoding – no hardware needed.

### test_github_sync.py / test_github_sync_matching.py
Token loading, label mapping, exact issue matching, PR filtering, token file permissions.

### test_issue_board.py / test_issue_board_storage.py
Issue CRUD, corrupt-file backup, atomic writes.

### test_reporter_i18n.py
HTML escaping, bundled Chart.js, thumbnails, translation completeness, language detection.

## Requirements

```bash
pip install pytest pytest-cov
```

Or use the development dependencies:

```bash
pip install -e ".[dev,github,species]" --extra-index-url https://download.pytorch.org/whl/cpu
```

Optional: `ffmpeg` in `PATH` enables the summary-video end-to-end test.
