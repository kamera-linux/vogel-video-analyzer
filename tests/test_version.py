#!/usr/bin/env python3
"""
Unit tests for version and module imports (pytest compatible)
"""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def test_version_format():
    """Test that version follows semantic versioning format"""
    from vogel_video_analyzer import __version__
    
    # Check format: X.Y.Z
    parts = __version__.split('.')
    assert len(parts) == 3, f"Version should have 3 parts, got {len(parts)}: {__version__}"
    
    # Check each part is numeric
    for i, part in enumerate(parts):
        assert part.isdigit(), f"Version part {i} should be numeric, got: {part}"


def test_module_imports():
    """Test that main exports are available"""
    import vogel_video_analyzer
    
    # Check version attributes
    assert hasattr(vogel_video_analyzer, '__version__')
    assert hasattr(vogel_video_analyzer, '__author__')
    assert hasattr(vogel_video_analyzer, '__license__')
    
    # Check main exports
    assert hasattr(vogel_video_analyzer, 'VideoAnalyzer')
    assert hasattr(vogel_video_analyzer, 'main')


def test_video_analyzer_class():
    """Test that VideoAnalyzer class can be instantiated"""
    from vogel_video_analyzer import VideoAnalyzer
    
    # Check class exists and has expected methods
    assert callable(VideoAnalyzer), "VideoAnalyzer should be a class"
    
    # Check for key methods
    expected_methods = ['analyze_video', 'print_report', 'annotate_video']
    for method in expected_methods:
        assert hasattr(VideoAnalyzer, method), f"VideoAnalyzer should have method: {method}"


def test_cli_main():
    """Test that CLI main function exists"""
    from vogel_video_analyzer import main
    
    assert callable(main), "main should be callable"


def test_constants_exist():
    """Test that module constants are properly defined"""
    from vogel_video_analyzer.analyzer import (
        COCO_CLASS_BIRD,
        DEFAULT_DETECTION_THRESHOLD,
        DEFAULT_SPECIES_THRESHOLD,
        DEFAULT_SAMPLE_RATE,
        DEFAULT_FLAG_SIZE,
        DEFAULT_FONT_SIZE
    )
    
    # Verify constants have expected values
    assert COCO_CLASS_BIRD == 14, "COCO bird class should be 14"
    assert DEFAULT_DETECTION_THRESHOLD == 0.3, "Default detection threshold should be 0.3"
    assert DEFAULT_SPECIES_THRESHOLD == 0.3, "Default species threshold should be 0.3"
    assert DEFAULT_SAMPLE_RATE == 5, "Default sample rate should be 5"
    assert DEFAULT_FLAG_SIZE == 24, "Default flag size should be 24"
    assert DEFAULT_FONT_SIZE == 20, "Default font size should be 20"


if __name__ == '__main__':
    # Allow running as standalone script for backward compatibility
    print("🧪 Testing vogel-video-analyzer module\n")
    print("=" * 60)
    
    try:
        test_version_format()
        test_module_imports()
        test_video_analyzer_class()
        test_cli_main()
        test_constants_exist()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
