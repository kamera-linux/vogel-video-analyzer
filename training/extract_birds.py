#!/usr/bin/env python3
"""
Script to extract bird crops from videos for training data collection.
Extracts detected birds and saves them as individual images.
"""

import cv2
import argparse
from pathlib import Path
from ultralytics import YOLO
import sys

def extract_birds_from_video(video_path, output_dir, model_path="yolov8n.pt", 
                             threshold=0.3, sample_rate=5, target_class=14):
    """
    Extract bird crops from video and save as images
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save extracted bird images
        model_path: YOLO model path
        threshold: Detection confidence threshold
        sample_rate: Analyze every Nth frame
        target_class: COCO class for bird (14)
    """
    # Load YOLO model
    print(f"🤖 Loading YOLO model: {model_path}")
    model = YOLO(model_path)
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"📹 Video: {Path(video_path).name}")
    print(f"   📊 {total_frames} frames, {fps:.1f} FPS")
    print(f"   🔍 Analyzing every {sample_rate}. frame...")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    bird_count = 0
    frame_num = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Only process every Nth frame
            if frame_num % sample_rate != 0:
                frame_num += 1
                continue
            
            # Run detection
            results = model(frame, verbose=False)
            
            # Extract birds
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Check if it's a bird with sufficient confidence
                    if cls == target_class and conf >= threshold:
                        # Get bounding box
                        xyxy = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                        
                        # Ensure coordinates are within frame
                        h, w = frame.shape[:2]
                        x1, y1 = max(0, x1), max(0, y1)
                        x2, y2 = min(w, x2), min(h, y2)
                        
                        # Crop bird
                        bird_crop = frame[y1:y2, x1:x2]
                        
                        if bird_crop.size > 0:
                            # Save crop
                            bird_count += 1
                            filename = f"bird_{frame_num:06d}_{bird_count:04d}_conf{conf:.2f}.jpg"
                            save_path = output_path / filename
                            cv2.imwrite(str(save_path), bird_crop)
                            
                            print(f"   ✅ Extracted bird #{bird_count}: frame {frame_num}, conf {conf:.2f}")
            
            frame_num += 1
            
            # Progress
            if frame_num % 100 == 0:
                progress = (frame_num / total_frames) * 100
                print(f"   ⏳ Progress: {progress:.1f}% ({frame_num}/{total_frames} frames)")
    
    except KeyboardInterrupt:
        print("\n⚠️  Extraction interrupted by user")
    
    finally:
        cap.release()
    
    print(f"\n✅ Extraction complete!")
    print(f"   📁 Output directory: {output_path}")
    print(f"   🐦 Total birds extracted: {bird_count}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review extracted images in: {output_path}")
    print(f"   2. Create subdirectories for each species (e.g., kohlmeise/, amsel/, etc.)")
    print(f"   3. Move images into correct species folders")
    print(f"   4. Use this dataset to train a custom model!")


def main():
    parser = argparse.ArgumentParser(
        description='Extract bird crops from videos for training data collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract birds from single video
  python extract_birds.py video.mp4 -o training_data/

  # Extract with custom threshold and sample rate
  python extract_birds.py video.mp4 -o data/ --threshold 0.4 --sample-rate 10

  # Process multiple videos
  for video in *.mp4; do python extract_birds.py "$video" -o data/; done
        """
    )
    
    parser.add_argument('video', help='Video file to process')
    parser.add_argument('-o', '--output', required=True, help='Output directory for bird images')
    parser.add_argument('--model', default='yolov8n.pt', help='YOLO model path (default: yolov8n.pt)')
    parser.add_argument('--threshold', type=float, default=0.3, help='Detection confidence threshold (default: 0.3)')
    parser.add_argument('--sample-rate', type=int, default=5, help='Analyze every Nth frame (default: 5)')
    
    args = parser.parse_args()
    
    # Check if video exists
    if not Path(args.video).exists():
        print(f"❌ Video file not found: {args.video}")
        sys.exit(1)
    
    extract_birds_from_video(
        video_path=args.video,
        output_dir=args.output,
        model_path=args.model,
        threshold=args.threshold,
        sample_rate=args.sample_rate
    )


if __name__ == '__main__':
    main()
