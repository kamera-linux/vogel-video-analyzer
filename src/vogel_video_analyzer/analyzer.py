"""
Video analyzer core module for bird detection in videos using YOLOv8
"""

import cv2
import subprocess
import tempfile
import os
import numpy as np
from pathlib import Path
from datetime import timedelta
from ultralytics import YOLO
from .i18n import t

# Try to import PIL for Unicode text rendering
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Optional species classification
try:
    from .species_classifier import BirdSpeciesClassifier, aggregate_species_detections
    SPECIES_AVAILABLE = True
except ImportError:
    SPECIES_AVAILABLE = False
    BirdSpeciesClassifier = None
    aggregate_species_detections = None

def render_emoji_icon(emoji, size=24):
    """
    Render flag emoji with accurate flag designs
    
    Args:
        emoji: Emoji character (e.g., '🇩🇪', '🇬🇧', '🇯🇵')
        size: Icon size in pixels
        
    Returns:
        PIL Image with colored flag representation (in BGR for later OpenCV compatibility)
    """
    if not PIL_AVAILABLE:
        return None
    
    try:
        width = int(size * 1.5)
        flag_array = np.zeros((size, width, 3), dtype=np.uint8)
        
        if emoji == '🇩🇪':
            # Germany: Horizontal stripes (Black, Red, Gold)
            stripe_height = size // 3
            flag_array[0:stripe_height, :] = (0, 0, 0)  # BGR: Black
            flag_array[stripe_height:2*stripe_height, :] = (0, 0, 221)  # BGR: Red
            flag_array[2*stripe_height:, :] = (0, 206, 255)  # BGR: Gold
            
        elif emoji == '🇬🇧':
            # UK: Simplified Union Jack
            # Blue background
            flag_array[:, :] = (125, 36, 0)  # BGR: Blue
            
            # White diagonal cross (thicker)
            thickness = max(2, size // 8)
            # Diagonals
            cv2.line(flag_array, (0, 0), (width, size), (255, 255, 255), thickness)
            cv2.line(flag_array, (width, 0), (0, size), (255, 255, 255), thickness)
            
            # Red cross (vertical and horizontal)
            cross_thickness = max(3, size // 6)
            cv2.line(flag_array, (width//2, 0), (width//2, size), (38, 17, 206), cross_thickness)  # BGR: Red
            cv2.line(flag_array, (0, size//2), (width, size//2), (38, 17, 206), cross_thickness)  # BGR: Red
            
        elif emoji == '🇯🇵':
            # Japan: White background with red circle
            flag_array[:, :] = (255, 255, 255)  # BGR: White
            
            # Red circle in center
            center_x = width // 2
            center_y = size // 2
            radius = int(size * 0.3)
            cv2.circle(flag_array, (center_x, center_y), radius, (60, 20, 220), -1)  # BGR: Red (filled)
            
        else:
            # Fallback: Gray
            flag_array[:, :] = (128, 128, 128)
        
        # Add border
        cv2.rectangle(flag_array, (0, 0), (width - 1, size - 1), (80, 80, 80), 1)
        
        # Convert BGR to RGB for PIL
        flag_rgb = cv2.cvtColor(flag_array, cv2.COLOR_BGR2RGB)
        return Image.fromarray(flag_rgb)
    except Exception as e:
        return None


def render_flag_from_file(flag_path, size=24):
    """
    Load flag icon from image file
    
    Args:
        flag_path: Path to flag image file (PNG, JPG, etc.)
        size: Target height in pixels
        
    Returns:
        PIL Image with flag icon, or None if loading fails
    """
    if not PIL_AVAILABLE:
        return None
    
    try:
        flag_path = Path(flag_path)
        if not flag_path.exists():
            return None
        
        img = Image.open(flag_path)
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Maintain 3:2 aspect ratio (standard flag ratio)
        width = int(size * 1.5)
        img = img.resize((width, size), Image.Resampling.LANCZOS)
        
        return img
    except Exception as e:
        return None


def render_flag_icon(source, size=24, flag_dir=None):
    """
    Flexible flag rendering supporting multiple input types
    
    Args:
        source: Can be:
            - Emoji string ('🇩🇪', '🇬🇧', '🇯🇵') -> pixel rendering
            - Path to image file (str or Path)
            - PIL Image object
            - numpy array (BGR or RGB)
        size: Icon height in pixels
        flag_dir: Optional directory to search for flag files (e.g., 'assets/flags/')
        
    Returns:
        PIL Image with flag icon, or None if rendering fails
        
    Examples:
        # Emoji (pixel-rendered)
        icon = render_flag_icon('🇩🇪', size=24)
        
        # File path
        icon = render_flag_icon('assets/flags/de.png', size=24)
        
        # Auto-detect from directory
        icon = render_flag_icon('de', size=24, flag_dir='assets/flags/')
        
        # PIL Image
        img = Image.open('flag.png')
        icon = render_flag_icon(img, size=24)
    """
    if not PIL_AVAILABLE:
        return None
    
    try:
        # String input
        if isinstance(source, str):
            # Check if it's an emoji
            if source in ['🇩🇪', '🇬🇧', '🇯🇵']:
                return render_emoji_icon(source, size)
            
            # Check if it's a file path
            source_path = Path(source)
            if source_path.exists() and source_path.is_file():
                return render_flag_from_file(source_path, size)
            
            # Try to find file in flag_dir
            if flag_dir:
                flag_dir = Path(flag_dir)
                # Try different extensions
                for ext in ['.png', '.jpg', '.jpeg', '.svg']:
                    flag_file = flag_dir / f"{source}{ext}"
                    if flag_file.exists():
                        return render_flag_from_file(flag_file, size)
            
            # Fallback to emoji rendering if string looks like emoji
            if len(source) <= 4 and not source.isalpha():
                return render_emoji_icon(source, size)
        
        # PIL Image input
        elif isinstance(source, Image.Image):
            width = int(size * 1.5)
            img = source.copy()
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return img.resize((width, size), Image.Resampling.LANCZOS)
        
        # NumPy array input
        elif isinstance(source, np.ndarray):
            # Assume BGR format (OpenCV default)
            if len(source.shape) == 3 and source.shape[2] == 3:
                # Convert BGR to RGB
                img_rgb = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img_rgb)
                width = int(size * 1.5)
                return img.resize((width, size), Image.Resampling.LANCZOS)
        
        # Path object input
        elif isinstance(source, Path):
            if source.exists() and source.is_file():
                return render_flag_from_file(source, size)
        
        return None
        
    except Exception as e:
        return None


def put_unicode_text(img, text, position, font_size=30, color=(255, 255, 255), bg_color=None, emoji_prefix=None, flag_dir=None):
    """
    Draw Unicode text (including emojis) on image using PIL
    
    Args:
        img: OpenCV image (numpy array, BGR)
        text: Text to draw (can contain Unicode/emojis)
        position: (x, y) position tuple
        font_size: Font size in pixels
        color: Text color in BGR format
        bg_color: Background color in BGR format (None = transparent)
        emoji_prefix: Optional emoji/flag to render as icon before text (e.g., '🇩🇪', 'de', or path)
        flag_dir: Directory containing flag image files (optional)
        
    Returns:
        Modified image with text
    """
    if not PIL_AVAILABLE:
        # Fallback to cv2.putText if PIL not available
        print("WARNING: PIL not available, using cv2.putText fallback")
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_size/30, color, 2, cv2.LINE_AA)
        return img
    
    # Make a copy to avoid modifying original
    img = img.copy()
    
    # Convert BGR to RGB for PIL
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Render flag icon if specified (now using hybrid system)
    emoji_icon = None
    emoji_width = 0
    if emoji_prefix:
        # Use hybrid render_flag_icon function
        emoji_icon = render_flag_icon(emoji_prefix, size=font_size, flag_dir=flag_dir)
        if emoji_icon:
            emoji_width = emoji_icon.width + 4  # Add spacing
    
    # Try to load fonts - we need TWO: one for Latin and one for CJK (Japanese)
    try:
        # Latin font paths (for English/German)
        latin_font_paths = [
            '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',  # Noto Sans
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # DejaVu
            '/usr/share/fonts/TTF/DejaVuSans.ttf',              # Arch
            '/System/Library/Fonts/Helvetica.ttc',              # macOS
            'C:\\Windows\\Fonts\\arial.ttf',                    # Windows
        ]
        
        # CJK font paths (for Japanese)
        cjk_font_paths = [
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Noto CJK
            '/usr/share/fonts/truetype/noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf',  # Takao
            '/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf',  # VL Gothic
            '/System/Library/Fonts/Hiragino Sans GB.ttc',       # macOS
            'C:\\Windows\\Fonts\\msgothic.ttc',                 # MS Gothic (Windows)
        ]
        
        # Load Latin font
        latin_font = None
        for font_path in latin_font_paths:
            if Path(font_path).exists():
                try:
                    latin_font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
        
        # Load CJK font
        cjk_font = None
        for font_path in cjk_font_paths:
            if Path(font_path).exists():
                try:
                    cjk_font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
        
        # Use Latin font as primary, fallback to default if both fail
        font = latin_font if latin_font else ImageFont.load_default()
    except:
        font = ImageFont.load_default()
        cjk_font = None
    
    # Detect if text contains CJK characters and choose appropriate font
    def contains_cjk(text):
        """Check if text contains CJK (Chinese/Japanese/Korean) characters"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff' or '\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff':
                return True
        return False
    
    # Choose font based on text content
    active_font = cjk_font if (cjk_font and contains_cjk(text)) else font
    
    # Adjust position for emoji icon
    text_position = (position[0] + emoji_width, position[1])
    
    # Get text bounding box for background
    bbox = draw.textbbox(text_position, text, font=active_font)
    
    # Adjust bbox to include emoji if present
    if emoji_icon:
        bbox = (position[0], bbox[1], bbox[2], bbox[3])
    
    # Draw background if specified
    if bg_color is not None:
        # Convert BGR to RGB
        bg_rgb = (bg_color[2], bg_color[1], bg_color[0])
        padding = 5
        draw.rectangle(
            [bbox[0] - padding, bbox[1] - padding, 
             bbox[2] + padding, bbox[3] + padding],
            fill=bg_rgb
        )
    
    # Paste emoji icon if available (no transparency, direct paste)
    if emoji_icon:
        # Calculate vertical centering
        emoji_y = position[1] + (font_size - emoji_icon.height) // 2
        # Convert emoji icon to RGB if needed and paste without mask
        if emoji_icon.mode == 'RGBA':
            emoji_icon = emoji_icon.convert('RGB')
        img_pil.paste(emoji_icon, (position[0], emoji_y))
    
    # Draw text (convert BGR to RGB) - use the appropriate font
    text_rgb = (color[2], color[1], color[0])
    draw.text(text_position, text, font=active_font, fill=text_rgb)
    
    # Convert back to BGR for OpenCV
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    return img_cv


class VideoAnalyzer:
    """Analyzes videos for bird content using YOLOv8"""
    
    def __init__(self, model_path="yolov8n.pt", threshold=0.3, target_class=14, identify_species=False, species_model="dima806/bird_species_image_detection", species_threshold=0.3):
        """
        Initialize the analyzer
        
        Args:
            model_path: Path to YOLO model (searches: models/, config/models/, current dir, auto-download)
            threshold: Confidence threshold (0.0-1.0), default 0.3 for bird detection
            target_class: COCO class for bird (14=bird)
            identify_species: Enable bird species classification (requires species dependencies)
            species_model: Hugging Face model for species classification (default: dima806/bird_species_image_detection)
            species_threshold: Minimum confidence threshold for species classification (default: 0.3)
        """
        model_path = self._find_model(model_path)
        print(f"🤖 {t('loading_model')} {model_path}")
        self.model = YOLO(model_path)
        self.threshold = threshold
        self.target_class = target_class
        self.identify_species = identify_species
        self.species_classifier = None
        
        # Initialize species classifier if requested
        if self.identify_species:
            if not SPECIES_AVAILABLE:
                print(f"   ⚠️  Species identification requires additional dependencies.")
                print(f"   Install with: pip install vogel-video-analyzer[species]")
                print(f"   Continuing with basic bird detection only.\n")
                self.identify_species = False
            else:
                try:
                    self.species_classifier = BirdSpeciesClassifier(model_name=species_model, confidence_threshold=species_threshold)
                except Exception as e:
                    print(f"   ⚠️  Could not load species classifier: {e}")
                    print(f"   Continuing with basic bird detection only.\n")
                    self.identify_species = False
    
    def _find_model(self, model_name):
        """
        Search for model in various directories
        
        Search paths (in order):
        1. models/
        2. config/models/
        3. Current directory
        4. Let Ultralytics auto-download
        
        Args:
            model_name: Name or path of model
            
        Returns:
            Path to model or original name for auto-download
        """
        # If absolute path provided
        if Path(model_name).is_absolute() and Path(model_name).exists():
            return model_name
        
        # Define search paths
        search_paths = [
            Path('models') / model_name,
            Path('config/models') / model_name,
            Path(model_name)
        ]
        
        # Search in directories
        for path in search_paths:
            if path.exists():
                return str(path)
        
        # Not found → Ultralytics downloads automatically
        print(f"   ℹ️  {t('model_not_found').format(model_name=model_name)}")
        return model_name
        
    def analyze_video(self, video_path, sample_rate=5):
        """
        Analyze video frame by frame
        
        Args:
            video_path: Path to MP4 video
            sample_rate: Analyze every Nth frame (1=all, 5=every 5th, etc.)
            
        Returns:
            dict with statistics
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(t('video_not_found').format(path=str(video_path)))
            
        print(f"\n📹 {t('analyzing')} {video_path.name}")
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(t('cannot_open_video').format(path=str(video_path)))
            
        # Video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"   📊 {t('video_info')} {width}x{height}, {fps:.1f} FPS, {duration:.1f}s, {total_frames} {t('frames')}")
        
        # Analysis variables
        frames_analyzed = 0
        frames_with_birds = 0
        bird_detections = []
        current_frame = 0
        
        print(f"   🔍 {t('analyzing_every_nth').format(n=sample_rate)}")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            current_frame += 1
            
            # Apply sample rate
            if current_frame % sample_rate != 0:
                continue
                
            frames_analyzed += 1
            
            # YOLO inference
            results = self.model(frame, verbose=False)
            
            # Check bird detection
            birds_in_frame = 0
            frame_species = []
            bird_bboxes = []  # Collect all bounding boxes for batch processing
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    if cls == self.target_class and conf >= self.threshold:
                        birds_in_frame += 1
                        
                        # Collect bounding boxes for batch species identification
                        if self.identify_species and self.species_classifier:
                            xyxy = box.xyxy[0].cpu().numpy()
                            x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                            bird_bboxes.append((x1, y1, x2, y2))
            
            # Batch process all bird crops at once (GPU-efficient)
            if bird_bboxes and self.identify_species and self.species_classifier:
                try:
                    batch_predictions = self.species_classifier.classify_crops_batch(
                        frame, bird_bboxes, top_k=1
                    )
                    
                    for predictions in batch_predictions:
                        if predictions:
                            species_info = predictions[0]
                            # Translate species name to current language
                            translated_name = BirdSpeciesClassifier.format_species_name(
                                species_info['label'], translate=True
                            )
                            frame_species.append({
                                'species': translated_name,
                                'confidence': species_info['score']
                            })
                except Exception as e:
                    # Log error for debugging
                    import sys
                    print(f"   ⚠️  Species classification error (frame {current_frame}): {e}", file=sys.stderr)
                    import traceback
                    traceback.print_exc()
                    pass
                        
            if birds_in_frame > 0:
                frames_with_birds += 1
                timestamp = current_frame / fps if fps > 0 else 0
                detection_entry = {
                    'frame': current_frame,
                    'timestamp': timestamp,
                    'birds': birds_in_frame
                }
                
                # Add species information if available
                if frame_species:
                    detection_entry['species'] = frame_species
                
                bird_detections.append(detection_entry)
                
            # Progress every 30 analyzed frames
            if frames_analyzed % 30 == 0:
                progress = (frames_analyzed * sample_rate / total_frames) * 100
                print(f"   ⏳ {progress:.1f}% ({frames_analyzed}/{total_frames//sample_rate} {t('frames')})", end='\r')
                
        cap.release()
        
        # Calculate statistics
        bird_percentage = (frames_with_birds / frames_analyzed * 100) if frames_analyzed > 0 else 0
        
        # Find continuous bird segments
        segments = self._find_bird_segments(bird_detections, fps, sample_rate)
        
        stats = {
            'video_file': video_path.name,
            'video_path': str(video_path),
            'resolution': f"{width}x{height}",
            'fps': fps,
            'duration_seconds': duration,
            'total_frames': total_frames,
            'frames_analyzed': frames_analyzed,
            'sample_rate': sample_rate,
            'frames_with_birds': frames_with_birds,
            'bird_percentage': bird_percentage,
            'bird_detections': len(bird_detections),
            'bird_segments': segments,
            'detections': bird_detections,  # Full detection list for HTML reports
            'threshold': self.threshold,
            'model': str(self.model.ckpt_path if hasattr(self.model, 'ckpt_path') else 'unknown')
        }
        
        # Add species statistics if species identification was enabled
        if self.identify_species and SPECIES_AVAILABLE:
            # Extract all species detections from bird_detections
            all_species = []
            for detection in bird_detections:
                if 'species' in detection:
                    all_species.extend(detection['species'])
            
            if all_species:
                species_stats = aggregate_species_detections(all_species)
                stats['species_stats'] = species_stats
        
        print(f"\n   ✅ {t('analysis_complete')}")
        return stats
        
    def _find_bird_segments(self, detections, fps, sample_rate):
        """
        Find continuous time segments with bird presence
        
        Args:
            detections: List of bird detections
            fps: Video FPS
            sample_rate: Frame sample rate
            
        Returns:
            List of segments with start/end times
        """
        if not detections:
            return []
            
        segments = []
        current_segment = None
        max_gap = 2.0 * sample_rate  # Max 2 second gap
        
        for detection in detections:
            timestamp = detection['timestamp']
            
            if current_segment is None:
                # Start new segment
                current_segment = {
                    'start': timestamp,
                    'end': timestamp,
                    'detections': 1
                }
            elif timestamp - current_segment['end'] <= max_gap:
                # Extend segment
                current_segment['end'] = timestamp
                current_segment['detections'] += 1
            else:
                # End segment and start new one
                segments.append(current_segment)
                current_segment = {
                    'start': timestamp,
                    'end': timestamp,
                    'detections': 1
                }
                
        # Add last segment
        if current_segment:
            segments.append(current_segment)
            
        return segments
        
    def print_report(self, stats):
        """
        Print formatted report
        
        Args:
            stats: Statistics dictionary
        """
        print(f"\n🎬 {t('report_title')}")
        print("━" * 70)
        
        print(f"\n📁 {t('report_file')} {stats['video_path']}")
        print(f"📊 {t('report_total_frames')} {stats['total_frames']} ({t('report_analyzed')} {stats['frames_analyzed']})")
        print(f"⏱️  {t('report_duration')} {stats['duration_seconds']:.1f} {t('report_seconds')}")
        print(f"🐦 {t('report_bird_frames')} {stats['frames_with_birds']} ({stats['bird_percentage']:.1f}%)")
        print(f"🎯 {t('report_bird_segments')} {len(stats['bird_segments'])}")
        
        if stats['bird_segments']:
            print(f"\n📍 {t('report_detected_segments')}")
            for i, segment in enumerate(stats['bird_segments'], 1):
                start = timedelta(seconds=int(segment['start']))
                end = timedelta(seconds=int(segment['end']))
                duration = segment['end'] - segment['start']
                bird_pct = (segment['detections'] / stats['frames_analyzed']) * 100
                print(f"  {'┌' if i == 1 else '├'} {t('report_segment')} {i}: {start} - {end} ({bird_pct:.0f}% {t('report_bird_frames_short')})")
                if i == len(stats['bird_segments']):
                    print(f"  └")
        
        # Status
        if stats['bird_percentage'] >= 50:
            print(f"\n✅ {t('report_status')} {t('status_significant')}")
        elif stats['bird_percentage'] > 0:
            print(f"\n⚠️  {t('report_status')} {t('status_limited')}")
        else:
            print(f"\n❌ {t('report_status')} {t('status_none')}")
        
        # Species identification results
        if 'species_stats' in stats and stats['species_stats']:
            species_stats = stats['species_stats']
            print(f"\n🦜 {t('species_title')}")
            if species_stats:
                print(f"   {t('species_count').format(count=len(species_stats))}")
                print()
                for species_name, data in sorted(species_stats.items(), 
                                                  key=lambda x: x[1]['count'], 
                                                  reverse=True):
                    # Translate species name to current language
                    translated_name = BirdSpeciesClassifier.translate_species_name(species_name)
                    count = data['count']
                    avg_conf = data['avg_confidence']
                    print(f"  • {translated_name}")
                    print(f"    {t('species_detections').format(detections=count)} ({t('species_avg_confidence')}: {avg_conf:.2f})")
            else:
                print(f"   {t('species_no_detections')}")
        
        print("━" * 70)

    def annotate_video(self, video_path, output_path, sample_rate=1, show_timestamp=True, show_confidence=True, box_color=(0, 255, 0), text_color=(255, 255, 255), multilingual=False, font_size=20, flag_dir=None):
        """
        Create annotated video with bounding boxes and species labels
        
        Args:
            video_path: Path to input video
            output_path: Path for output annotated video
            sample_rate: Process every Nth frame (1=all frames)
            show_timestamp: Display timestamp on video
            show_confidence: Display confidence scores
            box_color: BGR color for bounding boxes (default: green)
            text_color: BGR color for text labels (default: white)
            multilingual: Show bird names in all languages with flags (default: False)
            font_size: Font size for species labels (default: 20)
            flag_dir: Directory containing flag image files (optional, default: assets/flags/)
                     If None, uses pixel-rendered flags for DE, GB, JP
            
        Returns:
            dict with processing statistics
        """
        video_path = Path(video_path)
        output_path = Path(output_path)
        
        if not video_path.exists():
            raise FileNotFoundError(t('video_not_found').format(path=str(video_path)))
        
        # Set default flag directory if not specified
        if flag_dir is None:
            # Try to find assets/flags relative to this file
            module_dir = Path(__file__).parent.parent.parent
            flag_dir = module_dir / 'assets' / 'flags'
            if not flag_dir.exists():
                flag_dir = None  # Fall back to emoji rendering
            
        print(f"\n🎬 {t('annotation_creating')} {video_path.name}")
        if flag_dir and Path(flag_dir).exists():
            print(f"   {t('annotation_flag_directory')} {flag_dir}")
        print(f"{t('annotation_output')} {output_path}")
        
        # Open input video
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(t('cannot_open_video').format(path=str(video_path)))
            
        # Video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Handle high framerates that exceed codec limits
        # MPEG4 timebase denominator max is 65535, which limits FPS to ~65
        output_fps = fps
        if fps > 60:
            output_fps = 30.0  # Reduce to standard 30 FPS for compatibility
            print(f"   ℹ️  Original FPS ({fps:.1f}) exceeds codec limits, reducing output to {output_fps} FPS")
        
        # Create output video writer
        # Try different codecs for better compatibility
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, output_fps, (width, height))
        
        # Check if writer opened successfully
        if not out.isOpened():
            # Fallback to XVID with AVI container
            print(f"   ⚠️  MP4V codec not available, trying XVID with AVI...")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_path_avi = output_path.parent / (output_path.stem + '.avi')
            out = cv2.VideoWriter(str(output_path_avi), fourcc, output_fps, (width, height))
            if not out.isOpened():
                raise RuntimeError(f"Could not open video writer. Try installing ffmpeg: sudo apt install ffmpeg")
            output_path = output_path_avi
            print(f"   ℹ️  Output changed to: {output_path}")
        
        print(f"   📊 {t('annotation_video_info').format(width=width, height=height, fps=f'{fps:.1f}', output_fps=f'{output_fps:.1f}', frames=total_frames)}")
        print(f"   🔍 {t('annotation_processing').format(n=sample_rate)}")


        
        # Processing variables
        current_frame = 0
        frames_processed = 0
        total_birds_detected = 0
        
        # Cache for last detections (to avoid flickering)
        last_detections = []
        last_birds_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            current_frame += 1
            annotated_frame = frame.copy()
            
            # Process frame if matches sample rate
            if current_frame % sample_rate == 0:
                frames_processed += 1
                
                # YOLO inference
                results = self.model(frame, verbose=False)
                
                # Clear and rebuild detection cache
                last_detections = []
                birds_in_frame = 0
                bird_bboxes = []  # Collect all bounding boxes for batch processing
                bird_boxes_info = []  # Store YOLO box info
                
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        
                        if cls == self.target_class and conf >= self.threshold:
                            birds_in_frame += 1
                            total_birds_detected += 1
                            
                            # Get bounding box coordinates
                            xyxy = box.xyxy[0].cpu().numpy()
                            x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                            
                            # Store box info for batch processing
                            bird_bboxes.append((x1, y1, x2, y2))
                            bird_boxes_info.append({
                                'bbox': (x1, y1, x2, y2),
                                'conf': conf
                            })
                
                # Batch process all bird crops at once (GPU-efficient)
                if bird_bboxes and self.identify_species and self.species_classifier:
                    try:
                        batch_predictions = self.species_classifier.classify_crops_batch(
                            frame, bird_bboxes, top_k=1
                        )
                        
                        for idx, (predictions, box_info) in enumerate(zip(batch_predictions, bird_boxes_info)):
                            species_label = None
                            skip_detection = False
                            
                            if predictions:
                                species_info = predictions[0]
                                
                                # Use multilingual name if requested
                                if multilingual:
                                    # Use full Unicode format with emojis if PIL available
                                    bird_name = BirdSpeciesClassifier.get_multilingual_name(
                                        species_info['label'].upper(), 
                                        show_flags=PIL_AVAILABLE,
                                        opencv_compatible=not PIL_AVAILABLE
                                    )
                                else:
                                    bird_name = BirdSpeciesClassifier.format_species_name(
                                        species_info['label'], translate=True
                                    )
                                
                                if show_confidence:
                                    species_label = f"{bird_name} {species_info['score']:.0%}"
                                else:
                                    species_label = bird_name
                            else:
                                # No species passed threshold - skip this detection entirely
                                skip_detection = True
                            
                            # Fallback if species_label is still None
                            if species_label is None and not skip_detection:
                                # No species classification enabled - show as generic bird
                                if show_confidence:
                                    species_label = f"Bird {box_info['conf']:.0%}"
                                else:
                                    species_label = "Bird"
                            
                            # Store detection for reuse (only if not skipped)
                            if not skip_detection and species_label is not None:
                                last_detections.append({
                                    'bbox': box_info['bbox'],
                                    'label': species_label
                                })
                    except Exception as e:
                        # On error, fall back to generic bird labels
                        for box_info in bird_boxes_info:
                            if show_confidence:
                                species_label = f"Bird {box_info['conf']:.0%}"
                            else:
                                species_label = "Bird"
                            last_detections.append({
                                'bbox': box_info['bbox'],
                                'label': species_label
                            })
                elif bird_boxes_info:
                    # No species identification - show generic bird labels
                    for box_info in bird_boxes_info:
                        if show_confidence:
                            species_label = f"Bird {box_info['conf']:.0%}"
                        else:
                            species_label = "Bird"
                        last_detections.append({
                            'bbox': box_info['bbox'],
                            'label': species_label
                        })
                
                last_birds_count = birds_in_frame
            
            # Draw all cached detections (even on non-processed frames)
            for detection in last_detections:
                x1, y1, x2, y2 = detection['bbox']
                label = detection['label']
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), box_color, 2)
                
                # Use PIL for Unicode text if available, otherwise fallback to cv2
                if PIL_AVAILABLE and multilingual:
                    # Extract bird name and confidence
                    if '%' in label:
                        bird_part, conf_part = label.rsplit(' ', 1)
                    else:
                        bird_part = label
                        conf_part = ""
                    
                    # Get individual translations
                    try:
                        species_display = bird_part  # Already just the German name, no emojis
                        from .species_classifier import GERMAN_TO_ENGLISH, BIRD_NAME_TRANSLATIONS, ENGLISH_NAMES
                        species_key = GERMAN_TO_ENGLISH.get(species_display.lower())
                        
                        if species_key:
                            # Get translations (use proper English names from dictionary)
                            en_name = ENGLISH_NAMES.get(species_key, ' '.join(word.capitalize() for word in species_key.split()))
                            de_name = BIRD_NAME_TRANSLATIONS.get('de', {}).get(species_key, en_name)
                            ja_name = BIRD_NAME_TRANSLATIONS.get('ja', {}).get(species_key, en_name)
                            
                            # Multiline format with flag icons (hybrid rendering: PNG files if available, pixel fallback)
                            # Line 1: 🇬🇧 English name
                            # Line 2: 🇩🇪 German name
                            # Line 3: 🇯🇵 Japanese name
                            # Line 4: Confidence
                            lines = [
                                (en_name, 'gb'),  # Text + country code (loads PNG if available)
                                (de_name, 'de'),
                                (ja_name, 'jp'),
                                (conf_part, None)  # No icon for confidence
                            ]
                        else:
                            lines = [(label, None)]
                    except:
                        lines = [(label, None)]
                    
                    # Draw multiline with configurable font size
                    line_height = int(font_size * 1.4)  # Dynamic line height based on font size
                    total_height = len(lines) * line_height + 12  # Less padding
                    
                    # Calculate position - place box to the RIGHT of the bounding box
                    box_x_start = x2 + 10  # 10px gap to the right of bird box
                    box_y_start = y1
                    
                    # Dynamic width based on font size
                    box_width = int(font_size * 16)
                    box_y_end = box_y_start + total_height
                    
                    # Semi-transparent white background using PIL for better control
                    # Create overlay with alpha channel
                    overlay = annotated_frame.copy()
                    cv2.rectangle(
                        overlay,
                        (box_x_start, box_y_start),
                        (box_x_start + box_width, box_y_end),
                        (255, 255, 255),  # White background
                        -1
                    )
                    # Blend with original (0.7 = 70% opaque, 30% transparent)
                    cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0, annotated_frame)
                    
                    # Draw each line with black text and emoji icons
                    for i, line_data in enumerate(lines):
                        # Unpack line text and emoji
                        if isinstance(line_data, tuple):
                            line_text, emoji = line_data
                        else:
                            line_text, emoji = line_data, None
                        
                        # Slightly larger font for confidence percentage
                        current_font_size = font_size if i < len(lines) - 1 else int(font_size * 1.1)
                        annotated_frame = put_unicode_text(
                            annotated_frame,
                            line_text,
                            (box_x_start + 8, box_y_start + 8 + i * line_height),
                            font_size=current_font_size,
                            color=(0, 0, 0),  # Black text
                            bg_color=None,  # Background already drawn with transparency
                            emoji_prefix=emoji,  # Add emoji/flag icon
                            flag_dir=flag_dir  # Pass flag directory for hybrid rendering
                        )
                else:
                    # Fallback to OpenCV text (ASCII only)
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 3
                    )
                    
                    # Background rectangle
                    cv2.rectangle(
                        annotated_frame,
                        (x1, y1 - text_height - 15),
                        (x1 + text_width + 15, y1),
                        box_color,
                        -1
                    )
                    
                    # Text
                    cv2.putText(
                        annotated_frame,
                        label,
                        (x1 + 7, y1 - 7),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        text_color,
                        3
                    )
            
            # Add frame info overlay
            if show_timestamp:
                timestamp = current_frame / fps if fps > 0 else 0
                timestamp_str = str(timedelta(seconds=int(timestamp)))
                info_text = f"Frame: {current_frame}/{total_frames} | Time: {timestamp_str}"
                
                if last_birds_count > 0:
                    info_text += f" | Birds: {last_birds_count}"
                
                # Use PIL with same font size as species labels
                if PIL_AVAILABLE:
                    # Calculate scale factor from font_size to cv2 scale
                    cv2_scale = font_size / 30.0  # Approximate conversion
                    
                    # Use put_unicode_text for consistent styling
                    annotated_frame = put_unicode_text(
                        annotated_frame,
                        info_text,
                        (17, height - 17 - font_size),
                        font_size=font_size,
                        color=(255, 255, 255),
                        bg_color=(0, 0, 0)
                    )
                else:
                    # Fallback to OpenCV (original behavior)
                    (info_width, info_height), _ = cv2.getTextSize(
                        info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 3
                    )
                    cv2.rectangle(
                        annotated_frame,
                        (10, height - info_height - 25),
                        (info_width + 25, height - 10),
                        (0, 0, 0),
                        -1
                    )
                    
                    cv2.putText(
                        annotated_frame,
                        info_text,
                        (17, height - 17),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (255, 255, 255),
                        3
                    )
            
            # Write frame to output
            out.write(annotated_frame)
            
            # Progress indicator
            if current_frame % 100 == 0:
                progress = (current_frame / total_frames) * 100
                print(f"   Progress: {progress:.1f}% ({current_frame}/{total_frames})", end='\r')
        
        # Cleanup
        cap.release()
        out.release()
        
        print(f"\n{t('annotation_complete')}")
        print(f"{t('annotation_frames_processed').format(processed=frames_processed, total=total_frames)}")
        print(f"{t('annotation_birds_detected').format(count=total_birds_detected)}")
        
        # Try to merge audio from original video using ffmpeg
        try:
            # Check if ffmpeg is available
            subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, check=True, timeout=5)
            
            # Check if original video has audio
            probe_cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'a:0',
                '-show_entries', 'stream=codec_type',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ]
            
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
            has_audio = probe_result.stdout.strip() == 'audio'
            
            if has_audio:
                print(f"{t('annotation_merging_audio')}")
                
                # Create temporary file for video without audio
                temp_video = output_path.parent / f"{output_path.stem}_temp{output_path.suffix}"
                output_path.rename(temp_video)
                
                # Merge audio using ffmpeg
                ffmpeg_cmd = [
                    'ffmpeg', '-y',
                    '-i', str(temp_video),      # Video input (annotated, no audio)
                    '-i', str(video_path),       # Original video (with audio)
                    '-c:v', 'copy',              # Copy video stream
                    '-c:a', 'aac',               # Re-encode audio to AAC
                    '-map', '0:v:0',             # Take video from first input
                    '-map', '1:a:0',             # Take audio from second input
                    '-shortest',                 # Match shortest stream
                    str(output_path)
                ]
                
                result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    # Success - delete temp file
                    temp_video.unlink()
                    print(f"{t('annotation_audio_merged')}")
                else:
                    # Failed - restore original output
                    if temp_video.exists():
                        temp_video.rename(output_path)
                    print(f"{t('annotation_audio_failed')}")
            else:
                print(f"   ℹ️  Original video has no audio track")
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            # ffmpeg not available or failed - keep video without audio
            print(f"   ⚠️  ffmpeg not available - video saved without audio")
            print(f"   💡 Install ffmpeg to preserve audio: sudo apt install ffmpeg")
        except Exception as e:
            # Any other error - keep video without audio
            print(f"   ⚠️  Could not merge audio: {e}")
        
        return {
            'input_video': str(video_path),
            'output_video': str(output_path),
            'total_frames': total_frames,
            'frames_processed': frames_processed,
            'birds_detected': total_birds_detected,
            'fps': fps
        }
    
    def create_summary_video(self, video_path, output_path, sample_rate=5, 
                            skip_empty_seconds=3.0, min_activity_duration=2.0):
        """
        Create summary video by skipping segments without bird activity
        
        Args:
            video_path: Path to input video
            output_path: Path to output summary video
            sample_rate: Frames to skip between detections (higher = faster but less accurate)
            skip_empty_seconds: Minimum duration of bird-free segment to skip (default: 3.0)
            min_activity_duration: Minimum duration of bird activity to keep (default: 2.0)
            
        Returns:
            dict with summary statistics
        """
        video_path = Path(video_path)
        output_path = Path(output_path)
        
        print(f"\n{t('summary_analyzing')} {video_path.name}...")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_duration = total_frames / fps
        
        # Analyze video to find bird activity segments
        print(f"   📊 Analyzing {total_frames} frames at {fps:.1f} FPS...")
        
        bird_frames = set()  # Frame numbers with bird detections
        frame_number = 0
        
        while frame_number < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run detection
            results = self.model(frame, verbose=False)
            
            # Check if any birds detected
            for result in results:
                boxes = result.boxes
                if boxes is not None and len(boxes) > 0:
                    # Bird detected in this frame
                    bird_frames.add(frame_number)
                    break
            
            frame_number += sample_rate
            
            # Progress indicator
            if frame_number % (sample_rate * 100) == 0:
                progress = (frame_number / total_frames) * 100
                print(f"   ⏳ Progress: {progress:.1f}%", end='\r')
        
        cap.release()
        print(f"   ✅ Analysis complete - {len(bird_frames)} frames with birds detected")
        
        # Convert frame numbers to time segments
        skip_empty_frames = int(skip_empty_seconds * fps)
        min_activity_frames = int(min_activity_duration * fps)
        
        # Find continuous segments with bird activity
        segments = []  # [(start_time, end_time), ...]
        current_segment_start = None
        last_bird_frame = -skip_empty_frames - 1
        
        for frame_num in sorted(bird_frames):
            # Check if this frame is close enough to previous bird frame
            if frame_num - last_bird_frame <= skip_empty_frames:
                # Continue current segment
                if current_segment_start is None:
                    current_segment_start = max(0, last_bird_frame - min_activity_frames // 2)
            else:
                # End previous segment and start new one
                if current_segment_start is not None:
                    segment_end = min(total_frames, last_bird_frame + min_activity_frames // 2)
                    segment_duration = (segment_end - current_segment_start) / fps
                    if segment_duration >= min_activity_duration:
                        segments.append((current_segment_start / fps, segment_end / fps))
                
                current_segment_start = max(0, frame_num - min_activity_frames // 2)
            
            last_bird_frame = frame_num
        
        # Don't forget the last segment
        if current_segment_start is not None:
            segment_end = min(total_frames, last_bird_frame + min_activity_frames // 2)
            segment_duration = (segment_end - current_segment_start) / fps
            if segment_duration >= min_activity_duration:
                segments.append((current_segment_start / fps, segment_end / fps))
        
        if not segments:
            print(f"   ⚠️  No bird activity segments found - video would be empty")
            return {
                'input_video': str(video_path),
                'output_video': None,
                'original_duration': total_duration,
                'summary_duration': 0,
                'segments_kept': 0,
                'segments_skipped': 0,
                'compression_ratio': 0
            }
        
        summary_duration = sum(end - start for start, end in segments)
        print(f"\n{t('summary_segments_found')}")
        print(f"   📊 Segments to keep: {len(segments)}")
        print(f"   ⏱️  Original duration: {timedelta(seconds=int(total_duration))}")
        print(f"   ⏱️  Summary duration: {timedelta(seconds=int(summary_duration))}")
        print(f"   📉 Compression: {(1 - summary_duration/total_duration) * 100:.1f}% shorter")
        
        # Create ffmpeg concat file
        concat_file = output_path.parent / f"{output_path.stem}_concat.txt"
        
        try:
            print(f"\n{t('summary_creating')} {output_path.name}...")
            
            # Create temporary segment files
            temp_dir = Path(tempfile.mkdtemp())
            segment_files = []
            
            for idx, (start, end) in enumerate(segments):
                segment_path = temp_dir / f"segment_{idx:04d}.mp4"
                segment_files.append(segment_path)
                
                # Extract segment with ffmpeg (with audio)
                cmd = [
                    'ffmpeg', '-y',
                    '-ss', str(start),
                    '-i', str(video_path),
                    '-t', str(end - start),
                    '-c', 'copy',  # Copy streams without re-encoding
                    '-avoid_negative_ts', 'make_zero',
                    str(segment_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"   ⚠️  Warning: Failed to extract segment {idx}")
            
            # Create concat file
            with open(concat_file, 'w') as f:
                for seg_file in segment_files:
                    if seg_file.exists():
                        f.write(f"file '{seg_file}'\n")
            
            # Concatenate segments
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and output_path.exists():
                print(f"   {t('summary_complete')}")
                print(f"   📁 {output_path}")
                
                # Cleanup
                concat_file.unlink(missing_ok=True)
                for seg_file in segment_files:
                    seg_file.unlink(missing_ok=True)
                temp_dir.rmdir()
                
                return {
                    'input_video': str(video_path),
                    'output_video': str(output_path),
                    'original_duration': total_duration,
                    'summary_duration': summary_duration,
                    'segments_kept': len(segments),
                    'segments_skipped': total_duration - summary_duration,
                    'compression_ratio': 1 - (summary_duration / total_duration)
                }
            else:
                print(f"   ⚠️  ffmpeg concatenation failed")
                print(f"   Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  ffmpeg timeout - video too long")
            return None
        except FileNotFoundError:
            print(f"   ⚠️  ffmpeg not found - please install: sudo apt install ffmpeg")
            return None
        except Exception as e:
            print(f"   ⚠️  Error creating summary: {e}")
            return None
        finally:
            # Cleanup temp files
            if concat_file.exists():
                concat_file.unlink()
            if 'temp_dir' in locals():
                for seg_file in segment_files:
                    seg_file.unlink(missing_ok=True)
                temp_dir.rmdir()
