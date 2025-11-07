#!/usr/bin/env python3
"""
Training script for custom bird species classifier.
Fine-tunes an EfficientNet model on the extracted bird images.
"""

import os
import torch
from pathlib import Path
from datetime import datetime
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from datasets import load_dataset
from torchvision.transforms import (
    Compose,
    RandomResizedCrop,
    RandomHorizontalFlip,
    ColorJitter,
    ToTensor,
    Normalize,
    Resize,
    CenterCrop
)
import numpy as np
from PIL import Image
import json

# Configuration
DATA_DIR = Path("/home/imme/vogel-training-data/organized")
OUTPUT_DIR = Path("/home/imme/vogel-models")
MODEL_NAME = "google/efficientnet-b0"  # Base model for fine-tuning
BATCH_SIZE = 16
NUM_EPOCHS = 50
LEARNING_RATE = 2e-4
IMAGE_SIZE = 224

# Species labels (must match folder names)
SPECIES = ["blaumeise", "kleiber", "kohlmeise", "rotkehlchen", "sumpfmeise"]
id2label = {i: species for i, species in enumerate(SPECIES)}
label2id = {species: i for i, species in enumerate(SPECIES)}

def prepare_model_and_processor():
    """Load base model and processor."""
    print(f"Lade Basis-Modell: {MODEL_NAME}")
    
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(SPECIES),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True
    )
    
    return model, processor

def get_transforms(processor, is_training=True):
    """Create image transforms for data augmentation."""
    if is_training:
        return Compose([
            RandomResizedCrop(IMAGE_SIZE, scale=(0.8, 1.0)),
            RandomHorizontalFlip(p=0.5),
            ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            ToTensor(),
            Normalize(mean=processor.image_mean, std=processor.image_std)
        ])
    else:
        return Compose([
            Resize(IMAGE_SIZE + 32),
            CenterCrop(IMAGE_SIZE),
            ToTensor(),
            Normalize(mean=processor.image_mean, std=processor.image_std)
        ])

def transform_function(examples, processor, is_training=True):
    """Transform function for dataset mapping."""
    transforms = get_transforms(processor, is_training)
    
    images = [transforms(img.convert("RGB")) for img in examples["image"]]
    examples["pixel_values"] = images
    
    return examples

def compute_metrics(eval_pred):
    """Compute accuracy metrics."""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    accuracy = (predictions == labels).mean()
    
    # Per-class accuracy
    per_class_acc = {}
    for i, species in id2label.items():
        mask = labels == i
        if mask.sum() > 0:
            per_class_acc[species] = (predictions[mask] == labels[mask]).mean()
    
    return {
        "accuracy": accuracy,
        **{f"acc_{species}": acc for species, acc in per_class_acc.items()}
    }

def collate_fn(examples):
    """Custom collate function for DataLoader."""
    pixel_values = torch.stack([example["pixel_values"] for example in examples])
    labels = torch.tensor([example["label"] for example in examples])
    return {"pixel_values": pixel_values, "labels": labels}

def main():
    """Main training function."""
    print("="*60)
    print("Vogel-Artenerkennung Training")
    print("="*60)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUT_DIR / f"bird-classifier-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nOutput Ordner: {output_dir}")
    print(f"Vogelarten: {', '.join(SPECIES)}")
    print(f"Anzahl Klassen: {len(SPECIES)}")
    
    # Load dataset
    print("\nLade Dataset...")
    dataset = load_dataset("imagefolder", data_dir=str(DATA_DIR))
    
    print(f"  Training:   {len(dataset['train'])} Bilder")
    print(f"  Validation: {len(dataset['validation'])} Bilder")
    
    # Prepare model and processor
    model, processor = prepare_model_and_processor()
    
    # Apply transforms
    print("\nAppliziere Transformationen...")
    dataset["train"] = dataset["train"].map(
        lambda x: transform_function(x, processor, is_training=True),
        batched=True,
        remove_columns=["image"]
    )
    dataset["validation"] = dataset["validation"].map(
        lambda x: transform_function(x, processor, is_training=False),
        batched=True,
        remove_columns=["image"]
    )
    
    # Set format
    dataset["train"].set_format(type="torch", columns=["pixel_values", "label"])
    dataset["validation"].set_format(type="torch", columns=["pixel_values", "label"])
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        warmup_ratio=0.1,
        logging_dir=str(output_dir / "logs"),
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        push_to_hub=False,
        remove_unused_columns=False,
        dataloader_num_workers=4,
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        compute_metrics=compute_metrics,
        data_collator=collate_fn,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=5)]
    )
    
    # Train
    print("\n" + "="*60)
    print("Starte Training...")
    print("="*60)
    
    train_result = trainer.train()
    
    # Save final model
    print("\nSpeichere finales Modell...")
    trainer.save_model(str(output_dir / "final"))
    processor.save_pretrained(str(output_dir / "final"))
    
    # Save training stats
    with open(output_dir / "training_stats.json", "w") as f:
        json.dump({
            "train_runtime": train_result.metrics["train_runtime"],
            "train_samples_per_second": train_result.metrics["train_samples_per_second"],
            "train_loss": train_result.metrics["train_loss"],
            "species": SPECIES,
            "num_train_samples": len(dataset["train"]),
            "num_val_samples": len(dataset["validation"]),
        }, f, indent=2)
    
    # Final evaluation
    print("\n" + "="*60)
    print("Finale Evaluation")
    print("="*60)
    
    eval_results = trainer.evaluate()
    
    print(f"\nValidation Accuracy: {eval_results['eval_accuracy']:.4f}")
    print("\nPro-Vogelart Accuracy:")
    for species in SPECIES:
        key = f"eval_acc_{species}"
        if key in eval_results:
            print(f"  {species:12s}: {eval_results[key]:.4f}")
    
    # Save evaluation results
    with open(output_dir / "eval_results.json", "w") as f:
        json.dump(eval_results, f, indent=2)
    
    print("\n" + "="*60)
    print("Training abgeschlossen!")
    print("="*60)
    print(f"\nModell gespeichert in: {output_dir / 'final'}")
    print(f"\nUm das Modell zu nutzen:")
    print(f"  vogel-video-analyzer --species-model {output_dir / 'final'} <video>")

if __name__ == "__main__":
    main()
