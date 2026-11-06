"""
Tests for the analysis pipeline (segments, summary video, annotation, flags)
using synthetic videos and a fake YOLO model.
"""

import shutil
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest

from vogel_video_analyzer import analyzer as analyzer_module
from vogel_video_analyzer.analyzer import (
    COCO_CLASS_BIRD,
    VideoAnalyzer,
    compute_output_frame_step,
    compute_summary_segments,
    put_unicode_text,
    render_emoji_icon,
    render_flag_icon,
)

from conftest import FakeModel, make_analyzer

PERSON = 0
BIRD = COCO_CLASS_BIRD


# ── _find_bird_segments ──────────────────────────────────────────────────────

def _detections(timestamps):
    return [{'frame': i, 'timestamp': ts, 'birds': 1} for i, ts in enumerate(timestamps)]


def test_segments_split_at_gap_larger_than_two_seconds():
    analyzer = make_analyzer(model=None)
    # fps=30, sample_rate=5 -> sample interval 0.17s, so max gap = 2.0s
    segments = analyzer._find_bird_segments(_detections([0.0, 1.0, 2.5, 6.0, 7.0]), 30.0, 5)
    assert [(s['start'], s['end'], s['detections']) for s in segments] == [
        (0.0, 2.5, 3),
        (6.0, 7.0, 2),
    ]


def test_segments_max_gap_is_not_scaled_with_sample_rate():
    """Regression: max_gap used to be 2.0 * sample_rate seconds (10s for sample_rate=5)."""
    analyzer = make_analyzer(model=None)
    segments = analyzer._find_bird_segments(_detections([0.0, 5.0]), 30.0, 5)
    assert len(segments) == 2


def test_segments_join_consecutive_samples_with_long_sampling_interval():
    """With sample_rate=90 at 30 FPS samples are 3s apart and must still be joined."""
    analyzer = make_analyzer(model=None)
    segments = analyzer._find_bird_segments(_detections([0.0, 3.0, 6.0]), 30.0, 90)
    assert len(segments) == 1


def test_segments_empty():
    assert make_analyzer(model=None)._find_bird_segments([], 30.0, 5) == []


# ── compute_summary_segments ─────────────────────────────────────────────────

def test_summary_segments_merge_and_pad():
    # 10 fps, skip gaps > 3s (30 frames), pad 1s (min 2s -> 20 frames // 2 = 10)
    segments = compute_summary_segments({50, 60, 70, 200}, total_frames=300, fps=10.0,
                                        skip_empty_seconds=3.0, min_activity_duration=2.0)
    assert segments == [(4.0, 8.0), (19.0, 21.0)]


def test_summary_segments_clipped_short_segment_is_dropped():
    # Single detection at frame 0: padding is clipped at the video start -> only 1s long
    assert compute_summary_segments({0}, total_frames=300, fps=10.0) == []


def test_summary_segments_empty_and_invalid_fps():
    assert compute_summary_segments(set(), 100, 10.0) == []
    with pytest.raises(ValueError):
        compute_summary_segments({1}, 100, 0)


# ── compute_output_frame_step ────────────────────────────────────────────────

@pytest.mark.parametrize("fps, step, out_fps", [
    (25.0, 1, 25.0),
    (60.0, 1, 60.0),
    (120.0, 2, 60.0),
    (100.0, 2, 50.0),
    (240.0, 4, 60.0),
])
def test_output_frame_step(fps, step, out_fps):
    assert compute_output_frame_step(fps) == (step, pytest.approx(out_fps))


# ── analyze_video ────────────────────────────────────────────────────────────

def test_analyze_video_counts_only_birds_above_threshold(video_factory):
    video = video_factory(frames=20)
    # sample_rate=1 -> 20 calls; birds in calls 0-4, person in 5-9, weak bird in 10-14
    def dets(i):
        if i < 5:
            return [(BIRD, 0.9)]
        if i < 10:
            return [(PERSON, 0.9)]
        if i < 15:
            return [(BIRD, 0.1)]
        return []
    analyzer = make_analyzer(FakeModel(dets))
    stats = analyzer.analyze_video(video, sample_rate=1)
    assert stats['frames_analyzed'] == 20
    assert stats['frames_with_birds'] == 5
    assert stats['bird_percentage'] == pytest.approx(25.0)
    # frame numbers are 1-based
    assert [d['frame'] for d in stats['detections']] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("sample_rate", [0, -1, 1.5])
def test_analyze_video_rejects_invalid_sample_rate(video_factory, sample_rate):
    analyzer = make_analyzer(FakeModel(lambda i: []))
    with pytest.raises(ValueError):
        analyzer.analyze_video(video_factory(), sample_rate=sample_rate)


def test_constructor_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        VideoAnalyzer(threshold=1.5)


def test_hailo_engine_receives_num_classes_and_single_class_target(monkeypatch, tmp_path):
    """Regression: --hailo-num-classes was ignored; 1-class models use class ID 0."""
    hef = tmp_path / "model.hef"
    hef.write_bytes(b"x")
    captured = {}

    class DummyDetector:
        def __init__(self, path, num_classes=80):
            captured['num_classes'] = num_classes

    monkeypatch.setattr(analyzer_module, 'HAILO_AVAILABLE', True)
    monkeypatch.setattr(analyzer_module, 'HailoDetector', DummyDetector)

    analyzer = VideoAnalyzer(engine="hailo", hef_model=str(hef), hailo_num_classes=1)
    assert captured['num_classes'] == 1
    assert analyzer.target_class == 0

    analyzer = VideoAnalyzer(engine="hailo", hef_model=str(hef), hailo_num_classes=80)
    assert captured['num_classes'] == 80
    assert analyzer.target_class == COCO_CLASS_BIRD


