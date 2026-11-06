"""
Tests for the HTML report (escaping, bundled Chart.js, thumbnails) and i18n.
"""

import ast
import base64
import re
from pathlib import Path

import cv2
import numpy as np
import pytest

from vogel_video_analyzer import i18n
from vogel_video_analyzer.reporter import HTMLReporter, _js_json

from conftest import write_video

SRC = Path(__file__).parent.parent / "src" / "vogel_video_analyzer"


# ── Reporter ─────────────────────────────────────────────────────────────────

def _report_data(video_path, detections=None, species_stats=None):
    return {
        'video_path': str(video_path),
        'fps': 10.0,
        'duration_seconds': 2.0,
        'bird_detections': len(detections or []),
        'frames_with_birds': len(detections or []),
        'bird_segments': [{'start': 0.0, 'end': 1.0, 'detections': 2}],
        'detections': detections or [],
        'species_stats': species_stats or {},
    }


def test_report_escapes_video_name_and_species(tmp_path):
    video = write_video(tmp_path / "a.mp4", 5)
    evil = tmp_path / "<script>alert(1)<script>&.mp4"
    video.rename(evil)
    species = '<img src=x onerror=alert(1)>'
    data = _report_data(evil,
                        detections=[{'frame': 1, 'timestamp': 0.1, 'birds': 1,
                                     'species': [{'species': species, 'confidence': 0.9}]}],
                        species_stats={species: {'count': 1, 'avg_confidence': 0.9}})
    html = HTMLReporter(data, str(evil))._build_html(max_thumbnails=5)

    assert "<script>alert(1)" not in html
    assert "&lt;script&gt;alert(1)&lt;script&gt;&amp;.mp4" in html
    assert "<img src=x" not in html


def test_js_json_cannot_close_script_tag():
    encoded = _js_json(["</script><b>&"])
    assert "</script>" not in encoded
    assert "<" not in encoded and ">" not in encoded and "&" not in encoded


def test_bundled_chartjs_is_used(tmp_path, monkeypatch):
    def no_network(*args, **kwargs):
        raise AssertionError("no network access expected")
    monkeypatch.setattr("urllib.request.urlopen", no_network, raising=False)
    code = HTMLReporter._get_chartjs()
    assert "Chart.js v4.4.0" in code


def test_report_language_attribute(tmp_path):
    i18n.init_i18n('ja')
    video = write_video(tmp_path / "v.mp4", 3)
    html = HTMLReporter(_report_data(video), str(video))._build_html(max_thumbnails=0)
    assert '<html lang="ja">' in html


def test_thumbnails_use_the_detected_frame(tmp_path):
    """Frame numbers from analyze_video are 1-based: frame N is the N-th frame read."""
    values = [0, 40, 80, 120, 160, 200, 240]
    video = write_video(tmp_path / "v.mp4", values, size=(64, 48))
    detections = [
        {'frame': 3, 'timestamp': 0.3, 'birds': 1, 'species': [{'species': 'A', 'confidence': 0.5}]},
        {'frame': 6, 'timestamp': 0.6, 'birds': 1, 'species': [{'species': 'B', 'confidence': 0.9}]},
    ]
    reporter = HTMLReporter(_report_data(video, detections), str(video))
    thumbs = reporter._generate_thumbnails(max_count=10)

    assert [t['frame'] for t in thumbs] == [6, 3]  # sorted by confidence
    for thumb in thumbs:
        img = cv2.imdecode(np.frombuffer(base64.b64decode(thumb['image']), np.uint8), cv2.IMREAD_COLOR)
        expected = values[thumb['frame'] - 1]
        assert abs(float(img.mean()) - expected) < 12, (thumb['frame'], img.mean(), expected)


# ── i18n ─────────────────────────────────────────────────────────────────────

def _translations():
    tree = ast.parse((SRC / "i18n.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'TRANSLATIONS' for t in node.targets):
            return node.value
    raise AssertionError("TRANSLATIONS not found")


def test_all_used_translation_keys_exist_in_all_languages():
    used = set()
    for path in SRC.glob("*.py"):
        used |= set(re.findall(r"\bt\(['\"]([a-zA-Z0-9_]+)['\"]", path.read_text(encoding="utf-8")))
    for lang, table in i18n.TRANSLATIONS.items():
        missing = used - set(table)
        assert not missing, f"{lang}: missing {sorted(missing)}"


def test_translation_tables_have_same_keys_and_no_duplicates():
    node = _translations()
    key_sets = {}
    for lang_node, table_node in zip(node.keys, node.values):
        keys = [k.value for k in table_node.keys]
        assert len(keys) == len(set(keys)), f"duplicate keys in {lang_node.value}"
        key_sets[lang_node.value] = set(keys)
    assert key_sets['en'] == key_sets['de'] == key_sets['ja']


@pytest.mark.parametrize("env, expected", [
    ({'VOGEL_LANG': 'ja', 'LANG': 'de_DE.UTF-8'}, 'ja'),
    ({'LANG': 'de_DE.UTF-8'}, 'de'),
    ({'LC_ALL': 'ja_JP.UTF-8', 'LANG': 'de_DE.UTF-8'}, 'ja'),
    ({'LANGUAGE': 'fr:de', 'LANG': 'en_US.UTF-8'}, 'de'),
    ({'LANG': 'C.UTF-8'}, 'en'),
    ({'LANG': 'nl_BE.UTF-8'}, 'en'),  # 'de'/'ja' substrings must not match
])
def test_language_detection(monkeypatch, env, expected):
    for var in ('VOGEL_LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
        monkeypatch.delenv(var, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    assert i18n.I18n()._detect_language() == expected
