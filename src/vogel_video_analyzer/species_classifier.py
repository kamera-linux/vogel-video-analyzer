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

from .i18n import t


# Translation dictionary for common bird species
# English names from kamera-linux/german-bird-classifier
ENGLISH_NAMES = {
    'PARUS MAJOR': 'Great Tit',
    'BLUE TIT': 'Blue Tit',
    'MARSH TIT': 'Marsh Tit',
    'EURASIAN NUTHATCH': 'Eurasian Nuthatch',
    'EUROPEAN GREENFINCH': 'European Greenfinch',
    'HAWFINCH': 'Hawfinch',
    'HOUSE SPARROW': 'House Sparrow',
    'EUROPEAN ROBIN': 'European Robin',
}

BIRD_NAME_TRANSLATIONS = {
    'de': {
        # European garden birds (from kamera-linux/german-bird-classifier)
        'PARUS MAJOR': 'Kohlmeise',
        'BLUE TIT': 'Blaumeise',
        'MARSH TIT': 'Sumpfmeise',
        'EURASIAN NUTHATCH': 'Kleiber',
        'EUROPEAN GREENFINCH': 'Grünfink',
        'HAWFINCH': 'Kernbeißer',
        'HOUSE SPARROW': 'Haussperling',
        'EUROPEAN ROBIN': 'Rotkehlchen',
        
        # Additional European garden birds
        'COMMON STARLING': 'Star',
        'EUROPEAN GOLDFINCH': 'Stieglitz',
        'EUROPEAN TURTLE DOVE': 'Turteltaube',
        'EURASIAN BULLFINCH': 'Gimpel',
        'EURASIAN GOLDEN ORIOLE': 'Pirol',
        'EURASIAN MAGPIE': 'Elster',
        'HOUSE SPARROW': 'Haussperling',
        'COMMON HOUSE MARTIN': 'Mehlschwalbe',
        'BARN SWALLOW': 'Rauchschwalbe',
        'BARN OWL': 'Schleiereule',
        'CROW': 'Krähe',
        'COMMON FIRECREST': 'Sommergoldhähnchen',
        'BEARDED REEDLING': 'Bartmeise',
        
        # American birds (often misidentified)
        'AMERICAN ROBIN': 'Amerikanische Wanderdrossel',
        'AMERICAN GOLDFINCH': 'Goldzeisig',
        'BLACK-CAPPED CHICKADEE': 'Schwarzkopfmeise',
        'NORTHERN CARDINAL': 'Roter Kardinal',
        'DOWNY WOODPECKER': 'Dunenspecht',
        'INDIGO BUNTING': 'Indigofink',
        
        # Asian/exotic pheasants (common misidentifications)
        'CABOTS TRAGOPAN': 'Cabot-Tragopan',
        'BLOOD PHEASANT': 'Blutfasan',
        'SATYR TRAGOPAN': 'Satyr-Tragopan',
        
        # Exotic/tropical (common misidentifications)
        'AZURE BREASTED PITTA': 'Azurbrustpitta',
        'BULWERS PHEASANT': 'Bulwerfasan',
        'BORNEAN PHEASANT': 'Borneo-Fasan',
        'SAMATRAN THRUSH': 'Sumatra-Drossel',
        'FAIRY PENGUIN': 'Zwergpinguin',
        'OILBIRD': 'Fettschwalm',
        'BLUE DACNIS': 'Blautangare',
        'FRILL BACK PIGEON': 'Kröpfer-Taube',
        'JACOBIN PIGEON': 'Jacobiner-Taube',
        'WHITE THROATED BEE EATER': 'Weißkehlspint',
    },
    'ja': {
        # European garden birds (from kamera-linux/german-bird-classifier)
        'PARUS MAJOR': 'シジュウカラ',
        'BLUE TIT': 'アオガラ',
        'MARSH TIT': 'ヨーロッパコガラ',
        'EURASIAN NUTHATCH': 'ゴジュウカラ',
        'EUROPEAN GREENFINCH': 'アオカワラヒワ',
        'HAWFINCH': 'シメ',
        'HOUSE SPARROW': 'イエスズメ',
        'EUROPEAN ROBIN': 'ヨーロッパコマドリ',
        
        # Additional European garden birds
        'COMMON STARLING': 'ホシムクドリ',
        'EUROPEAN GOLDFINCH': 'ゴシキヒワ',
        'EUROPEAN TURTLE DOVE': 'コキジバト',
        'EURASIAN BULLFINCH': 'ウソ',
        'EURASIAN GOLDEN ORIOLE': 'ニシコウライウグイス',
        'EURASIAN MAGPIE': 'カササギ',
        'HOUSE SPARROW': 'イエスズメ',
        'COMMON HOUSE MARTIN': 'ニシイワツバメ',
        'BARN SWALLOW': 'ツバメ',
        'BARN OWL': 'メンフクロウ',
        'CROW': 'カラス',
        'COMMON FIRECREST': 'マミジロキクイタダキ',
        'BEARDED REEDLING': 'ヒゲガラ',
        
        # American birds
        'AMERICAN ROBIN': 'コマツグミ',
        'AMERICAN GOLDFINCH': 'オウゴンヒワ',
        'BLACK-CAPPED CHICKADEE': 'アメリカコガラ',
        'NORTHERN CARDINAL': 'ショウジョウコウカンチョウ',
        'DOWNY WOODPECKER': 'コゲラ',
        'INDIGO BUNTING': 'ルリノジコ',
        
        # Asian/exotic pheasants
        'CABOTS TRAGOPAN': 'カボットジュケイ',
        'BLOOD PHEASANT': 'ベニジュケイ',
        'SATYR TRAGOPAN': 'ニジュケイ',
        
        # Exotic/tropical
        'AZURE BREASTED PITTA': 'ムネアオヤイロチョウ',
        'BULWERS PHEASANT': 'ハイイロコクジャク',
        'BORNEAN PHEASANT': 'ボルネオコクジャク',
        'SAMATRAN THRUSH': 'スマトラツグミ',
        'FAIRY PENGUIN': 'コガタペンギン',
        'OILBIRD': 'アブラヨタカ',
        'BLUE DACNIS': 'ルリミツドリ',
        'FRILL BACK PIGEON': 'フリルバックピジョン',
        'JACOBIN PIGEON': 'ジャコビンピジョン',
        'WHITE THROATED BEE EATER': 'ノドジロハチクイ',
    }
}