def test_default_species_model_matches_cli():
    import inspect
    from vogel_video_analyzer.species_classifier import BirdSpeciesClassifier
    analyzer_default = inspect.signature(VideoAnalyzer.__init__).parameters['species_model'].default
    classifier_default = inspect.signature(BirdSpeciesClassifier.__init__).parameters['model_name'].default
    assert analyzer_default == classifier_default == "chriamue/bird-species-classifier"


# ── create_summary_video ─────────────────────────────────────────────────────

def test_summary_ignores_non_bird_detections(video_factory, tmp_path):
    """Regression: any detection (person, car, ...) used to count as bird activity."""
    video = video_factory(frames=40, fps=10.0)
    analyzer = make_analyzer(FakeModel(lambda i: [(PERSON, 0.99), (BIRD, 0.1)]))
    result = analyzer.create_summary_video(video, tmp_path / "summary.mp4", sample_rate=2)
    assert result['output_video'] is None
    assert result['segments_kept'] == 0


@pytest.mark.skipif(shutil.which('ffmpeg') is None, reason="ffmpeg not installed")
def test_summary_success_returns_stats_and_cleans_up(video_factory, tmp_path):
    """Regression: a successful summary raised FileNotFoundError (temp dir removed twice)."""
    video = video_factory(frames=60, fps=10.0)
    # birds in the first 30 frames only
    model = FakeModel(lambda i: [(BIRD, 0.9)] if i < 15 else [])
    analyzer = make_analyzer(model)
    output = tmp_path / "summary.mp4"
    before = set(Path(tempfile.gettempdir()).glob('vogel_summary_*'))

    result = analyzer.create_summary_video(video, output, sample_rate=2,
                                           skip_empty_seconds=1.0, min_activity_duration=1.0)

    assert result is not None
    assert result['output_video'] == str(output)
    assert result['segments_kept'] == 1
    assert output.exists()
    assert set(Path(tempfile.gettempdir()).glob('vogel_summary_*')) == before
    assert not list(tmp_path.glob('*_concat.txt'))


def test_summary_reads_frames_sequentially(video_factory, tmp_path):
    video = video_factory(frames=30)
    model = FakeModel(lambda i: [])
    make_analyzer(model).create_summary_video(video, tmp_path / "s.mp4", sample_rate=3)
    assert model.calls == 10  # frames 0, 3, ..., 27


# ── annotate_video ───────────────────────────────────────────────────────────

def test_annotate_high_fps_keeps_realtime_speed(video_factory, tmp_path, monkeypatch):
    """Regression: >60 FPS videos were written at 30 FPS with all frames (slow motion)."""
    monkeypatch.setattr(analyzer_module.subprocess, 'run', _no_ffmpeg)
    video = video_factory(frames=60, fps=120.0)
    analyzer = make_analyzer(FakeModel(lambda i: [(BIRD, 0.9)]))
    out = tmp_path / "annotated.mp4"
    stats = analyzer.annotate_video(video, out, sample_rate=1)

    cap = cv2.VideoCapture(stats['output_video'])
    out_fps = cap.get(cv2.CAP_PROP_FPS)
    out_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    assert stats['output_fps'] == pytest.approx(60.0)
    assert out_fps == pytest.approx(60.0, abs=0.5)
    assert out_frames == 30
    # duration unchanged: 60 frames @ 120 fps == 30 frames @ 60 fps
    assert out_frames / out_fps == pytest.approx(60 / 120.0, abs=0.05)
    assert stats['birds_detected'] == 60


def _no_ffmpeg(*args, **kwargs):
    raise FileNotFoundError("ffmpeg")


# ── put_unicode_text / flags ─────────────────────────────────────────────────

def test_put_unicode_text_draws_without_modifying_input():
    img = np.zeros((60, 200, 3), dtype=np.uint8)
    result = put_unicode_text(img, "Kohlmeise シジュウカラ", (5, 5), font_size=16,
                              color=(255, 255, 255), bg_color=(0, 0, 255), emoji_prefix='de')
    assert result.shape == img.shape
    assert img.sum() == 0, "input image must not be modified"
    assert result.sum() > 0


def test_put_unicode_text_outside_image_is_noop():
    img = np.zeros((20, 20, 3), dtype=np.uint8)
    result = put_unicode_text(img, "Bird", (500, 500), font_size=12, bg_color=(0, 0, 0))
    assert np.array_equal(result, img)


def test_fonts_are_cached():
    analyzer_module._get_fonts.cache_clear()
    analyzer_module._get_fonts(18)
    analyzer_module._get_fonts(18)
    info = analyzer_module._get_fonts.cache_info()
    assert info.hits == 1 and info.misses == 1


def test_gb_fallback_renders_union_jack_not_grey(monkeypatch):
    """Regression: 'gb' mapped to a Base64 string instead of the 🇬🇧 emoji."""
    monkeypatch.setattr(analyzer_module, '_get_embedded_flag_image', lambda *a, **k: None)
    icon = render_flag_icon('gb', size=24)
    expected = render_emoji_icon('🇬🇧', size=24)
    assert icon is not None
    assert np.array_equal(np.array(icon), np.array(expected))
    # The grey fallback flag would be uniform (128,128,128) inside the border
    assert len(np.unique(np.array(icon).reshape(-1, 3), axis=0)) > 2
