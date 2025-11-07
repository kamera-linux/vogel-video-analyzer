"""
Video analyzer core module for bird detection in videos using YOLOv8
"""

import cv2
from pathlib import Path
from datetime import timedelta
from ultralytics import YOLO
from .i18n import t


class VideoAnalyzer:
    """Analyzes videos for bird content using YOLOv8"""
    
    def __init__(self, model_path="yolov8n.pt", threshold=0.3, target_class=14):
        """
        Initialize the analyzer
        
        Args:
            model_path: Path to YOLO model (searches: models/, config/models/, current dir, auto-download)
            threshold: Confidence threshold (0.0-1.0), default 0.3 for bird detection
            target_class: COCO class for bird (14=bird)
        """
        model_path = self._find_model(model_path)
        print(f"🤖 {t('loading_model')} {model_path}")
        self.model = YOLO(model_path)
        self.threshold = threshold
        self.target_class = target_class
    
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
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    if cls == self.target_class and conf >= self.threshold:
                        birds_in_frame += 1
                        
            if birds_in_frame > 0:
                frames_with_birds += 1
                timestamp = current_frame / fps if fps > 0 else 0
                bird_detections.append({
                    'frame': current_frame,
                    'timestamp': timestamp,
                    'birds': birds_in_frame
                })
                
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
            'threshold': self.threshold,
            'model': str(self.model.ckpt_path if hasattr(self.model, 'ckpt_path') else 'unknown')
        }
        
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
        
        print("━" * 70)
