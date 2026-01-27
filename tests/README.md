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

## Requirements

```bash
pip install pytest pytest-cov
```

Or use the development dependencies:

```bash
pip install -e ".[dev]"
```
