"""
Issue Board System für vogel-video-analyzer
Verwaltet Issues für Projekt-Tracking und Bug-Reporting
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Literal
from dataclasses import dataclass, asdict, field


IssueStatus = Literal["todo", "in_progress", "done", "blocked"]
IssuePriority = Literal["low", "medium", "high", "critical"]


@dataclass
class Issue:
    """Repräsentiert ein einzelnes Issue"""
    id: int
    title: str
    description: str
    status: IssueStatus = "todo"
    priority: IssuePriority = "medium"
    labels: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    assignee: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Konvertiert Issue zu Dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Issue':
        """Erstellt Issue aus Dictionary"""
        return cls(**data)


class IssueBoard:
    """Verwaltet Issues in einer JSON-Datei"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialisiert das Issue Board
        
        Args:
            storage_path: Pfad zur Speicherdatei (Standard: ~/.vogel_issues.json)
        """
        if storage_path is None:
            storage_path = Path.home() / ".vogel_issues.json"
        self.storage_path = Path(storage_path)
        self.issues: List[Issue] = []
        self._load()
    
    def _load(self):
        """Lädt Issues aus der Speicherdatei"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.issues = [Issue.from_dict(issue_data) for issue_data in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️  Warnung: Fehler beim Laden von {self.storage_path}: {e}")
                self.issues = []
        else:
            self.issues = []
    
    def _save(self):
        """Speichert Issues in die Speicherdatei"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump([issue.to_dict() for issue in self.issues], f, indent=2, ensure_ascii=False)
    
    def _get_next_id(self) -> int:
        """Ermittelt die nächste verfügbare ID"""
        if not self.issues:
            return 1
        return max(issue.id for issue in self.issues) + 1
    
    def create_issue(
        self,
        title: str,
        description: str,
        status: IssueStatus = "todo",
        priority: IssuePriority = "medium",
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None
    ) -> Issue:
        """
        Erstellt ein neues Issue
        
        Args:
            title: Issue-Titel
            description: Beschreibung
            status: Status (todo, in_progress, done, blocked)
            priority: Priorität (low, medium, high, critical)
            labels: Liste von Labels
            assignee: Zugewiesene Person
        
        Returns:
            Das erstellte Issue
        """
        issue = Issue(
            id=self._get_next_id(),
            title=title,
            description=description,
            status=status,
            priority=priority,
            labels=labels or [],
            assignee=assignee
        )
        self.issues.append(issue)
        self._save()
        return issue
    
    def get_issue(self, issue_id: int) -> Optional[Issue]:
        """Ruft ein Issue anhand der ID ab"""
        for issue in self.issues:
            if issue.id == issue_id:
                return issue
        return None
    
    def list_issues(
        self,
        status: Optional[IssueStatus] = None,
        priority: Optional[IssuePriority] = None,
        label: Optional[str] = None,
        assignee: Optional[str] = None
    ) -> List[Issue]:
        """
        Listet Issues mit optionalen Filtern auf
        
        Args:
            status: Filtert nach Status
            priority: Filtert nach Priorität
            label: Filtert nach Label
            assignee: Filtert nach Assignee
        
        Returns:
            Liste der gefilterten Issues
        """
        filtered = self.issues
        
        if status:
            filtered = [i for i in filtered if i.status == status]
        if priority:
            filtered = [i for i in filtered if i.priority == priority]
        if label:
            filtered = [i for i in filtered if label in i.labels]
        if assignee:
            filtered = [i for i in filtered if i.assignee == assignee]
        
        return filtered
    
    def update_issue(
        self,
        issue_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[IssueStatus] = None,
        priority: Optional[IssuePriority] = None,
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None
    ) -> Optional[Issue]:
        """
        Aktualisiert ein Issue
        
        Args:
            issue_id: ID des zu aktualisierenden Issues
            title: Neuer Titel (optional)
            description: Neue Beschreibung (optional)
            status: Neuer Status (optional)
            priority: Neue Priorität (optional)
            labels: Neue Labels (optional)
            assignee: Neuer Assignee (optional)
        
        Returns:
            Das aktualisierte Issue oder None
        """
        issue = self.get_issue(issue_id)
        if not issue:
            return None
        
        if title is not None:
            issue.title = title
        if description is not None:
            issue.description = description
        if status is not None:
            issue.status = status
        if priority is not None:
            issue.priority = priority
        if labels is not None:
            issue.labels = labels
        if assignee is not None:
            issue.assignee = assignee
        
        issue.updated_at = datetime.now().isoformat()
        self._save()
        return issue
    
    def delete_issue(self, issue_id: int) -> bool:
        """
        Löscht ein Issue
        
        Args:
            issue_id: ID des zu löschenden Issues
        
        Returns:
            True wenn erfolgreich, False wenn Issue nicht gefunden
        """
        issue = self.get_issue(issue_id)
        if not issue:
            return False
        
        self.issues.remove(issue)
        self._save()
        return True
    
    def get_statistics(self) -> Dict:
        """
        Berechnet Statistiken über alle Issues
        
        Returns:
            Dictionary mit Statistiken
        """
        total = len(self.issues)
        if total == 0:
            return {
                "total": 0,
                "by_status": {},
                "by_priority": {}
            }
        
        stats = {
            "total": total,
            "by_status": {
                "todo": len([i for i in self.issues if i.status == "todo"]),
                "in_progress": len([i for i in self.issues if i.status == "in_progress"]),
                "done": len([i for i in self.issues if i.status == "done"]),
                "blocked": len([i for i in self.issues if i.status == "blocked"])
            },
            "by_priority": {
                "low": len([i for i in self.issues if i.priority == "low"]),
                "medium": len([i for i in self.issues if i.priority == "medium"]),
                "high": len([i for i in self.issues if i.priority == "high"]),
                "critical": len([i for i in self.issues if i.priority == "critical"])
            }
        }
        
        return stats
