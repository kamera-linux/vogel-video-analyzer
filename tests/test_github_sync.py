"""
Tests für GitHub-Synchronisation (Mock-basiert)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile

try:
    from vogel_video_analyzer.github_sync import GitHubSync, GITHUB_AVAILABLE
    from vogel_video_analyzer.issue_board import IssueBoard, Issue
except ImportError:
    pytest.skip("PyGithub nicht installiert", allow_module_level=True)


@pytest.fixture
def mock_github():
    """Mock GitHub API"""
    with patch('vogel_video_analyzer.github_sync.Github') as mock_gh:
        yield mock_gh


@pytest.fixture
def temp_storage():
    """Erstellt eine temporäre Speicherdatei"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    yield temp_path
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def board(temp_storage):
    """Erstellt ein IssueBoard mit temporärem Storage"""
    return IssueBoard(temp_storage)


def test_github_available():
    """Test: PyGithub ist verfügbar"""
    assert GITHUB_AVAILABLE is True


def test_token_from_env(mock_github, monkeypatch):
    """Test: Token aus Umgebungsvariable laden"""
    monkeypatch.setenv('GITHUB_TOKEN', 'test_token_123')
    
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    sync = GitHubSync(repo='test/repo')
    assert sync.token == 'test_token_123'


def test_token_from_config(mock_github, tmp_path, monkeypatch):
    """Test: Token aus Config-Datei laden"""
    import json
    
    # Erstelle temporäre Config
    config_file = tmp_path / '.vogel_config.json'
    config = {'github_token': 'config_token_456'}
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    # Mock home directory
    monkeypatch.setattr(Path, 'home', lambda: tmp_path)
    
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    sync = GitHubSync(repo='test/repo')
    assert sync.token == 'config_token_456'


def test_missing_token(mock_github, monkeypatch):
    """Test: Fehler bei fehlendem Token"""
    # Entferne alle Token-Quellen
    monkeypatch.delenv('GITHUB_TOKEN', raising=False)
    monkeypatch.delenv('GH_TOKEN', raising=False)
    
    with pytest.raises(ValueError, match="GitHub Token nicht gefunden"):
        GitHubSync(repo='test/repo')


def test_issue_to_github_format(mock_github, board):
    """Test: Lokales Issue zu GitHub-Format konvertieren"""
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    sync = GitHubSync(token='test_token', repo='test/repo')
    
    issue = board.create_issue(
        title="Test Issue",
        description="Test Beschreibung",
        status="in_progress",
        priority="high",
        labels=["bug", "urgent"]
    )
    
    gh_format = sync._issue_to_github_format(issue)
    
    assert gh_format['title'] == "Test Issue"
    assert 'Test Beschreibung' in gh_format['body']
    assert 'status: in progress' in gh_format['labels']
    assert 'priority: high' in gh_format['labels']
    assert 'bug' in gh_format['labels']
    assert 'urgent' in gh_format['labels']


def test_github_to_local_issue(mock_github):
    """Test: GitHub Issue zu lokalem Format konvertieren"""
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    sync = GitHubSync(token='test_token', repo='test/repo')
    
    # Mock GitHub Issue
    gh_issue = Mock()
    gh_issue.number = 42
    gh_issue.title = "GitHub Issue"
    gh_issue.body = "GitHub Beschreibung"
    gh_issue.created_at = Mock()
    gh_issue.created_at.isoformat.return_value = "2024-01-01T12:00:00"
    gh_issue.updated_at = Mock()
    gh_issue.updated_at.isoformat.return_value = "2024-01-01T13:00:00"
    gh_issue.assignee = Mock()
    gh_issue.assignee.login = "testuser"
    
    # Mock Labels
    label1 = Mock()
    label1.name = "status: done"
    label2 = Mock()
    label2.name = "priority: critical"
    label3 = Mock()
    label3.name = "bug"
    gh_issue.labels = [label1, label2, label3]
    
    issue_data = sync._github_to_local_issue(gh_issue)
    
    assert issue_data['title'] == "GitHub Issue"
    assert issue_data['description'] == "GitHub Beschreibung"
    assert issue_data['status'] == "done"
    assert issue_data['priority'] == "critical"
    assert 'bug' in issue_data['labels']
    assert issue_data['assignee'] == "testuser"


def test_detect_repo_from_git(mock_github, tmp_path, monkeypatch):
    """Test: Repository aus Git-Konfiguration erkennen"""
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    # Mock subprocess für git config
    with patch('subprocess.run') as mock_run:
        mock_result = Mock()
        mock_result.stdout = "git@github.com:owner/repo.git\n"
        mock_run.return_value = mock_result
        
        sync = GitHubSync(token='test_token')
        assert sync.repo_name == "owner/repo"


def test_status_labels_mapping(mock_github):
    """Test: Status-Label-Mapping"""
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    sync = GitHubSync(token='test_token', repo='test/repo')
    
    assert sync.STATUS_LABELS['todo'] == "status: todo"
    assert sync.STATUS_LABELS['in_progress'] == "status: in progress"
    assert sync.STATUS_LABELS['done'] == "status: done"
    assert sync.STATUS_LABELS['blocked'] == "status: blocked"


def test_priority_labels_mapping(mock_github):
    """Test: Prioritäts-Label-Mapping"""
    mock_repo = Mock()
    mock_github.return_value.get_repo.return_value = mock_repo
    
    sync = GitHubSync(token='test_token', repo='test/repo')
    
    assert sync.PRIORITY_LABELS['low'] == "priority: low"
    assert sync.PRIORITY_LABELS['medium'] == "priority: medium"
    assert sync.PRIORITY_LABELS['high'] == "priority: high"
    assert sync.PRIORITY_LABELS['critical'] == "priority: critical"


@pytest.mark.skipif(not GITHUB_AVAILABLE, reason="PyGithub nicht installiert")
def test_module_import():
    """Test: Module können importiert werden"""
    from vogel_video_analyzer.github_sync import GitHubSync
    assert GitHubSync is not None
