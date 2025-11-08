#!/usr/bin/env python3
"""
Script to organize extracted bird images into train/val split.
Performs 80/20 split with random shuffling.
Works with both old (species_video*/) and new (species/) directory structures.
"""

import os
import shutil
import random
import argparse
from pathlib import Path

# Default configuration
DEFAULT_SOURCE_DIR = Path("/home/imme/vogel-training-data")
TRAIN_RATIO = 0.8

def collect_images_by_species(source_dir):
    """
    Collect all images grouped by species.
    Supports multiple directory structures:
    - New: source_dir/species/*.jpg (direct species folders)
    - Old: source_dir/species_video*/*.jpg (legacy video folders)
    """
    images_by_species = {}
    
    print(f"🔍 Scanning directory: {source_dir}")
    print()
    
    # Find all subdirectories that might contain species images
    for item in source_dir.iterdir():
        if not item.is_dir():
            continue
        
        species_name = None
        images = []
        
        # Check if it's a direct species folder (new format)
        jpg_files = list(item.glob("*.jpg"))
        if jpg_files:
            species_name = item.name
            images = jpg_files
        
        # Also check for old format: species_video* folders
        if not species_name:
            # Extract species name from folder like "kohlmeise_video20241108"
            for potential_species in ["blaumeise", "kleiber", "kohlmeise", "rotkehlchen", "sumpfmeise", 
                                     "amsel", "buchfink", "erlenzeisig", "feldsperling", "gimpel",
                                     "gruenfink", "haussperling", "kernbeisser", "star", "stieglitz"]:
                if item.name.startswith(potential_species):
                    species_name = potential_species
                    images = list(item.glob("*.jpg"))
                    break
        
        if species_name and images:
            if species_name not in images_by_species:
                images_by_species[species_name] = []
            images_by_species[species_name].extend(images)
    
    # Print summary
    for species, imgs in sorted(images_by_species.items()):
        print(f"   {species}: {len(imgs)} Bilder gefunden")
    
    if not images_by_species:
        print("   ⚠️  Keine Bilder gefunden!")
    
    print()
    return images_by_species

def split_and_copy(images_by_species, output_dir, train_ratio=TRAIN_RATIO):
    """Split images 80/20 and copy to train/val folders."""
    stats = {}
    
    for species, images in images_by_species.items():
        if len(images) == 0:
            print(f"⚠️  {species}: Keine Bilder gefunden, überspringe...")
            continue
        
        # Shuffle images randomly
        random.shuffle(images)
        
        # Calculate split point
        split_idx = int(len(images) * train_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Copy to train folder
        train_dir = output_dir / "train" / species
        train_dir.mkdir(parents=True, exist_ok=True)
        for img_path in train_images:
            shutil.copy2(img_path, train_dir / img_path.name)
        
        # Copy to val folder
        val_dir = output_dir / "val" / species
        val_dir.mkdir(parents=True, exist_ok=True)
        for img_path in val_images:
            shutil.copy2(img_path, val_dir / img_path.name)
        
        stats[species] = {
            "total": len(images),
            "train": len(train_images),
            "val": len(val_images)
        }
        
        print(f"✓ {species}: {len(train_images)} train, {len(val_images)} val")
    
    return stats

def print_summary(stats, output_dir):
    """Print summary statistics."""
    print("\n" + "="*50)
    print("Dataset Organisation abgeschlossen")
    print("="*50)
    
    total_train = sum(s["train"] for s in stats.values())
    total_val = sum(s["val"] for s in stats.values())
    total = sum(s["total"] for s in stats.values())
    
    print(f"\nGesamt: {total} Bilder")
    print(f"  Training:   {total_train} ({total_train/total*100:.1f}%)")
    print(f"  Validation: {total_val} ({total_val/total*100:.1f}%)")
    
    print("\nPro Vogelart:")
    for species, s in stats.items():
        print(f"  {species:12s}: {s['total']:3d} gesamt ({s['train']:3d} train, {s['val']:2d} val)")
    
    print(f"\nDataset Ordner: {output_dir}")
    print(f"  Training:   {output_dir}/train/")
    print(f"  Validation: {output_dir}/val/")

def main():
    parser = argparse.ArgumentParser(
        description='Organize bird images into train/val split',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Organize images from default directory
  python organize_dataset.py
  
  # Organize images from custom directory
  python organize_dataset.py --source ~/my-birds/ --output ~/my-dataset/
  
  # Custom train/val split (70/30)
  python organize_dataset.py --train-ratio 0.7
        """
    )
    
    parser.add_argument('--source', '-s', type=Path, default=DEFAULT_SOURCE_DIR,
                       help=f'Source directory with species folders (default: {DEFAULT_SOURCE_DIR})')
    parser.add_argument('--output', '-o', type=Path, default=None,
                       help='Output directory for organized dataset (default: <source>/organized)')
    parser.add_argument('--train-ratio', type=float, default=TRAIN_RATIO,
                       help=f'Train/val split ratio (default: {TRAIN_RATIO})')
    
    args = parser.parse_args()
    
    source_dir = args.source.expanduser()
    output_dir = args.output.expanduser() if args.output else source_dir / "organized"
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return 1
    
    print(f"📂 Source: {source_dir}")
    print(f"📂 Output: {output_dir}")
    print(f"📊 Train/Val Split: {args.train_ratio*100:.0f}% / {(1-args.train_ratio)*100:.0f}%")
    print()
    
    print("🔍 Sammle Bilder nach Vogelart...")
    images_by_species = collect_images_by_species(source_dir)
    
    if not images_by_species:
        print("❌ Keine Bilder gefunden!")
        return 1
    
    print("📋 Splitte und kopiere Bilder...")
    stats = split_and_copy(images_by_species, output_dir, args.train_ratio)
    
    print_summary(stats, output_dir)
    return 0

if __name__ == "__main__":
    exit(main())
