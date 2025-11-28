#!/usr/bin/env python3
"""
Test script for hybrid flag rendering system

Demonstrates all supported input methods:
1. Emoji rendering (pixel-based)
2. File path (direct)
3. Country code + directory
4. PIL Image object
5. NumPy array
"""

import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from vogel_video_analyzer.analyzer import render_flag_icon
import numpy as np
from PIL import Image
import cv2

def test_flag_rendering():
    """Test all flag rendering methods"""
    
    print("🧪 Testing Hybrid Flag Rendering System\n")
    print("=" * 60)
    
    # Test 1: Emoji rendering (built-in)
    print("\n1️⃣  Emoji Rendering (Pixel-based)")
    print("-" * 60)
    for emoji in ['🇩🇪', '🇬🇧', '🇯🇵']:
        icon = render_flag_icon(emoji, size=24)
        if icon:
            print(f"   ✅ {emoji} -> {icon.size[0]}x{icon.size[1]}px PIL Image")
        else:
            print(f"   ❌ {emoji} -> Failed")
    
    # Test 2: File path (if exists)
    print("\n2️⃣  File Path Rendering")
    print("-" * 60)
    flag_dir = Path(__file__).parent.parent / 'assets' / 'flags'
    if flag_dir.exists():
        for flag_file in flag_dir.glob('*.png'):
            icon = render_flag_icon(str(flag_file), size=24)
            if icon:
                print(f"   ✅ {flag_file.name} -> {icon.size[0]}x{icon.size[1]}px")
            else:
                print(f"   ❌ {flag_file.name} -> Failed")
    else:
        print(f"   ⚠️  Flag directory not found: {flag_dir}")
        print(f"   💡 Create directory and add PNG files to test")
    
    # Test 3: Country code + directory
    print("\n3️⃣  Country Code + Directory")
    print("-" * 60)
    if flag_dir.exists():
        for code in ['de', 'gb', 'jp', 'us', 'fr']:
            icon = render_flag_icon(code, size=24, flag_dir=str(flag_dir))
            if icon:
                print(f"   ✅ '{code}' -> {icon.size[0]}x{icon.size[1]}px")
            else:
                print(f"   ⚠️  '{code}' -> Not found (fallback to emoji or gray)")
    else:
        print(f"   ⚠️  Skipping (no flag directory)")
    
    # Test 4: PIL Image
    print("\n4️⃣  PIL Image Object")
    print("-" * 60)
    try:
        # Create test image (red square)
        test_img = Image.new('RGB', (60, 40), color=(255, 0, 0))
        icon = render_flag_icon(test_img, size=24)
        if icon:
            print(f"   ✅ PIL Image (60x40) -> {icon.size[0]}x{icon.size[1]}px (resized)")
        else:
            print(f"   ❌ PIL Image -> Failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: NumPy Array
    print("\n5️⃣  NumPy Array (BGR format)")
    print("-" * 60)
    try:
        # Create test array (blue square in BGR)
        test_array = np.zeros((40, 60, 3), dtype=np.uint8)
        test_array[:, :] = (255, 0, 0)  # BGR: Blue
        icon = render_flag_icon(test_array, size=24)
        if icon:
            print(f"   ✅ NumPy (40x60x3) -> {icon.size[0]}x{icon.size[1]}px (resized)")
        else:
            print(f"   ❌ NumPy Array -> Failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Fallback behavior
    print("\n6️⃣  Fallback Behavior")
    print("-" * 60)
    invalid_inputs = [
        ('nonexistent.png', 'Invalid file path'),
        ('xyz', 'Unknown country code'),
        (None, 'None value'),
    ]
    for test_input, description in invalid_inputs:
        icon = render_flag_icon(test_input, size=24)
        if icon:
            print(f"   ⚠️  {description} -> Got icon (unexpected)")
        else:
            print(f"   ✅ {description} -> None (expected)")
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!\n")
    
    # Usage examples
    print("📖 Usage Examples:")
    print("-" * 60)
    print("""
    # Method 1: Emoji (built-in pixel rendering)
    icon = render_flag_icon('🇩🇪', size=24)
    
    # Method 2: Direct file path
    icon = render_flag_icon('assets/flags/de.png', size=24)
    
    # Method 3: Country code + directory
    icon = render_flag_icon('de', size=24, flag_dir='assets/flags/')
    
    # Method 4: PIL Image
    img = Image.open('my_flag.png')
    icon = render_flag_icon(img, size=24)
    
    # Method 5: NumPy array (BGR)
    array = cv2.imread('flag.png')
    icon = render_flag_icon(array, size=24)
    """)


if __name__ == '__main__':
    test_flag_rendering()
