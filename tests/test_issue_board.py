"""
Tests für das Issue Board System
"""

import pytest
import json
import tempfile
from pathlib import Path
from vogel_video_analyzer.issue_board import IssueBoard, Issue


@pytest.fixture
def temp_storage():
    """Erstellt eine temporäre Speicherdatei"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    yield temp_path
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def board(temp_storage):
    """Erstellt ein IssueBoard mit temporärem Storage"""
    return IssueBoard(temp_storage)


def test_create_issue(board):
    """Test: Issue erstellen"""
    issue = board.create_issue(
        title="Test Issue",
        description="Dies ist ein Test",
        priority="high"
    )
    
    assert issue.id == 1
    assert issue.title == "Test Issue"
    assert issue.description == "Dies ist ein Test"
    assert issue.status == "todo"
    assert issue.priority == "high"
    assert len(board.issues) == 1


def test_create_multiple_issues(board):
    """Test: Mehrere Issues erstellen"""
    issue1 = board.create_issue("Issue 1", "Beschreibung 1")
    issue2 = board.create_issue("Issue 2", "Beschreibung 2")
    issue3 = board.create_issue("Issue 3", "Beschreibung 3")
    
    assert issue1.id == 1
    assert issue2.id == 2
    assert issue3.id == 3
    assert len(board.issues) == 3


def test_get_issue(board):
    """Test: Issue abrufen"""
    created = board.create_issue("Test", "Test Beschreibung")
    retrieved = board.get_issue(created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.title == created.title


def test_get_nonexistent_issue(board):
    """Test: Nicht existierendes Issue abrufen"""
    issue = board.get_issue(999)
    assert issue is None


def test_update_issue(board):
    """Test: Issue aktualisieren"""
    issue = board.create_issue("Original", "Original Beschreibung")
    
    updated = board.update_issue(
        issue.id,
        title="Aktualisiert",
        status="in_progress",
        priority="critical"
    )
    
    assert updated is not None
    assert updated.title == "Aktualisiert"
    assert updated.status == "in_progress"
    assert updated.priority == "critical"
    assert updated.description == "Original Beschreibung"  # Nicht geändert


def test_delete_issue(board):
    """Test: Issue löschen"""
    issue = board.create_issue("Zu löschen", "Wird gelöscht")
    assert len(board.issues) == 1
    
    result = board.delete_issue(issue.id)
    assert result is True
    assert len(board.issues) == 0


def test_delete_nonexistent_issue(board):
    """Test: Nicht existierendes Issue löschen"""
    result = board.delete_issue(999)
    assert result is False


def test_list_issues_no_filter(board):
    """Test: Alle Issues auflisten"""
    board.create_issue("Issue 1", "Desc 1")
    board.create_issue("Issue 2", "Desc 2")
    board.create_issue("Issue 3", "Desc 3")
    
    issues = board.list_issues()
    assert len(issues) == 3


def test_list_issues_by_status(board):
    """Test: Issues nach Status filtern"""
    board.create_issue("Todo 1", "Desc", status="todo")
    board.create_issue("Todo 2", "Desc", status="todo")
    board.create_issue("Done", "Desc", status="done")
    
    todo_issues = board.list_issues(status="todo")
    done_issues = board.list_issues(status="done")
    
    assert len(todo_issues) == 2
    assert len(done_issues) == 1


def test_list_issues_by_priority(board):
    """Test: Issues nach Priorität filtern"""
    board.create_issue("Low", "Desc", priority="low")
    board.create_issue("High 1", "Desc", priority="high")
    board.create_issue("High 2", "Desc", priority="high")
    
    high_issues = board.list_issues(priority="high")
    assert len(high_issues) == 2


def test_list_issues_by_label(board):
    """Test: Issues nach Label filtern"""
    board.create_issue("Bug 1", "Desc", labels=["bug", "critical"])
    board.create_issue("Bug 2", "Desc", labels=["bug"])
    board.create_issue("Feature", "Desc", labels=["enhancement"])
    
    bug_issues = board.list_issues(label="bug")
    assert len(bug_issues) == 2


def test_list_issues_by_assignee(board):
    """Test: Issues nach Assignee filtern"""
    board.create_issue("Task 1", "Desc", assignee="Alice")
    board.create_issue("Task 2", "Desc", assignee="Alice")
    board.create_issue("Task 3", "Desc", assignee="Bob")
    
    alice_issues = board.list_issues(assignee="Alice")
    assert len(alice_issues) == 2


def test_persistence(temp_storage):
    """Test: Persistenz über mehrere Board-Instanzen"""
    # Board 1: Issues erstellen
    board1 = IssueBoard(temp_storage)
    board1.create_issue("Issue 1", "Beschreibung 1")
    board1.create_issue("Issue 2", "Beschreibung 2")
    
    # Board 2: Issues laden
    board2 = IssueBoard(temp_storage)
    assert len(board2.issues) == 2
    assert board2.issues[0].title == "Issue 1"
    assert board2.issues[1].title == "Issue 2"


def test_statistics_empty(board):
    """Test: Statistiken für leeres Board"""
    stats = board.get_statistics()
    assert stats['total'] == 0


def test_statistics_with_issues(board):
    """Test: Statistiken mit Issues"""
    board.create_issue("Todo 1", "Desc", status="todo", priority="low")
    board.create_issue("Todo 2", "Desc", status="todo", priority="high")
    board.create_issue("Done", "Desc", status="done", priority="high")
    board.create_issue("Progress", "Desc", status="in_progress", priority="critical")
    
    stats = board.get_statistics()
    
    assert stats['total'] == 4
    assert stats['by_status']['todo'] == 2
    assert stats['by_status']['done'] == 1
    assert stats['by_status']['in_progress'] == 1
    assert stats['by_priority']['low'] == 1
    assert stats['by_priority']['high'] == 2
    assert stats['by_priority']['critical'] == 1


def test_issue_with_labels(board):
    """Test: Issue mit Labels"""
    issue = board.create_issue(
        "Bug Fix",
        "Fix critical bug",
        labels=["bug", "critical", "security"]
    )
    
    assert len(issue.labels) == 3
    assert "bug" in issue.labels
    assert "critical" in issue.labels
    assert "security" in issue.labels


def test_issue_to_dict(board):
    """Test: Issue zu Dictionary konvertieren"""
    issue = board.create_issue(
        "Test",
        "Test Beschreibung",
        priority="high",
        labels=["test"]
    )
    
    data = issue.to_dict()
    
    assert isinstance(data, dict)
    assert data['title'] == "Test"
    assert data['description'] == "Test Beschreibung"
    assert data['priority'] == "high"
    assert 'created_at' in data
    assert 'updated_at' in data


def test_issue_from_dict():
    """Test: Issue aus Dictionary erstellen"""
    data = {
        'id': 1,
        'title': 'Test',
        'description': 'Test Beschreibung',
        'status': 'todo',
        'priority': 'medium',
        'labels': ['test'],
        'created_at': '2024-01-01T12:00:00',
        'updated_at': '2024-01-01T12:00:00',
        'assignee': None
    }
    
    issue = Issue.from_dict(data)
    
    assert issue.id == 1
    assert issue.title == 'Test'
    assert issue.status == 'todo'
    assert issue.priority == 'medium'


def test_invalid_storage_file(temp_storage):
    """Test: Ungültige Speicherdatei"""
    # Schreibe ungültige JSON
    with open(temp_storage, 'w') as f:
        f.write("invalid json{{{")
    
    # Board sollte trotzdem initialisiert werden
    board = IssueBoard(temp_storage)
    assert len(board.issues) == 0
