"""
Shared pytest fixtures: synthetic videos and a fake YOLO model, so the
analysis pipeline can be tested without downloading model weights.
"""

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from vogel_video_analyzer.analyzer import VideoAnalyzer, COCO_CLASS_BIRD  # noqa: E402
from vogel_video_analyzer.hailo_engine import _MockBox, _MockResult  # noqa: E402
from vogel_video_analyzer.i18n import init_i18n  # noqa: E402


@pytest.fixture(autouse=True)
def english_messages():
    """Use English messages in all tests (independent of the system locale)."""
    init_i18n('en')
    yield


def write_video(path, frames, fps=10.0, size=(64, 48)):
    """
    Write a synthetic MP4 video.

    Args:
        frames: number of frames, or a list of grey values (one per frame)
    Returns:
        Path of the written video
    """
    width, height = size
    values = list(range(frames)) if isinstance(frames, int) else list(frames)
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    assert writer.isOpened(), "OpenCV cannot write mp4v videos in this environment"
    for value in values:
        frame = np.full((height, width, 3), int(value) % 256, dtype=np.uint8)
        writer.write(frame)
    writer.release()
    return Path(path)


class FakeModel:
    """
    Callable that mimics ultralytics YOLO: model(frame, verbose=False).

    detections_for(call_index) -> list of (cls_id, conf); boxes are fixed.
    """

    def __init__(self, detections_for):
        self.detections_for = detections_for
        self.calls = 0

    def __call__(self, frame, verbose=False, **kwargs):
        dets = self.detections_for(self.calls)
        self.calls += 1
        h, w = frame.shape[:2]
        boxes = [_MockBox(2, 2, w // 2, h // 2, conf, cls_id) for cls_id, conf in dets]
        return [_MockResult(boxes)]


def make_analyzer(model, threshold=0.3, target_class=COCO_CLASS_BIRD):
    """Create a VideoAnalyzer without loading any real model."""
    analyzer = VideoAnalyzer.__new__(VideoAnalyzer)
    analyzer.threshold = threshold
    analyzer.target_class = target_class
    analyzer.identify_species = False
    analyzer.species_classifier = None
    analyzer.model = model
    return analyzer


@pytest.fixture
def video_factory(tmp_path):
    def factory(name='video.mp4', frames=20, fps=10.0, size=(64, 48)):
        return write_video(tmp_path / name, frames, fps=fps, size=size)
    return factory
