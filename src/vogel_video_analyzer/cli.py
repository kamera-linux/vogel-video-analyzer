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

# File extensions treated as videos when checking folders before deletion
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm', '.h264', '.mjpeg', '.mjpg'}


class Tee:
    """Write to several streams at once (console + log file).

    Implements the parts of the io.TextIOBase API that third-party libraries
    (ultralytics, tqdm, transformers) commonly query on sys.stdout/sys.stderr.
    The first stream is treated as the primary (console) stream.
    """

    def __init__(self, *files):
        self.files = files
        self._primary = files[0]

    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush()
        return len(data)

    def flush(self):
        for f in self.files:
            f.flush()

    def isatty(self):
        try:
            return self._primary.isatty()
        except Exception:
            return False

    def fileno(self):
        return self._primary.fileno()

    @property
    def encoding(self):
        return getattr(self._primary, 'encoding', 'utf-8')

    def __getattr__(self, name):
        # Delegate everything else (errors, buffer, ...) to the console stream
        return getattr(self._primary, name)


def _positive_int(value):
    """argparse type: integer >= 1"""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}")
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"must be >= 1, got {ivalue}")
    return ivalue


def _probability(value):
    """argparse type: float in [0.0, 1.0]"""
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid float value: {value!r}")
    if not 0.0 <= fvalue <= 1.0:
        raise argparse.ArgumentTypeError(f"must be between 0.0 and 1.0, got {fvalue}")
    return fvalue


def _non_negative_float(value):
    """argparse type: float >= 0"""
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid float value: {value!r}")
    if fvalue < 0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {fvalue}")
    return fvalue


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='YOLOv26-based video analysis for bird content detection',
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
  vogel-analyze --threshold 0.3 --model yolo26n.pt video.mp4
  
  # Faster analysis (every 5th frame)
  vogel-analyze --sample-rate 5 video.mp4
  
  # Save report as JSON
  vogel-analyze --output report.json video.mp4
  
  # Delete only video files with 0% bird content
  vogel-analyze --delete-file --sample-rate 5 *.mp4
  
  # Delete entire folders with 0% bird content
  vogel-analyze --delete-folder --sample-rate 5 ~/Videos/*/*.mp4

  # Preview what would be deleted without deleting anything
  vogel-analyze --delete-folder --dry-run ~/Videos/*/*.mp4

  # Save output to log file
  vogel-analyze --log *.mp4

