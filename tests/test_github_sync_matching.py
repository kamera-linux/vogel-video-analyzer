"""
Tests for issue matching, PR filtering and token storage in GitHubSync.
"""

import os
import stat
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

try:
    from vogel_video_analyzer.github_sync import GitHubSync, GITHUB_AVAILABLE
    from vogel_video_analyzer.issue_board import IssueBoard
except ImportError:  # pragma: no cover
    pytest.skip("PyGithub nicht installiert", allow_module_level=True)

if not GITHUB_AVAILABLE:  # pragma: no cover
    pytest.skip("PyGithub nicht installiert", allow_module_level=True)


@pytest.fixture
def sync():
    with patch('vogel_video_analyzer.github_sync.Github') as gh:
        repo = Mock()
        gh.return_value.get_repo.return_value = repo
        s = GitHubSync(token='t', repo='owner/repo')
        yield s


def _gh_issue(number, title="T", body="", is_pr=False, state="open"):
    issue = Mock()
    issue.number = number
    issue.title = title
    issue.body = body
    issue.state = state
    issue.labels = []
    issue.assignee = None
    issue.pull_request = Mock() if is_pr else None
    issue.created_at.isoformat.return_value = "2026-01-01T00:00:00"
    issue.updated_at.isoformat.return_value = "2026-01-01T00:00:00"
    return issue


@pytest.mark.parametrize("url, expected", [
    ("git@github.com:owner/repo.git", "owner/repo"),
    ("git@github.com:owner/repo", "owner/repo"),
    ("ssh://git@github.com/owner/repo.git", "owner/repo"),
    ("https://github.com/owner/repo.git", "owner/repo"),
    ("https://user:token@github.com/owner/repo/", "owner/repo"),
    ("https://github.com/owner/my.github.io.git", "owner/my.github.io"),
    ("https://gitlab.com/owner/repo.git", None),
])
def test_parse_remote_url(url, expected):
    assert GitHubSync._parse_remote_url(url) == expected


def test_linked_issue_number_is_exact(sync):
    desc = ("See also https://github.com/other/project/issues/7 and #3.\n\n---\n"
            "**GitHub Issue:** https://github.com/owner/repo/issues/12")
    assert sync._linked_issue_number(desc) == 12
    assert sync._linked_issue_number("https://github.com/other/project/issues/7") is None
    assert sync._linked_issue_number("") is None


def test_pull_does_not_confuse_issue_1_with_issue_12(sync, tmp_path):
    """Regression: substring '/issues/1' matched '/issues/12'."""
    board = IssueBoard(tmp_path / "issues.json")
    local = board.create_issue("Local 12", "x\n\n---\n**GitHub Issue:** https://github.com/owner/repo/issues/12")
    sync.repo.get_issues.return_value = [_gh_issue(1, title="Remote 1"), _gh_issue(12, title="Remote 12")]

    sync.pull_issues(board, state='all')

    assert board.get_issue(local.id).title == "Remote 12"
    titles = sorted(i.title for i in board.issues)
    assert titles == ["Remote 1", "Remote 12"]


def test_pull_skips_pull_requests(sync, tmp_path):
    board = IssueBoard(tmp_path / "issues.json")
    sync.repo.get_issues.return_value = [_gh_issue(5, title="A PR", is_pr=True), _gh_issue(6, title="Issue")]
    synced = sync.pull_issues(board, state='all')
    assert [i.title for i in synced] == ["Issue"]


def test_push_ignores_links_to_other_repositories(sync, tmp_path):
    """Regression: any '/issues/N' link (also to other repos) selected the issue to update."""
    board = IssueBoard(tmp_path / "issues.json")
    issue = board.create_issue("Bug", "Related: https://github.com/other/project/issues/3")
    sync.repo.get_issues.return_value = []
    created = _gh_issue(20)
    sync.repo.create_issue.return_value = created

    sync.push_issue(issue, board=board)

    sync.repo.get_issue.assert_not_called()
    sync.repo.create_issue.assert_called_once()
    assert sync._linked_issue_number(board.get_issue(issue.id).description) == 20


def test_sync_all_lists_repository_issues_once_for_push(sync, tmp_path):
    """Regression: every pushed issue triggered a full scan of all GitHub issues."""
    board = IssueBoard(tmp_path / "issues.json")
    for i in range(5):
        board.create_issue(f"Issue {i}", "desc")
    sync.repo.get_issues.return_value = []
    sync.repo.create_issue.side_effect = lambda **kw: _gh_issue(100 + len(sync.repo.create_issue.mock_calls))

    stats = sync.sync_all(board, direction='push', sync_project_status=False)

    assert stats['pushed'] == 5, stats['errors']
    assert sync.repo.get_issues.call_count == 1


def test_push_finds_existing_issue_by_local_id(sync, tmp_path):
    board = IssueBoard(tmp_path / "issues.json")
    issue = board.create_issue("Bug", "desc")
    existing = _gh_issue(9, body=f"desc\n\n---\n\n**Local Issue ID:** #{issue.id}\n")
    other = _gh_issue(10, body=f"**Local Issue ID:** #{issue.id}0\n")  # ID 10, not 1
    sync.repo.get_issues.return_value = [other, existing]

    result = sync.push_issue(issue, board=board)

    assert result is existing
    existing.edit.assert_called()
    sync.repo.create_issue.assert_not_called()


@pytest.mark.skipif(os.name != 'posix', reason="POSIX permissions")
def test_save_token_creates_private_file(tmp_path):
    config = tmp_path / ".vogel_config.json"
    config.write_text('{"other": 1}')
    os.chmod(config, 0o644)

    GitHubSync.save_token("secret", config_path=config)

    mode = stat.S_IMODE(config.stat().st_mode)
    assert mode == 0o600
    import json
    assert json.loads(config.read_text()) == {"other": 1, "github_token": "secret"}
    assert not list(tmp_path.glob("*.tmp"))


def test_setup_token_uses_getpass(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, 'home', lambda: tmp_path)
    monkeypatch.setattr('builtins.input', lambda prompt="": "y")
    calls = []
    monkeypatch.setattr('getpass.getpass', lambda prompt="": calls.append(prompt) or "tok")
    assert GitHubSync.setup_token_interactive() is True
    assert calls, "token must be read with getpass (not echoed)"
    assert "tok" in (tmp_path / ".vogel_config.json").read_text()
