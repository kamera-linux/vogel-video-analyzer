"""
Tests for the CLI: argument validation, Tee logging, exit codes and the
safety rules of --delete-file / --delete-folder.
"""

import argparse
import io
import subprocess
import sys
from pathlib import Path

import pytest

from vogel_video_analyzer import cli


def _stats(path, frames_analyzed=10, frames_with_birds=0):
    pct = (frames_with_birds / frames_analyzed * 100) if frames_analyzed else 0
    return {
        'video_path': str(path),
        'frames_analyzed': frames_analyzed,
        'frames_with_birds': frames_with_birds,
        'bird_percentage': pct,
        'duration_seconds': 10.0,
    }


def _touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"video")
    return path


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """Run in a separate cwd so that tmp_path folders are not protected."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    return tmp_path


# ── Argument validation ─────────────────────────────────────────────────────

@pytest.mark.parametrize("value", ["0", "-3", "abc"])
def test_positive_int_rejects_invalid(value):
    with pytest.raises(argparse.ArgumentTypeError):
        cli._positive_int(value)


@pytest.mark.parametrize("value", ["-0.1", "1.5", "x"])
def test_probability_rejects_invalid(value):
    with pytest.raises(argparse.ArgumentTypeError):
        cli._probability(value)


def test_validators_accept_valid_values():
    assert cli._positive_int("5") == 5
    assert cli._probability("0.3") == pytest.approx(0.3)
    assert cli._non_negative_float("0") == 0.0


def test_cli_rejects_sample_rate_zero(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['vogel-analyze', '--sample-rate', '0', 'video.mp4'])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 2


# ── Tee ──────────────────────────────────────────────────────────────────────

def test_tee_writes_to_all_streams_and_supports_stream_api():
    console, logfile = io.StringIO(), io.StringIO()
    tee = cli.Tee(console, logfile)
    assert tee.write("hello") == 5
    tee.flush()
    assert console.getvalue() == logfile.getvalue() == "hello"
    assert tee.isatty() is False
    assert isinstance(tee.encoding, (str, type(None)))
    # Unknown attributes are delegated to the console stream
    assert tee.getvalue() == "hello"


# ── Exit codes / python -m ───────────────────────────────────────────────────

def test_python_m_propagates_exit_code(tmp_path):
    """Regression: __main__ ignored the return value of main() (always exit 0)."""
    result = subprocess.run(
        [sys.executable, '-m', 'vogel_video_analyzer', '--language', 'en',
         '--export-onnx', str(tmp_path / 'missing.pt')],
        capture_output=True, text=True, cwd=tmp_path,
        env={**__import__('os').environ, 'PYTHONPATH': str(Path(__file__).parent.parent / 'src')},
    )
    assert result.returncode == 1, result.stderr


def test_main_returns_1_when_a_video_fails(monkeypatch, tmp_path):
    class DummyAnalyzer:
        def __init__(self, **kwargs):
            pass

        def analyze_video(self, path, sample_rate=5):
            raise RuntimeError("cannot open")

    monkeypatch.setattr(cli, 'VideoAnalyzer', DummyAnalyzer)
    monkeypatch.setattr(sys, 'argv', ['vogel-analyze', '--language', 'en', str(tmp_path / 'x.mp4')])
    assert cli.main() == 1


# ── --delete-file ────────────────────────────────────────────────────────────

def test_file_deletion_skips_unreadable_videos(workdir):
    empty = _touch(workdir / "a" / "empty.mp4")
    unreadable = _touch(workdir / "a" / "broken.mp4")
    birds = _touch(workdir / "a" / "birds.mp4")
    stats = [_stats(empty), _stats(unreadable, frames_analyzed=0), _stats(birds, frames_with_birds=3)]

    cli._delete_empty_video_files(stats)

    assert not empty.exists()
    assert unreadable.exists(), "a video without readable frames must never be deleted"
    assert birds.exists()


def test_file_deletion_dry_run_deletes_nothing(workdir, capsys):
    empty = _touch(workdir / "a" / "empty.mp4")
    cli._delete_empty_video_files([_stats(empty)], dry_run=True)
    assert empty.exists()
    assert "DRY RUN" in capsys.readouterr().out


# ── --delete-folder ──────────────────────────────────────────────────────────

def test_folder_deletion_deletes_only_fully_empty_folders(workdir):
    empty_dir = workdir / "2026-01-01"
    mixed_dir = workdir / "2026-01-02"
    e1 = _touch(empty_dir / "a.mp4")
    e2 = _touch(empty_dir / "b.mp4")
    m_empty = _touch(mixed_dir / "a.mp4")
    m_birds = _touch(mixed_dir / "b.mp4")
    stats = [_stats(e1), _stats(e2), _stats(m_empty), _stats(m_birds, frames_with_birds=4)]

    to_delete, skipped = cli._plan_folder_deletion(stats)
    assert to_delete == [empty_dir.resolve()]
    assert (mixed_dir.resolve(), 'delete_skip_mixed') in skipped

    cli._delete_empty_video_folders(stats)
    assert not empty_dir.exists()
    assert m_birds.exists(), "videos with birds must never be deleted"


def test_folder_deletion_never_deletes_current_directory(workdir, monkeypatch):
    """Regression: 'vogel-analyze --delete-folder video.mp4' deleted the cwd."""
    folder = workdir / "here"
    video = _touch(folder / "video.mp4")
    monkeypatch.chdir(folder)

    to_delete, skipped = cli._plan_folder_deletion([_stats(Path("video.mp4"))])
    assert to_delete == []
    assert skipped == [(folder.resolve(), 'delete_skip_protected')]

    cli._delete_empty_video_folders([_stats(Path("video.mp4"))])
    assert video.exists()


def test_folder_deletion_never_deletes_parents_of_cwd(workdir, monkeypatch):
    parent = workdir / "parent"
    video = _touch(parent / "video.mp4")
    child = parent / "child"
    child.mkdir()
    monkeypatch.chdir(child)
    to_delete, skipped = cli._plan_folder_deletion([_stats(video)])
    assert to_delete == []
    assert skipped[0][1] == 'delete_skip_protected'


def test_folder_deletion_never_deletes_home(workdir, monkeypatch):
    home = workdir / "home"
    video = _touch(home / "video.mp4")
    monkeypatch.setattr(Path, 'home', lambda: home)
    to_delete, skipped = cli._plan_folder_deletion([_stats(video)])
    assert to_delete == []
    assert skipped[0][1] == 'delete_skip_protected'


def test_folder_deletion_skips_folders_with_unanalyzed_videos(workdir):
    folder = workdir / "folder"
    analyzed = _touch(folder / "a.mp4")
    _touch(folder / "not_analyzed.MP4")
    to_delete, skipped = cli._plan_folder_deletion([_stats(analyzed)])
    assert to_delete == []
    assert skipped == [(folder.resolve(), 'delete_skip_unanalyzed')]


def test_folder_deletion_skips_folders_with_unreadable_videos(workdir):
    folder = workdir / "folder"
    empty = _touch(folder / "a.mp4")
    broken = _touch(folder / "b.mp4")
    to_delete, skipped = cli._plan_folder_deletion([_stats(empty), _stats(broken, frames_analyzed=0)])
    assert to_delete == []
    assert skipped[0][1] == 'delete_skip_unreadable'


def test_folder_deletion_dry_run(workdir):
    folder = workdir / "folder"
    video = _touch(folder / "a.mp4")
    cli._delete_empty_video_folders([_stats(video)], dry_run=True)
    assert video.exists()
