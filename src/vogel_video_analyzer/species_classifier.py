"""
Bird species classification module using Hugging Face transformers
"""

import warnings
from typing import Optional, Dict, List, Tuple
from pathlib import Path

try:
    from transformers import pipeline
    from PIL import Image
    import torch
    SPECIES_AVAILABLE = True
except ImportError:
    SPECIES_AVAILABLE = False


class BirdSpeciesClassifier:
    """Classifies bird species using a pre-trained model from Hugging Face"""
    
    def __init__(self, model_name: str = "chriamue/bird-species-classifier", confidence_threshold: float = 0.3):
        """
        Initialize the species classifier
        
        Args:
            model_name: Hugging Face model identifier
            confidence_threshold: Minimum confidence score (0.0-1.0)
        """
        if not SPECIES_AVAILABLE:
            raise ImportError(
                "Species identification requires additional dependencies. Install with:\n"
                "pip install vogel-video-analyzer[species]"
            )
        
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.classifier = None
        self._load_model()
    
    def _load_model(self):
        """Load the Hugging Face model"""
        try:
            print(f"🤖 Loading bird species classification model: {self.model_name}")
            print(f"   (First run will download ~100-300MB, then cached locally)")
            
            # Suppress some warnings from transformers
            warnings.filterwarnings('ignore', category=FutureWarning)
            
            self.classifier = pipeline(
                "image-classification",
                model=self.model_name,
                device=0 if torch.cuda.is_available() else -1  # Use GPU if available
            )
            
            print(f"   ✅ Model loaded successfully")
            
        except Exception as e:
            print(f"   ❌ Error loading model: {e}")
            print(f"   Falling back to basic bird detection only")
            self.classifier = None
    
    def classify_image(self, image, top_k: int = 3) -> List[Dict[str, any]]:
        """
        Classify bird species in an image
        
        Args:
            image: PIL Image or numpy array
            top_k: Return top K predictions
            
        Returns:
            List of dicts with 'label' and 'score' keys
        """
        if self.classifier is None:
            return []
        
        try:
            # Convert numpy array to PIL Image if needed
            if not isinstance(image, Image.Image):
                image = Image.fromarray(image)
            
            # Get predictions
            predictions = self.classifier(image, top_k=top_k)
            
            # Filter by confidence threshold
            filtered = [
                pred for pred in predictions 
                if pred['score'] >= self.confidence_threshold
            ]
            
            return filtered
            
        except Exception as e:
            print(f"   ⚠️  Classification error: {e}")
            return []
    
    def classify_crop(self, frame, bbox: Tuple[int, int, int, int], top_k: int = 3) -> List[Dict[str, any]]:
        """
        Classify a cropped region of a frame
        
        Args:
            frame: Full video frame (numpy array)
            bbox: Bounding box (x1, y1, x2, y2)
            top_k: Return top K predictions
            
        Returns:
            List of dicts with 'label' and 'score' keys
        """
        try:
            x1, y1, x2, y2 = bbox
            
            # Ensure coordinates are within frame
            h, w = frame.shape[:2]
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(w, int(x2)), min(h, int(y2))
            
            # Crop the region
            cropped = frame[y1:y2, x1:x2]
            
            if cropped.size == 0:
                return []
            
            # Classify the crop
            return self.classify_image(cropped, top_k=top_k)
            
        except Exception as e:
            print(f"   ⚠️  Crop classification error: {e}")
            return []
    
    @staticmethod
    def is_available() -> bool:
        """Check if species classification dependencies are installed"""
        return SPECIES_AVAILABLE
    
    @staticmethod
    def format_species_name(label: str) -> str:
        """
        Format species label for display
        
        Args:
            label: Raw label from model
            
        Returns:
            Formatted species name
        """
        # Remove common prefixes and format
        label = label.replace('_', ' ')
        
        # Capitalize each word
        words = label.split()
        formatted = ' '.join(word.capitalize() for word in words)
        
        return formatted


def aggregate_species_detections(detections: List[Dict[str, any]]) -> Dict[str, Dict[str, any]]:
    """
    Aggregate multiple species detections
    
    Args:
        detections: List of detection dicts with 'species' and 'confidence'
        
    Returns:
        Dict mapping species name to aggregated stats
    """
    species_stats = {}
    
    for detection in detections:
        species = detection.get('species', 'Unknown')
        confidence = detection.get('confidence', 0.0)
        
        if species not in species_stats:
            species_stats[species] = {
                'count': 0,
                'total_confidence': 0.0,
                'max_confidence': 0.0,
                'min_confidence': 1.0
            }
        
        stats = species_stats[species]
        stats['count'] += 1
        stats['total_confidence'] += confidence
        stats['max_confidence'] = max(stats['max_confidence'], confidence)
        stats['min_confidence'] = min(stats['min_confidence'], confidence)
    
    # Calculate averages
    for species, stats in species_stats.items():
        stats['avg_confidence'] = stats['total_confidence'] / stats['count']
    
    # Sort by count (descending)
    sorted_species = dict(sorted(
        species_stats.items(), 
        key=lambda x: x[1]['count'], 
        reverse=True
    ))
    
    return sorted_species
