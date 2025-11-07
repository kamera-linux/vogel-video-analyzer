#!/usr/bin/env python3
"""
Script to test the trained custom bird classifier on sample images.
"""

import sys
from pathlib import Path
from transformers import pipeline
from PIL import Image

def test_model(model_path: str, image_path: str):
    """Test the model on a single image."""
    
    print(f"Lade Modell: {model_path}")
    classifier = pipeline(
        "image-classification",
        model=model_path,
        device=-1  # CPU
    )
    
    print(f"Klassifiziere Bild: {image_path}")
    img = Image.open(image_path)
    
    results = classifier(img, top_k=5)
    
    print("\nErgebnisse:")
    print("=" * 50)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['label']:15s} - {result['score']:.4f} ({result['score']*100:.1f}%)")
    
    return results

def test_on_validation_set(model_path: str):
    """Test the model on random validation images from each class."""
    import random
    
    val_dir = Path("/home/imme/vogel-training-data/organized/val")
    
    print(f"Lade Modell: {model_path}")
    classifier = pipeline(
        "image-classification",
        model=model_path,
        device=-1  # CPU
    )
    
    species = ["blaumeise", "kleiber", "kohlmeise", "rotkehlchen", "sumpfmeise"]
    
    correct = 0
    total = 0
    
    print("\nTeste auf Validation Set (1 zufälliges Bild pro Klasse):")
    print("=" * 70)
    
    for sp in species:
        species_dir = val_dir / sp
        images = list(species_dir.glob("*.jpg"))
        
        if not images:
            print(f"⚠️  Keine Bilder für {sp} gefunden")
            continue
        
        # Pick random image
        img_path = random.choice(images)
        img = Image.open(img_path)
        
        results = classifier(img, top_k=1)
        predicted = results[0]['label']
        confidence = results[0]['score']
        
        is_correct = predicted == sp
        correct += is_correct
        total += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} {sp:12s} -> {predicted:12s} ({confidence:.4f}) | {img_path.name}")
    
    print("=" * 70)
    print(f"Accuracy: {correct}/{total} = {correct/total*100:.1f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Test single image:")
        print("    python test_model.py <model_path> <image_path>")
        print()
        print("  Test on validation set:")
        print("    python test_model.py <model_path>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    
    if len(sys.argv) == 3:
        image_path = sys.argv[2]
        test_model(model_path, image_path)
    else:
        test_on_validation_set(model_path)
