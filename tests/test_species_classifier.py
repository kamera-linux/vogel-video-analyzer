"""
Tests for species classification pre-processing (no model download).
"""

import numpy as np
import pytest

from vogel_video_analyzer import species_classifier as sc
from vogel_video_analyzer.species_classifier import BirdSpeciesClassifier, bgr_to_rgb


def test_bgr_to_rgb_swaps_channels():
    bgr = np.zeros((2, 2, 3), dtype=np.uint8)
    bgr[..., 0] = 255  # blue in OpenCV order
    rgb = bgr_to_rgb(bgr)
    assert tuple(rgb[0, 0]) == (0, 0, 255)
    assert tuple(bgr[0, 0]) == (255, 0, 0), "input must not be modified"


def test_bgr_to_rgb_leaves_other_shapes_unchanged():
    grey = np.zeros((2, 2), dtype=np.uint8)
    assert bgr_to_rgb(grey) is grey


needs_species = pytest.mark.skipif(not sc.SPECIES_AVAILABLE, reason="species extras not installed")


class _CapturingPipeline:
    def __init__(self):
        self.images = []

    def __call__(self, images, top_k=1, batch_size=None):
        single = not isinstance(images, list)
        images = [images] if single else images
        self.images.extend(images)
        preds = [[{'label': 'GREAT TIT', 'score': 0.9}] for _ in images]
        return preds[0] if single else preds


def _classifier_with(pipeline):
    clf = BirdSpeciesClassifier.__new__(BirdSpeciesClassifier)
    clf.model_name = "fake"
    clf.confidence_threshold = 0.3
    clf.classifier = pipeline
    return clf


def _blue_bgr_frame():
    frame = np.zeros((20, 20, 3), dtype=np.uint8)
    frame[..., 0] = 255  # pure blue in OpenCV BGR order
    return frame


@needs_species
def test_batch_crops_are_passed_as_rgb():
    """Regression: BGR crops were passed to the RGB model (red/blue swapped)."""
    pipeline = _CapturingPipeline()
    clf = _classifier_with(pipeline)
    result = clf.classify_crops_batch(_blue_bgr_frame(), [(0, 0, 10, 10), (5, 5, 15, 15)], top_k=1)
    assert len(result) == 2 and result[0][0]['label'] == 'GREAT TIT'
    for img in pipeline.images:
        assert img.getpixel((0, 0)) == (0, 0, 255)


@needs_species
def test_single_crop_is_passed_as_rgb():
    pipeline = _CapturingPipeline()
    clf = _classifier_with(pipeline)
    clf.classify_crop(_blue_bgr_frame(), (0, 0, 10, 10))
    assert pipeline.images[0].getpixel((0, 0)) == (0, 0, 255)


@needs_species
def test_empty_and_out_of_frame_crops():
    clf = _classifier_with(_CapturingPipeline())
    assert clf.classify_crops_batch(_blue_bgr_frame(), [(30, 30, 40, 40)]) == [[]]


@needs_species
def test_model_load_failure_raises(monkeypatch):
    """Regression: load errors were swallowed and classification silently returned nothing."""
    def broken_pipeline(*args, **kwargs):
        raise OSError("model not found")
    monkeypatch.setattr(sc, 'pipeline', broken_pipeline)
    with pytest.raises(RuntimeError):
        BirdSpeciesClassifier(model_name="does/not-exist")


def test_translation_tables_have_no_duplicate_keys():
    import ast
    import inspect
    tree = ast.parse(inspect.getsource(sc))
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant)]
            assert len(keys) == len(set(keys)), f"duplicate keys: {sorted(k for k in keys if keys.count(k) > 1)}"
