#!/usr/bin/env python3
"""
Test script to verify YOLOv26 upgrade
Tests model loading, configuration, and basic functionality
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all imports work"""
    print("✅ Testing imports...")
    try:
        from ultralytics import YOLO
        print("  ✓ Ultralytics YOLO imported")
    except ImportError as e:
        print(f"  ✗ Failed to import YOLO: {e}")
        return False
    
    try:
        from vogel_video_analyzer import VideoAnalyzer, __version__
        print(f"  ✓ VideoAnalyzer imported (v{__version__})")
    except ImportError as e:
        print(f"  ✗ Failed to import VideoAnalyzer: {e}")
        return False
    
    return True

def test_model_loading():
    """Test YOLOv26 model loading"""
    print("\n✅ Testing YOLOv26 model loading...")
    try:
        from ultralytics import YOLO
        print("  Downloading yolo26n.pt (5.3 MB)...")
        model = YOLO("yolo26n.pt")
        print("  ✓ YOLOv26n model loaded successfully")
        
        # Check model info
        print(f"  ✓ Model type: {type(model).__name__}")
        print(f"  ✓ Model device: {model.device}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to load YOLOv26 model: {e}")
        return False

def test_analyzer_config():
    """Test VideoAnalyzer configuration"""
    print("\n✅ Testing VideoAnalyzer configuration...")
    try:
        from vogel_video_analyzer import VideoAnalyzer
        
        # Check default config
        analyzer = VideoAnalyzer(model_path="yolo26n.pt", threshold=0.3)
        print(f"  ✓ VideoAnalyzer initialized with yolo26n.pt")
        print(f"  ✓ Threshold: {analyzer.threshold}")
        print(f"  ✓ Target class: {analyzer.target_class} (bird)")
        
        # Check model is loaded
        if analyzer.model is not None:
            print(f"  ✓ Model loaded: {type(analyzer.model).__name__}")
            return True
        else:
            print("  ✗ Model not loaded")
            return False
    except Exception as e:
        print(f"  ✗ Failed to configure analyzer: {e}")
        return False

def test_cli_module():
    """Test CLI module"""
    print("\n✅ Testing CLI module...")
    try:
        from vogel_video_analyzer import cli
        print("  ✓ CLI module imported")
        
        # Check for main function
        if hasattr(cli, 'main'):
            print("  ✓ CLI main() function found")
            return True
        else:
            print("  ✗ CLI main() function not found")
            return False
    except ImportError as e:
        print(f"  ✗ Failed to import CLI: {e}")
        return False

def test_version():
    """Test version string"""
    print("\n✅ Testing version...")
    try:
        from vogel_video_analyzer import __version__
        print(f"  ✓ Version: {__version__}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to get version: {e}")
        return False

def check_documentation():
    """Verify documentation updates"""
    print("\n✅ Checking documentation...")
    checks = [
        ("README.md", "YOLOv26-based"),
        ("README.de.md", "YOLOv26-basiert"),
        ("README.ja.md", "YOLOv26"),
    ]
    
    all_ok = True
    for filename, search_text in checks:
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            content = filepath.read_text()
            if "yolo26n.pt" in content or search_text in content:
                print(f"  ✓ {filename} updated to YOLOv26")
            else:
                print(f"  ✗ {filename} not updated")
                all_ok = False
        else:
            print(f"  ⚠ {filename} not found")
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 60)
    print("🤖 YOLOv26 Upgrade Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Model Loading", test_model_loading),
        ("Analyzer Configuration", test_analyzer_config),
        ("CLI Module", test_cli_module),
        ("Version", test_version),
        ("Documentation", check_documentation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! YOLOv26 upgrade successful!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