For more information: https://github.com/kamera-linux/vogel-video-analyzer
        """
    )
    
    parser.add_argument('videos', nargs='*', help='Video file(s) to analyze')
    parser.add_argument('--model', default='yolo26n.pt', help='YOLO model (default: yolo26n.pt)')
    parser.add_argument('--threshold', type=_probability, default=0.3, help='Confidence threshold 0.0-1.0 (default: 0.3)')
    parser.add_argument('--sample-rate', type=_positive_int, default=5, help='Analyze every Nth frame, >= 1 (default: 5)')
    parser.add_argument('--identify-species', action='store_true', help='Identify bird species (requires: pip install vogel-video-analyzer[species])')
    parser.add_argument('--species-model', default='chriamue/bird-species-classifier', 
                        help='Species classification model: Hugging Face model ID or local path (default: chriamue/bird-species-classifier)')
    parser.add_argument('--species-threshold', type=_probability, default=0.3,
                        help='Minimum confidence threshold for species classification (default: 0.3)')
    parser.add_argument('--multilingual', action='store_true', 
                        help='Show bird names in all available languages with flag emojis (🇬🇧 🇩🇪 🇯🇵)')
    parser.add_argument('--annotate-video', action='store_true',
                        help='Create annotated video with bounding boxes and species labels, saves as <original>_annotated.mp4 in the same directory')
    parser.add_argument('--annotate-output', metavar='PATH',
                        help='Custom output path for annotated video (requires --annotate-video)')
    parser.add_argument('--font-size', type=_positive_int, default=20,
                        help='Font size for species labels in annotated video (default: 20)')
    parser.add_argument('--flag-dir', metavar='PATH',
                        help='Directory containing flag image files (PNG/JPG). Falls back to pixel-rendered flags if not specified')
    parser.add_argument('--create-summary', action='store_true',
                        help='Create summary video by skipping segments without bird activity (v0.3.1+)')
    parser.add_argument('--summary-output', metavar='PATH',
                        help='Custom output path for summary video (requires --create-summary)')
    parser.add_argument('--skip-empty-seconds', type=_non_negative_float, default=3.0,
                        help='Skip segments without birds longer than N seconds (default: 3.0, requires --create-summary)')
    parser.add_argument('--min-activity-duration', type=_non_negative_float, default=2.0,
                        help='Minimum duration for bird activity segments in seconds (default: 2.0, requires --create-summary)')
    parser.add_argument('--output', '-o', help='Save report as JSON')
    parser.add_argument('--html-report', metavar='PATH',
                        help='Generate interactive HTML report with charts and thumbnails (v0.5.0+)')
    parser.add_argument('--max-thumbnails', type=_positive_int, default=50,
                        help='Maximum number of thumbnails in HTML report (default: 50)')
    parser.add_argument('--delete-file', action='store_true', help='Delete video files with 0%% bird content')
    parser.add_argument('--delete-folder', action='store_true',
                        help='Delete parent folders with 0%% bird content. A folder is only deleted if every '
                             'video in it was analyzed and none contains birds; the current directory, '
                             'home directory and filesystem root are never deleted')
    parser.add_argument('--dry-run', action='store_true',
                        help='With --delete-file/--delete-folder: only show what would be deleted')
    parser.add_argument('--delete', action='store_true', help='(Deprecated) Use --delete-file or --delete-folder instead')
    parser.add_argument('--log', action='store_true', help='Save console output to log file')
    parser.add_argument('--language', choices=['en', 'de', 'ja'], help='Set output language (default: auto-detect from system)')
    parser.add_argument('--engine', choices=['auto', 'hailo'], default='auto',
                        help='Inference backend: "auto" uses ultralytics/CPU/GPU (default), '
                             '"hailo" uses Raspberry Pi AI HAT+ (Hailo-8 NPU)')
    parser.add_argument('--hef-model', metavar='PATH',
                        help='Path to HEF model file for Hailo NPU (required with --engine hailo). '
                             'Download from https://github.com/hailo-ai/hailo_model_zoo')
    parser.add_argument('--hailo-num-classes', type=_positive_int, default=80, metavar='N',
                        help='Number of output classes in the HEF model (default: 80 for COCO). '
                             'Use 1 if HEF was compiled from a single-class bird model.')
    parser.add_argument('--export-onnx', metavar='MODEL_PATH',
                        help='Export a YOLO .pt model to ONNX format (first step for Hailo HEF '
                             'compilation). Example: --export-onnx yolov26n.pt')
    parser.add_argument('--export-onnx-output', metavar='PATH',
                        help='Output path for the exported ONNX file (optional, default: same '
                             'directory as the .pt file)')
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
                print("   pip install vogel-video-analyzer[species]", file=sys.stderr)
                return 1
        except ImportError:
            print(f"❌ {t('species_dependencies_missing')}", file=sys.stderr)
            print("   pip install vogel-video-analyzer[species]", file=sys.stderr)
            return 1
    
    try:
        # Handle --export-onnx before initialising the analyzer
        if args.export_onnx:
            from .hailo_engine import export_to_onnx
            export_to_onnx(args.export_onnx, output_path=args.export_onnx_output)
            return 0

        if not args.videos:
            parser.error('the following arguments are required: videos')

        # Initialize analyzer
        analyzer = VideoAnalyzer(
            model_path=args.model,
            threshold=args.threshold,
            identify_species=args.identify_species,
            species_model=args.species_model,
            species_threshold=args.species_threshold,
            engine=args.engine,
            hef_model=args.hef_model,
            hailo_num_classes=args.hailo_num_classes,
        )
        
        # Analyze videos
        all_stats = []
        failed_videos = 0
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
                    
                    analyzer.annotate_video(
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
                    
                    analyzer.create_summary_video(
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
                failed_videos += 1
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
            _delete_empty_video_files(all_stats, dry_run=args.dry_run)
        elif args.delete_folder and all_stats:
            _delete_empty_video_folders(all_stats, dry_run=args.dry_run)
        
        # JSON output
        if args.output:
            _save_json_output(all_stats, args.output)
        
        # HTML report generation
        if args.html_report and all_stats:
            _generate_html_report(all_stats, args.html_report, args.max_thumbnails)
        
        # Non-zero exit code if at least one video could not be processed
        return 1 if failed_videos else 0
        
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


def _is_empty_result(stats):
    """True if a video was actually analyzed (>= 1 frame) and contains no birds.

    Videos from which no frame could be read are NOT considered empty, so a
    corrupted or unreadable file is never deleted by accident.
    """
    return stats.get('frames_analyzed', 0) > 0 and stats.get('frames_with_birds', 0) == 0


def _is_protected_directory(directory):
    """Directories that must never be deleted by --delete-folder."""
    directory = Path(directory).resolve()
    cwd = Path.cwd().resolve()
    home = Path.home().resolve()
    if directory.parent == directory:  # filesystem root
        return True
    if directory == cwd or directory in cwd.parents:
        return True
    if directory == home or directory in home.parents:
        return True
    return False


def _plan_file_deletion(all_stats):
    """Return (files_to_delete, skipped) where skipped is a list of (path, reason_key)."""
    to_delete = []
    skipped = []
    for stats in all_stats:
        video_path = Path(stats['video_path'])
        if _is_empty_result(stats):
            to_delete.append(video_path)
        elif stats.get('frames_analyzed', 0) == 0:
            skipped.append((video_path, 'delete_skip_unreadable'))
    return to_delete, skipped


def _plan_folder_deletion(all_stats):
    """Return (folders_to_delete, skipped) where skipped is a list of (path, reason_key).

    A folder is only deleted if
      * at least one analyzed video in it is empty,
      * no analyzed video in it contains birds or was unreadable,
      * it contains no other (not analyzed) video files, and
      * it is not a protected directory (cwd and its parents, home and its parents, root).
    """
    folders = {}
    for stats in all_stats:
        directory = Path(stats['video_path']).resolve().parent
        folders.setdefault(directory, []).append(stats)

    to_delete = []
    skipped = []
    for directory, folder_stats in folders.items():
        if not any(_is_empty_result(s) for s in folder_stats):
            continue  # nothing to delete in this folder

        if any(s.get('frames_with_birds', 0) > 0 for s in folder_stats):
            skipped.append((directory, 'delete_skip_mixed'))
            continue
        if any(s.get('frames_analyzed', 0) == 0 for s in folder_stats):
            skipped.append((directory, 'delete_skip_unreadable'))
            continue
        if _is_protected_directory(directory):
            skipped.append((directory, 'delete_skip_protected'))
            continue

        analyzed = {Path(s['video_path']).resolve() for s in folder_stats}
        try:
            other_videos = [
                p for p in directory.iterdir()
                if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS and p.resolve() not in analyzed
            ]
        except OSError:
            other_videos = []
        if other_videos:
            skipped.append((directory, 'delete_skip_unanalyzed'))
            continue

        to_delete.append(directory)
    return to_delete, skipped


def _print_skipped(skipped):
    for path, reason_key in skipped:
        print(f"   ⏭️  {t('delete_skipped')} {path}: {t(reason_key)}")


def _delete_empty_videos(all_stats):
    """Delete directories with 0% bird content (deprecated, kept for compatibility)"""
    _delete_empty_video_folders(all_stats)


def _delete_empty_video_files(all_stats, dry_run=False):
    """Delete video files with 0% bird content"""
    videos_to_delete, skipped = _plan_file_deletion(all_stats)

    if videos_to_delete or skipped:
        print("\n" + "=" * 70)
        print(f"🗑️  {t('delete_files_title').format(count=len(videos_to_delete))}")
        if dry_run:
            print(f"   {t('delete_dry_run_hint')}")
        print("=" * 70)

        deleted = 0
        for video_path in videos_to_delete:
            if dry_run:
                print(f"   🔎 {t('delete_would_delete')} {video_path}")
                continue
            try:
                print(f"   🗑️  {t('deleting')} {video_path.name}")
                video_path.unlink()
                deleted += 1
                print(f"      ✅ {t('delete_success')}")
            except Exception as e:
                print(f"      ❌ {t('delete_error')} {e}")

        _print_skipped(skipped)

        if not dry_run:
            print(f"\n   {t('deleted_files')} {deleted}")
            print(f"   {t('remaining_videos')} {len(all_stats) - deleted}")
        print("=" * 70)
    else:
        print(f"\n✅ {t('no_empty_files')}")


def _delete_empty_video_folders(all_stats, dry_run=False):
    """Delete parent folders with 0% bird content"""
    folders_to_delete, skipped = _plan_folder_deletion(all_stats)

    if folders_to_delete or skipped:
        print("\n" + "=" * 70)
        print(f"🗑️  {t('delete_folders_title').format(count=len(folders_to_delete))}")
        if dry_run:
            print(f"   {t('delete_dry_run_hint')}")
        print("=" * 70)

        deleted = 0
        for directory in folders_to_delete:
            if dry_run:
                print(f"   🔎 {t('delete_would_delete')} {directory}")
                continue
            try:
                print(f"   🗑️  {t('deleting_folder')} {directory.name}")
                shutil.rmtree(directory)
                deleted += 1
                print(f"      ✅ {t('delete_success')}")
            except Exception as e:
                print(f"      ❌ {t('delete_error')} {e}")

        _print_skipped(skipped)

        if not dry_run:
            print(f"\n   {t('deleted_folders')} {deleted}")
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
