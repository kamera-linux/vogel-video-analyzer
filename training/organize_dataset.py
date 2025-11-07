#!/usr/bin/env python3
"""
Script to organize extracted bird images into train/val split.
Performs 80/20 split with random shuffling.
"""

import os
import shutil
import random
from pathlib import Path

# Configuration
SOURCE_DIR = Path("/home/imme/vogel-training-data")
OUTPUT_DIR = SOURCE_DIR / "organized"
TRAIN_RATIO = 0.8

# Species mapping from folder names to class names
SPECIES_MAPPING = {
    "blaumeise": "blaumeise",
    "kleiber": "kleiber", 
    "kohlmeise": "kohlmeise",
    "rotkehlchen": "rotkehlchen",
    "sumpfmeise": "sumpfmeise"
}

def collect_images_by_species():
    """Collect all images grouped by species."""
    images_by_species = {}
    
    for species in SPECIES_MAPPING.keys():
        images = []
        # Find all folders matching this species
        for folder in SOURCE_DIR.glob(f"{species}_video*"):
            if folder.is_dir():
                images.extend(list(folder.glob("*.jpg")))
        
        images_by_species[species] = images
        print(f"{species}: {len(images)} Bilder gefunden")
    
    return images_by_species

def split_and_copy(images_by_species):
    """Split images 80/20 and copy to train/val folders."""
    stats = {}
    
    for species, images in images_by_species.items():
        if len(images) == 0:
            print(f"⚠️  {species}: Keine Bilder gefunden, überspringe...")
            continue
        
        # Shuffle images randomly
        random.shuffle(images)
        
        # Calculate split point
        split_idx = int(len(images) * TRAIN_RATIO)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Copy to train folder
        train_dir = OUTPUT_DIR / "train" / species
        train_dir.mkdir(parents=True, exist_ok=True)
        for img_path in train_images:
            shutil.copy2(img_path, train_dir / img_path.name)
        
        # Copy to val folder
        val_dir = OUTPUT_DIR / "val" / species
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

def print_summary(stats):
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
    
    print(f"\nDataset Ordner: {OUTPUT_DIR}")

if __name__ == "__main__":
    print("Sammle Bilder nach Vogelart...")
    images_by_species = collect_images_by_species()
    
    print("\nSplitte und kopiere Bilder...")
    stats = split_and_copy(images_by_species)
    
    print_summary(stats)
