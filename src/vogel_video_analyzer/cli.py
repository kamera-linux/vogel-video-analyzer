"""
Command-line interface for vogel-video-analyzer
"""

import argparse
import json
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta

from . import __version__
from .analyzer import VideoAnalyzer
from .i18n import init_i18n, t


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='YOLOv8-based video analysis for bird content detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single video
  vogel-analyze video.mp4
  
  # Multiple videos
  vogel-analyze video1.mp4 video2.mp4
  
  # All MP4s in directory
  vogel-analyze ~/Videos/Birds/*/*.mp4
  
  # Custom threshold and model
  vogel-analyze --threshold 0.3 --model yolov8n.pt video.mp4
  
  # Faster analysis (every 5th frame)
  vogel-analyze --sample-rate 5 video.mp4
  
  # Save report as JSON
  vogel-analyze --output report.json video.mp4
  
  # Delete only video files with 0% bird content
  vogel-analyze --delete-file --sample-rate 5 *.mp4
  
  # Delete entire folders with 0% bird content
  vogel-analyze --delete-folder --sample-rate 5 ~/Videos/*/*.mp4
  
  # Save output to log file
  vogel-analyze --log *.mp4

For more information: https://github.com/kamera-linux/vogel-video-analyzer
        """
    )
    
    parser.add_argument('videos', nargs='+', help='Video file(s) to analyze')
    parser.add_argument('--model', default='yolov8n.pt', help='YOLO model (default: yolov8n.pt)')
    parser.add_argument('--threshold', type=float, default=0.3, help='Confidence threshold (default: 0.3)')
    parser.add_argument('--sample-rate', type=int, default=5, help='Analyze every Nth frame (default: 5)')
    parser.add_argument('--identify-species', action='store_true', help='Identify bird species (requires: pip install vogel-video-analyzer[species])')
    parser.add_argument('--species-model', default='chriamue/bird-species-classifier', 
                        help='Species classification model: Hugging Face model ID or local path (default: chriamue/bird-species-classifier)')
    parser.add_argument('--species-threshold', type=float, default=0.3,
                        help='Minimum confidence threshold for species classification (default: 0.3)')
    parser.add_argument('--multilingual', action='store_true', 
                        help='Show bird names in all available languages with flag emojis (🇬🇧 🇩🇪 🇯🇵)')
    parser.add_argument('--annotate-video', action='store_true',
                        help='Create annotated video with bounding boxes and species labels, saves as <original>_annotated.mp4 in the same directory')
    parser.add_argument('--annotate-output', metavar='PATH',
                        help='Custom output path for annotated video (requires --annotate-video)')
    parser.add_argument('--font-size', type=int, default=20,
                        help='Font size for species labels in annotated video (default: 20)')
    parser.add_argument('--flag-dir', metavar='PATH',
                        help='Directory containing flag image files (PNG/JPG). Falls back to pixel-rendered flags if not specified')
    parser.add_argument('--create-summary', action='store_true',
                        help='Create summary video by skipping segments without bird activity (v0.3.1+)')
    parser.add_argument('--summary-output', metavar='PATH',
                        help='Custom output path for summary video (requires --create-summary)')
    parser.add_argument('--skip-empty-seconds', type=float, default=3.0,
                        help='Skip segments without birds longer than N seconds (default: 3.0, requires --create-summary)')
    parser.add_argument('--min-activity-duration', type=float, default=2.0,
                        help='Minimum duration for bird activity segments in seconds (default: 2.0, requires --create-summary)')
    parser.add_argument('--output', '-o', help='Save report as JSON')
    parser.add_argument('--html-report', metavar='PATH',
                        help='Generate interactive HTML report with charts and thumbnails (v0.5.0+)')
    parser.add_argument('--max-thumbnails', type=int, default=50,
                        help='Maximum number of thumbnails in HTML report (default: 50)')
    parser.add_argument('--delete-file', action='store_true', help='Delete video files with 0%% bird content')
    parser.add_argument('--delete-folder', action='store_true', help='Delete parent folders with 0%% bird content')
    parser.add_argument('--delete', action='store_true', help='(Deprecated) Use --delete-file or --delete-folder instead')
    parser.add_argument('--log', action='store_true', help='Save console output to log file')
    parser.add_argument('--language', choices=['en', 'de', 'ja'], help='Set output language (default: auto-detect from system)')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Initialize i18n with user's language choice or auto-detect
    init_i18n(args.language)
    
    # Setup logging if requested
    log_file = None
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    if args.log:
        try:
            now = datetime.now()
            year = now.strftime('%Y')
            week = now.strftime('%V')
            timestamp = now.strftime('%Y%m%d_%H%M%S')
            
            log_dir = Path(f'/var/log/vogel-kamera-linux/{year}/KW{week}')
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file_path = log_dir / f'{timestamp}_analyze.log'
            print(f"📝 {t('log_file')} {log_file_path}\n")
            
            # Open log file and redirect stdout/stderr
            log_file = open(log_file_path, 'w', encoding='utf-8')
            
            # Create a Tee class to write to both console and file
            class Tee:
                def __init__(self, *files):
                    self.files = files
                def write(self, data):
                    for f in self.files:
                        f.write(data)
                        f.flush()
                def flush(self):
                    for f in self.files:
                        f.flush()
            
            # Redirect to both console and file
            sys.stdout = Tee(original_stdout, log_file)
            sys.stderr = Tee(original_stderr, log_file)
            
        except PermissionError:
            print(f"⚠️  {t('log_permission_denied')}", file=sys.stderr)
            print(f"   {t('log_permission_hint')}", file=sys.stderr)
            print("   sudo mkdir -p /var/log/vogel-kamera-linux && sudo chown $USER /var/log/vogel-kamera-linux", file=sys.stderr)
            return 1
    
    # Check species dependencies if requested
    if args.identify_species:
        try:
            from .species_classifier import SPECIES_AVAILABLE
            if not SPECIES_AVAILABLE:
                print(f"❌ {t('species_dependencies_missing')}", file=sys.stderr)
                print(f"   pip install vogel-video-analyzer[species]", file=sys.stderr)
                return 1
        except ImportError:
            print(f"❌ {t('species_dependencies_missing')}", file=sys.stderr)
            print(f"   pip install vogel-video-analyzer[species]", file=sys.stderr)
            return 1
    
    try:
        # Initialize analyzer
        analyzer = VideoAnalyzer(
            model_path=args.model,
            threshold=args.threshold,
            identify_species=args.identify_species,
            species_model=args.species_model,
            species_threshold=args.species_threshold
        )
        
        # Analyze videos
        all_stats = []
        for video_path in args.videos:
            try:
                # Create annotated video if requested
                if args.annotate_video:
                    # Determine output path
                    if args.annotate_output:
                        # Use custom output path (only for single video)
                        if len(args.videos) > 1:
                            print(f"\n⚠️  {t('annotation_multiple_custom_path')}: {video_path}")
                            print(f"    {t('annotation_using_auto_path')}")
                            video_path_obj = Path(video_path)
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            output_path = video_path_obj.parent / f"{video_path_obj.stem}_annotated_{timestamp}{video_path_obj.suffix}"
                        else:
                            output_path = args.annotate_output
                    else:
                        # Auto-generate output filename with timestamp in same directory
                        video_path_obj = Path(video_path)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        output_path = video_path_obj.parent / f"{video_path_obj.stem}_annotated_{timestamp}{video_path_obj.suffix}"
                    
                    annotation_stats = analyzer.annotate_video(
                        video_path, 
                        str(output_path), 
                        sample_rate=args.sample_rate,
                        multilingual=args.multilingual,
                        font_size=args.font_size,
                        flag_dir=args.flag_dir  # Pass flag directory for hybrid rendering
                    )
                elif args.create_summary:
                    # Create summary video (skip empty segments)
                    # Determine output path
                    if args.summary_output:
                        # Use custom output path (only for single video)
                        if len(args.videos) > 1:
                            print(f"\n⚠️  {t('summary_multiple_custom_path')}: {video_path}")
                            print(f"    {t('summary_using_auto_path')}")
                            video_path_obj = Path(video_path)
                            output_path = video_path_obj.parent / f"{video_path_obj.stem}_summary{video_path_obj.suffix}"
                        else:
                            output_path = args.summary_output
                    else:
                        # Auto-generate output filename in same directory
                        video_path_obj = Path(video_path)
                        output_path = video_path_obj.parent / f"{video_path_obj.stem}_summary{video_path_obj.suffix}"
                    
                    summary_stats = analyzer.create_summary_video(
                        video_path,
                        str(output_path),
                        sample_rate=args.sample_rate,
                        skip_empty_seconds=args.skip_empty_seconds,
                        min_activity_duration=args.min_activity_duration
                    )
                else:
                    # Standard analysis
                    stats = analyzer.analyze_video(video_path, sample_rate=args.sample_rate)
                    analyzer.print_report(stats)
                    all_stats.append(stats)
            except Exception as e:
                print(f"❌ {t('error_analyzing')} {video_path}: {e}", file=sys.stderr)
                continue
        
        # Summary for multiple videos
        if len(all_stats) > 1:
            _print_summary(all_stats)
        
        # Auto-delete feature (with deprecation warning)
        if args.delete:
            print(f"\n⚠️  {t('delete_deprecated')}", file=sys.stderr)
            print(f"   {t('delete_deprecated_hint')}\n", file=sys.stderr)
            args.delete_folder = True
        
        if args.delete_file and all_stats:
            _delete_empty_video_files(all_stats)
        elif args.delete_folder and all_stats:
            _delete_empty_video_folders(all_stats)
        
        # JSON output
        if args.output:
            _save_json_output(all_stats, args.output)
        
        # HTML report generation
        if args.html_report and all_stats:
            _generate_html_report(all_stats, args.html_report, args.max_thumbnails)
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  {t('analysis_interrupted')}")
        return 1
    except Exception as e:
        print(f"\n❌ {t('error')}: {e}", file=sys.stderr)
        return 1
    finally:
        # Restore stdout/stderr and close log file
        if log_file:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            log_file.close()


def _print_summary(all_stats):
    """Print summary for multiple videos"""
    total_videos = len(all_stats)
    total_duration = sum(s['duration_seconds'] for s in all_stats)
    avg_bird_percentage = sum(s['bird_percentage'] for s in all_stats) / total_videos
    total_frames_analyzed = sum(s['frames_analyzed'] for s in all_stats)
    total_frames_with_birds = sum(s['frames_with_birds'] for s in all_stats)
    
    print("\n" + "=" * 70)
    print(f"📊 {t('summary_title').format(count=total_videos)}")
    print("=" * 70)
    print(f"   {t('summary_total_duration')} {timedelta(seconds=int(total_duration))}")
    print(f"   {t('summary_total_frames')} {total_frames_analyzed}")
    print(f"   {t('summary_bird_frames')} {total_frames_with_birds}")
    print(f"   {t('summary_avg_bird')} {avg_bird_percentage:.1f}%")
    
    print(f"\n📋 {t('summary_overview')}")
    print(f"   {'Nr.':<4} {t('summary_directory'):<70} {t('summary_bird'):<6} {t('summary_bird_pct'):<8} {t('summary_frames'):<12} {t('summary_duration'):<8}")
    print(f"   {'-'*4} {'-'*70} {'-'*6} {'-'*8} {'-'*12} {'-'*8}")
    
    for i, stats in enumerate(all_stats, 1):
        video_path = Path(stats['video_path'])
        directory_name = video_path.parent.name
        status = "✅" if stats['frames_with_birds'] > 0 else "❌"
        bird_pct = f"{stats['bird_percentage']:.1f}%"
        frames_info = f"{stats['frames_with_birds']}/{stats['frames_analyzed']}"
        duration = f"{int(stats['duration_seconds'])}s"
        
        print(f"   {i:<4} {directory_name:<70} {status:<6} {bird_pct:<8} {frames_info:<12} {duration:<8}")
    
    print("=" * 70)


def _delete_empty_videos(all_stats):
    """Delete directories with 0% bird content (deprecated, kept for compatibility)"""
    _delete_empty_video_folders(all_stats)


def _delete_empty_video_files(all_stats):
    """Delete video files with 0% bird content"""
    videos_to_delete = [s for s in all_stats if s['bird_percentage'] == 0.0]
    
    if videos_to_delete:
        print("\n" + "=" * 70)
        print(f"🗑️  {t('delete_files_title').format(count=len(videos_to_delete))}")
        print("=" * 70)
        
        for stats in videos_to_delete:
            video_path = Path(stats['video_path'])
            
            try:
                print(f"   🗑️  {t('deleting')} {video_path.name}")
                video_path.unlink()
                print(f"      ✅ {t('delete_success')}")
            except Exception as e:
                print(f"      ❌ {t('delete_error')} {e}")
                
        print(f"\n   {t('deleted_files')} {len(videos_to_delete)}")
        print(f"   {t('remaining_videos')} {len(all_stats) - len(videos_to_delete)}")
        print("=" * 70)
    else:
        print(f"\n✅ {t('no_empty_files')}")


def _delete_empty_video_folders(all_stats):
    """Delete parent folders with 0% bird content"""
    videos_to_delete = [s for s in all_stats if s['bird_percentage'] == 0.0]
    
    if videos_to_delete:
        print("\n" + "=" * 70)
        print(f"🗑️  {t('delete_folders_title').format(count=len(videos_to_delete))}")
        print("=" * 70)
        
        for stats in videos_to_delete:
            video_path = Path(stats['video_path'])
            directory = video_path.parent
            
            try:
                print(f"   🗑️  {t('deleting_folder')} {directory.name}")
                shutil.rmtree(directory)
                print(f"      ✅ {t('delete_success')}")
            except Exception as e:
                print(f"      ❌ {t('delete_error')} {e}")
                
        print(f"\n   {t('deleted_folders')} {len(videos_to_delete)}")
        print(f"   {t('remaining_videos')} {len(all_stats) - len(videos_to_delete)}")
        print("=" * 70)
    else:
        print(f"\n✅ {t('no_empty_folders')}")


def _save_json_output(all_stats, output_path):
    """Save report as JSON"""
    output_data = all_stats[0] if len(all_stats) == 1 else {
        'videos': all_stats,
        'summary': {
            'total_videos': len(all_stats),
            'total_duration': sum(s['duration_seconds'] for s in all_stats),
            'average_bird_percentage': sum(s['bird_percentage'] for s in all_stats) / len(all_stats)
        }
    }
    
    output_path = Path(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 {t('report_saved')} {output_path}")


def _generate_html_report(all_stats, output_path, max_thumbnails):
    """Generate interactive HTML report"""
    try:
        from .reporter import HTMLReporter
        
        # For now, only support single video reports
        # Multi-video reports could be a future enhancement
        if len(all_stats) > 1:
            print(f"\n⚠️  {t('html_single_only')}")
            print(f"    {t('html_processing_first')} {all_stats[0]['video_path']}")
        
        stats = all_stats[0]
        video_path = stats['video_path']
        
        print(f"\n📊 {t('html_generating')}")
        reporter = HTMLReporter(stats, video_path)
        reporter.generate_report(output_path, max_thumbnails=max_thumbnails)
        print(f"✅ {t('html_success')} {output_path}")
        
    except ImportError as e:
        print(f"❌ {t('html_error')} {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ {t('html_error')} {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()



if __name__ == '__main__':
    sys.exit(main())