# Create reverse mapping: German lowercase -> English uppercase
# This is needed for models that use German labels (like kamera-linux/german-bird-classifier)
GERMAN_TO_ENGLISH = {
    v.lower(): k for k, v in BIRD_NAME_TRANSLATIONS['de'].items()
}


class BirdSpeciesClassifier:
    """Classifies bird species using a pre-trained model from Hugging Face"""
    
    def __init__(self, model_name: str = "chriamue/bird-species-classifier", confidence_threshold: float = 0.3):
        """
        Initialize the species classifier
        
        Args:
            model_name: Hugging Face model identifier
                       Default: "chriamue/bird-species-classifier" (8.5M params, EfficientNet-based)
                       Alternatives:
                       - "dima806/bird_species_image_detection" (ViT-based, 86M params, larger but lower confidence)
                       - "prithivMLmods/Bird-Species-Classifier-526" (SigLIP2-based, 93M params, 526 species)
            confidence_threshold: Minimum confidence score (0.0-1.0), default 0.3
        
        Note:
            ⚠️  EXPERIMENTAL FEATURE: Species identification accuracy is currently limited,
            especially for European garden birds. All tested models tend to misidentify
            common European species (e.g., Great Tit, Robin, Blackbird) as exotic species.
            Use results with caution and consider them as rough estimates only.
            
            For best results with European birds, consider training a custom model on
            European-specific datasets like iNaturalist Europe or NABU bird photos.
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
        """Load the Hugging Face model (from Hub or local path)"""
        try:
            # Check if model_name is a local path
            model_path = Path(self.model_name)
            if model_path.exists() and model_path.is_dir():
                print(f"🤖 {t('loading_species_model')} {model_path.name} (lokal)")
                model_source = str(model_path)
            else:
                print(f"🤖 {t('loading_species_model')} {self.model_name}")
                print(f"   ({t('model_download_info')})")
                model_source = self.model_name
            
            # Suppress some warnings from transformers
            warnings.filterwarnings('ignore', category=FutureWarning)
            
            # Determine device
            device = 0 if torch.cuda.is_available() else -1
            if device == 0:
                device_name = torch.cuda.get_device_name(0)
                print(f"   🎮 Using GPU: {device_name}")
            
            self.classifier = pipeline(
                "image-classification",
                model=model_source,
                device=device,
                batch_size=8  # Process up to 8 images in parallel for efficiency
            )
            
            print(f"   ✅ {t('model_loaded_success')}")
            
        except Exception as e:
            print(f"   ❌ {t('model_load_error')} {e}")
            print(f"   {t('fallback_basic_detection')}")
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
            
            # Return only predictions that meet the threshold
            # Do not return low-confidence predictions as fallback
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
    
    def classify_crops_batch(self, frame, bboxes: List[Tuple[int, int, int, int]], top_k: int = 3) -> List[List[Dict[str, any]]]:
        """
        Classify multiple cropped regions from the same frame in a batch (efficient for GPU)
        
        Args:
            frame: Full video frame (numpy array)
            bboxes: List of bounding boxes [(x1, y1, x2, y2), ...]
            top_k: Return top K predictions per crop
            
        Returns:
            List of prediction lists, one per bounding box
        """
        if self.classifier is None or not bboxes:
            return [[] for _ in bboxes]
        
        try:
            # Crop all regions
            crops = []
            valid_indices = []
            
            h, w = frame.shape[:2]
            for idx, bbox in enumerate(bboxes):
                x1, y1, x2, y2 = bbox
                
                # Ensure coordinates are within frame
                x1, y1 = max(0, int(x1)), max(0, int(y1))
                x2, y2 = min(w, int(x2)), min(h, int(y2))
                
                # Crop the region
                cropped = frame[y1:y2, x1:x2]
                
                if cropped.size > 0:
                    # Convert to PIL Image
                    crops.append(Image.fromarray(cropped))
                    valid_indices.append(idx)
            
            if not crops:
                return [[] for _ in bboxes]
            
            # Batch classify all crops at once (GPU-efficient)
            all_predictions = self.classifier(crops, top_k=top_k, batch_size=len(crops))
            
            # Organize results back to match input bboxes order
            results = [[] for _ in bboxes]
            for crop_idx, predictions in enumerate(all_predictions):
                original_idx = valid_indices[crop_idx]
                
                # Filter by confidence threshold
                filtered = [
                    pred for pred in predictions 
                    if pred['score'] >= self.confidence_threshold
                ]
                results[original_idx] = filtered
            
            return results
            
        except Exception as e:
            print(f"   ⚠️  Batch classification error: {e}")
            return [[] for _ in bboxes]

    
    @staticmethod
    def is_available() -> bool:
        """Check if species classification dependencies are installed"""
        return SPECIES_AVAILABLE
    
    @staticmethod
    def translate_species_name(species_name: str) -> str:
        """
        Translate bird species name to current language
        
        Args:
            species_name: Species name in English (uppercase) or German (any case)
            
        Returns:
            Translated species name or original if no translation available
        """
        from .i18n import get_language
        
        # Try to convert German label to English key (for models using German labels)
        species_name_lower = species_name.lower()
        if species_name_lower in GERMAN_TO_ENGLISH:
            species_name = GERMAN_TO_ENGLISH[species_name_lower]
        
        lang = get_language()
        if lang in BIRD_NAME_TRANSLATIONS and species_name in BIRD_NAME_TRANSLATIONS[lang]:
            return BIRD_NAME_TRANSLATIONS[lang][species_name]
        
        # If no translation found, return proper English name or formatted version
        return ENGLISH_NAMES.get(species_name, ' '.join(word.capitalize() for word in species_name.split()))
    
    @staticmethod
    def get_multilingual_name(species_name: str, show_flags: bool = True, opencv_compatible: bool = False) -> str:
        """
        Get bird name in all available languages with flag emojis
        
        Args:
            species_name: Species name in English (uppercase) or German (any case)
            show_flags: Whether to show flag emojis (default: True)
            opencv_compatible: Use only ASCII-compatible characters (default: False)
            
        Returns:
            Multilingual string with all translations
            Example: "EN: Great Tit | DE: Kohlmeise" (opencv_compatible=True)
            Example: "🇬🇧 Great Tit 🇩🇪 Kohlmeise 🇯🇵 シジュウカラ" (opencv_compatible=False)
        """
        # Try to convert German label to English key (for models using German labels)
        species_name_lower = species_name.lower()
        if species_name_lower in GERMAN_TO_ENGLISH:
            species_name = GERMAN_TO_ENGLISH[species_name_lower]
        
        # Get proper English name from dictionary, or format as title case
        en_name = ENGLISH_NAMES.get(species_name, ' '.join(word.capitalize() for word in species_name.split()))
        
        # Get translations
        de_name = BIRD_NAME_TRANSLATIONS.get('de', {}).get(species_name, en_name)
        ja_name = BIRD_NAME_TRANSLATIONS.get('ja', {}).get(species_name, en_name)
        
        if opencv_compatible:
            # Use ASCII-only format for OpenCV compatibility
            parts = [f"EN: {en_name}"]
            
            # Add German translation if available
            if species_name in BIRD_NAME_TRANSLATIONS.get('de', {}):
                parts.append(f"DE: {de_name}")
            
            # Add Japanese translation if available
            if species_name in BIRD_NAME_TRANSLATIONS.get('ja', {}):
                parts.append(f"JA: {ja_name}")
            
            return ' | '.join(parts)
        else:
            # For video annotation with PIL: return German name only
            # The rendering code will fetch EN/DE/JA separately and render with flag icons
            if show_flags:
                return de_name
            else:
                # No flags: concatenate all available names
                parts = [en_name]
                if species_name in BIRD_NAME_TRANSLATIONS.get('de', {}):
                    parts.append(de_name)
                if species_name in BIRD_NAME_TRANSLATIONS.get('ja', {}):
                    parts.append(ja_name)
                return ' / '.join(parts)
    
    @staticmethod
    def format_species_name(label: str, translate: bool = True) -> str:
        """
        Format species label for display
        
        Args:
            label: Raw label from model
            translate: Whether to translate species name (default: True)
            
        Returns:
            Formatted (and optionally translated) species name
        """
        # Remove common prefixes and format
        label = label.replace('_', ' ')
        
        # Capitalize each word
        words = label.split()
        formatted = ' '.join(word.capitalize() for word in words)
        
        # Translate if requested
        if translate:
            formatted = BirdSpeciesClassifier.translate_species_name(formatted.upper())
        
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
