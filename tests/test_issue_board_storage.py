"""
Tests for robust storage of the issue board (corrupt files, atomic writes).
"""

import json

from vogel_video_analyzer.issue_board import IssueBoard


def test_corrupt_file_is_backed_up_not_overwritten(tmp_path, capsys):
    """Regression: a corrupt file was silently replaced by an empty list on the next save."""
    storage = tmp_path / "issues.json"
    storage.write_text("{ this is not json", encoding="utf-8")

    board = IssueBoard(storage)
    assert board.issues == []

    backups = list(tmp_path.glob("issues.json.corrupt-*"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "{ this is not json"
    assert "issues.json.corrupt-" in capsys.readouterr().out

    board.create_issue("New", "after corruption")
    assert backups[0].exists()


def test_wrong_structure_is_backed_up(tmp_path):
    storage = tmp_path / "issues.json"
    storage.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
    IssueBoard(storage)
    assert list(tmp_path.glob("issues.json.corrupt-*"))


def test_unknown_fields_are_ignored(tmp_path):
    storage = tmp_path / "issues.json"
    storage.write_text(json.dumps([{
        "id": 1, "title": "T", "description": "D", "status": "todo", "priority": "low",
        "labels": [], "created_at": "x", "updated_at": "y", "assignee": None,
        "future_field": "ignored",
    }]), encoding="utf-8")
    board = IssueBoard(storage)
    assert board.get_issue(1).title == "T"


def test_save_is_atomic_and_leaves_no_temp_files(tmp_path):
    storage = tmp_path / "issues.json"
    board = IssueBoard(storage)
    for i in range(3):
        board.create_issue(f"Issue {i}", "d")
    assert json.loads(storage.read_text(encoding="utf-8"))[2]["title"] == "Issue 2"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["issues.json"]


def test_empty_file_is_treated_as_empty_board(tmp_path):
    storage = tmp_path / "issues.json"
    storage.write_text("", encoding="utf-8")
    board = IssueBoard(storage)
    assert board.issues == []
    assert not list(tmp_path.glob("*.corrupt-*"))
