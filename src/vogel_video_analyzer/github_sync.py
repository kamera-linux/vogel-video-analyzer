"""
GitHub Issues Synchronisation für das Issue Board
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import json

try:
    from github import Github, GithubException
    from github.Issue import Issue as GHIssue
    import requests
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

from .issue_board import IssueBoard, Issue, IssueStatus, IssuePriority


class GitHubSync:
    """Synchronisiert lokale Issues mit GitHub Issues"""
    
    # Mapping zwischen lokalem Status und GitHub-Labels
    STATUS_LABELS = {
        "todo": "status: todo",
        "in_progress": "status: in progress",
        "done": "status: done",
        "blocked": "status: blocked"
    }
    
    PRIORITY_LABELS = {
        "low": "priority: low",
        "medium": "priority: medium",
        "high": "priority: high",
        "critical": "priority: critical"
    }
    
    def __init__(self, token: Optional[str] = None, repo: Optional[str] = None):
        """
        Initialisiert GitHub-Synchronisation
        
        Args:
            token: GitHub Personal Access Token (optional, wird aus verschiedenen Quellen geladen)
            repo: Repository im Format "owner/repo" (optional, wird automatisch erkannt)
        """
        if not GITHUB_AVAILABLE:
            raise ImportError(
                "PyGithub ist nicht installiert. Installieren Sie es mit: "
                "pip install PyGithub"
            )
        
        self.token = token or self._get_token()
        if not self.token:
            raise ValueError(
                "GitHub Token nicht gefunden. Bitte setzen Sie:\n"
                "1. Umgebungsvariable: export GITHUB_TOKEN=your_token\n"
                "2. Config-Datei: ~/.vogel_config.json\n"
                "3. CLI-Parameter: --github-token your_token"
            )
        
        self.github = Github(self.token)
        self.repo_name = repo or self._detect_repo()
        
        try:
            self.repo = self.github.get_repo(self.repo_name)
        except GithubException as e:
            raise ValueError(f"Repository '{self.repo_name}' nicht gefunden: {e}")
        
        # Project Board Info (wird bei Bedarf geladen)
        self._project_id = None
        self._status_field_id = None
        self._status_options = {}
        self._project_owner = None
    
    def _get_token(self) -> Optional[str]:
        """
        Lädt GitHub Token aus verschiedenen Quellen
        
        Priorität:
        1. Umgebungsvariable GITHUB_TOKEN
        2. Umgebungsvariable GH_TOKEN
        3. Config-Datei ~/.vogel_config.json
        4. Git credential helper
        """
        # 1. Umgebungsvariablen
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if token:
            return token
        
        # 2. Config-Datei
        config_path = Path.home() / '.vogel_config.json'
        if config_path.exists():
            try:
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    token = config.get('github_token')
                    if token:
                        return token
            except Exception:
                pass
        
        return None
    
    def _detect_repo(self) -> str:
        """
        Erkennt Repository aus Git-Konfiguration
        
        Returns:
            Repository im Format "owner/repo"
        """
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                capture_output=True,
                text=True,
                check=True
            )
            
            url = result.stdout.strip()
            
            # Parse GitHub URL
            # Formate: git@github.com:owner/repo.git oder https://github.com/owner/repo.git
            if 'github.com' in url:
                if url.startswith('git@'):
                    # git@github.com:owner/repo.git
                    parts = url.split(':')[1].replace('.git', '')
                else:
                    # https://github.com/owner/repo.git
                    parts = url.split('github.com/')[1].replace('.git', '')
                return parts
        except Exception:
            pass
        
        # Fallback auf vogel-video-analyzer Repository
        return "kamera-linux/vogel-video-analyzer"
    
    def _issue_to_github_format(self, issue: Issue) -> Dict:
        """Konvertiert lokales Issue zu GitHub-Format"""
        labels = []
        
        # Status-Label hinzufügen
        if issue.status in self.STATUS_LABELS:
            labels.append(self.STATUS_LABELS[issue.status])
        
        # Prioritäts-Label hinzufügen
        if issue.priority in self.PRIORITY_LABELS:
            labels.append(self.PRIORITY_LABELS[issue.priority])
        
        # Benutzerdefinierte Labels hinzufügen
        labels.extend(issue.labels)
        
        return {
            'title': issue.title,
            'body': self._format_issue_body(issue),
            'labels': labels,
            'assignee': issue.assignee
        }
    
    def _format_issue_body(self, issue: Issue) -> str:
        """Formatiert Issue-Body für GitHub"""
        body = issue.description + "\n\n---\n\n"
        body += f"**Local Issue ID:** #{issue.id}\n"
        body += f"**Created:** {issue.created_at}\n"
        body += f"**Updated:** {issue.updated_at}\n"
        return body
    
    def _extract_github_number_from_body(self, description: str) -> Optional[int]:
        """Extrahiert GitHub Issue Number aus dem Body"""
        import re
        match = re.search(r'github\.com/[^/]+/[^/]+/issues/(\d+)', description)
        if match:
            return int(match.group(1))
        return None
    
    def _github_to_local_issue(self, gh_issue: GHIssue, local_id: Optional[int] = None) -> Dict:
        """Konvertiert GitHub Issue zu lokalem Format"""
        # Status aus Labels extrahieren oder aus Issue State ableiten
        status = "todo"
        priority = "medium"
        custom_labels = []
        status_from_label = False
        
        for label in gh_issue.labels:
            label_name = label.name
            
            # Status-Label
            for local_status, gh_label in self.STATUS_LABELS.items():
                if label_name == gh_label:
                    status = local_status
                    status_from_label = True
                    break
            
            # Prioritäts-Label
            for local_priority, gh_label in self.PRIORITY_LABELS.items():
                if label_name == gh_label:
                    priority = local_priority
                    break
            
            # Andere Labels
            if (label_name not in self.STATUS_LABELS.values() and 
                label_name not in self.PRIORITY_LABELS.values()):
                custom_labels.append(label_name)
        
        # Fallback: Wenn kein Status-Label vorhanden, nutze Issue State
        if not status_from_label:
            if gh_issue.state == "closed":
                status = "done"
            else:
                status = "todo"
        
        # Füge GitHub Issue Link zur Beschreibung hinzu
        description = gh_issue.body or ""
        gh_link = f"\n\n---\n**GitHub Issue:** https://github.com/{self.repo_name}/issues/{gh_issue.number}"
        if gh_link not in description:
            description += gh_link
        
        return {
            'id': local_id or gh_issue.number,
            'title': gh_issue.title,
            'description': description,
            'status': status,
            'priority': priority,
            'labels': custom_labels,
            'assignee': gh_issue.assignee.login if gh_issue.assignee else None,
            'created_at': gh_issue.created_at.isoformat(),
            'updated_at': gh_issue.updated_at.isoformat()
        }
    
    def push_issue(self, issue: Issue, update_existing: bool = True, board: Optional[IssueBoard] = None) -> GHIssue:
        """
        Pusht ein lokales Issue zu GitHub
        
        Args:
            issue: Lokales Issue
            update_existing: Aktualisiere existierende Issues
            board: Issue Board (optional, für lokales Update nach Push)
        
        Returns:
            GitHub Issue Objekt
        """
        gh_data = self._issue_to_github_format(issue)
        
        # Suche nach existierendem Issue (anhand Titel oder ID im Body)
        existing = None
        if update_existing:
            # Prüfe erst ob Issue bereits GitHub Link hat
            gh_link = f"/issues/"
            if gh_link in issue.description:
                # Extrahiere Issue Number
                import re
                match = re.search(r'/issues/(\d+)', issue.description)
                if match:
                    issue_num = int(match.group(1))
                    try:
                        existing = self.repo.get_issue(issue_num)
                    except:
                        pass
            
            # Fallback: Suche nach Local Issue ID
            if not existing:
                for gh_issue in self.repo.get_issues(state='all'):
                    if f"Local Issue ID:** #{issue.id}" in (gh_issue.body or ""):
                        existing = gh_issue
                        break
        
        if existing:
            # Aktualisiere existierendes Issue
            existing.edit(
                title=gh_data['title'],
                body=gh_data['body'],
                labels=gh_data['labels']
            )
            if gh_data['assignee']:
                existing.add_to_assignees(gh_data['assignee'])
            
            # Schließe Issue wenn Status "done"
            if issue.status == "done" and existing.state == "open":
                existing.edit(state='closed')
            elif issue.status != "done" and existing.state == "closed":
                existing.edit(state='open')
            
            return existing
        else:
            # Erstelle neues Issue
            create_params = {
                'title': gh_data['title'],
                'body': gh_data['body'],
                'labels': gh_data['labels']
            }
            if gh_data['assignee']:
                create_params['assignee'] = gh_data['assignee']
            
            gh_issue = self.repo.create_issue(**create_params)
            
            # Aktualisiere lokales Issue mit GitHub Link
            if board:
                gh_link = f"\n\n---\n**GitHub Issue:** https://github.com/{self.repo_name}/issues/{gh_issue.number}"
                if gh_link not in issue.description:
                    board.update_issue(
                        issue.id,
                        description=issue.description + gh_link
                    )
            
            return gh_issue
    
    def pull_issues(self, board: IssueBoard, state: str = 'open') -> List[Issue]:
        """
        Holt GitHub Issues und erstellt/aktualisiert lokale Issues
        
        Args:
            board: Lokales Issue Board
            state: GitHub Issue State ('open', 'closed', 'all')
        
        Returns:
            Liste der synchronisierten Issues
        """
        synced_issues = []
        
        for gh_issue in self.repo.get_issues(state=state):
            # Prüfe ob Issue bereits lokal existiert (anhand GitHub Issue Link im Body)
            local_id = None
            gh_link = f"/issues/{gh_issue.number}"
            
            for local_issue in board.issues:
                if gh_link in local_issue.description:
                    local_id = local_issue.id
                    break
            
            issue_data = self._github_to_local_issue(gh_issue, local_id)
            
            if local_id:
                # Aktualisiere existierendes lokales Issue
                board.update_issue(
                    local_id,
                    title=issue_data['title'],
                    description=issue_data['description'],
                    status=issue_data['status'],
                    priority=issue_data['priority'],
                    labels=issue_data['labels'],
                    assignee=issue_data['assignee']
                )
                issue = board.get_issue(local_id)
            else:
                # Erstelle neues lokales Issue
                issue = board.create_issue(
                    title=issue_data['title'],
                    description=issue_data['description'],
                    status=issue_data['status'],
                    priority=issue_data['priority'],
                    labels=issue_data['labels'],
                    assignee=issue_data['assignee']
                )
            
            synced_issues.append(issue)
        
        return synced_issues
    
    def _graphql_query(self, query: str, variables: Dict = None) -> Dict:
        """
        Führt eine GraphQL-Abfrage aus
        
        Args:
            query: GraphQL Query String
            variables: Query Variablen
        
        Returns:
            Query-Resultat
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        payload = {'query': query}
        if variables:
            payload['variables'] = variables
        
        response = requests.post(
            'https://api.github.com/graphql',
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"GraphQL query failed: {response.status_code} - {response.text}")
        
        result = response.json()
        
        if 'errors' in result:
            errors = result['errors']
            raise Exception(f"GraphQL errors: {errors}")
        
        return result.get('data', {})
    
    def _load_project_data(self, project_number: int = 3):
        """
        Lädt Project Board Daten (ID, Fields, Options)
        
        Args:
            project_number: Project Number (Standard: 3 für vogel-video-analyzer)
        """
        if self._project_id:
            return  # Bereits geladen
        
        # Ermittle Owner (User oder Organization)
        owner = self.repo_name.split('/')[0]
        self._project_owner = owner
        
        # Query für User Project
        query = '''
        query($owner: String!, $number: Int!) {
          user(login: $owner) {
            projectV2(number: $number) {
              id
              title
              fields(first: 20) {
                nodes {
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    options {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
        '''
        
        variables = {
            'owner': owner,
            'number': project_number
        }
        
        try:
            data = self._graphql_query(query, variables)
            
            if not data.get('user') or not data['user'].get('projectV2'):
                raise Exception(f"Project #{project_number} nicht gefunden für User {owner}")
            
            project = data['user']['projectV2']
            self._project_id = project['id']
            
            # Finde Status Field
            for field in project['fields']['nodes']:
                if field.get('name') == 'Status':
                    self._status_field_id = field['id']
                    # Speichere Status-Optionen
                    for option in field.get('options', []):
                        # Mappe Emoji-Status auf interne Werte
                        name = option['name']
                        if 'Todo' in name:
                            self._status_options['todo'] = option['id']
                        elif 'Progress' in name:
                            self._status_options['in_progress'] = option['id']
                        elif 'Done' in name:
                            self._status_options['done'] = option['id']
                        elif 'Blocked' in name:
                            self._status_options['blocked'] = option['id']
                    break
        
        except Exception as e:
            print(f"⚠️  Warnung: Konnte Project Board Daten nicht laden: {e}")
    
    def _get_project_item_status(self, issue_node_id: str) -> Optional[str]:
        """
        Holt den Status eines Issues im Project Board
        
        Args:
            issue_node_id: GitHub Issue Node ID
        
        Returns:
            Status string ('todo', 'in_progress', 'done', 'blocked') oder None
        """
        if not self._project_id:
            return None
        
        query = '''
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100) {
                nodes {
                  id
                  content {
                    ... on Issue {
                      id
                    }
                  }
                  fieldValues(first: 20) {
                    nodes {
                      ... on ProjectV2ItemFieldSingleSelectValue {
                        field {
                          ... on ProjectV2SingleSelectField {
                            id
                            name
                          }
                        }
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
        '''
        
        variables = {'projectId': self._project_id}
        
        try:
            data = self._graphql_query(query, variables)
            
            if not data.get('node') or not data['node'].get('items'):
                return None
            
            # Suche nach dem Issue
            for item in data['node']['items']['nodes']:
                if item.get('content', {}).get('id') == issue_node_id:
                    # Finde Status Field Value
                    for field_value in item.get('fieldValues', {}).get('nodes', []):
                        if field_value.get('field', {}).get('name') == 'Status':
                            status_name = field_value.get('name', '')
                            # Mappe zurück auf interne Werte
                            if 'Todo' in status_name:
                                return 'todo'
                            elif 'Progress' in status_name:
                                return 'in_progress'
                            elif 'Done' in status_name:
                                return 'done'
                            elif 'Blocked' in status_name:
                                return 'blocked'
                    break
        
        except Exception as e:
            print(f"⚠️  Warnung: Status für Issue {issue_node_id[:10]}... nicht abrufbar: {e}")
        
        return None
    
    def sync_all(self, board: IssueBoard, direction: str = 'both', sync_project_status: bool = True) -> Dict:
        """
        Synchronisiert alle Issues
        
        Args:
            board: Lokales Issue Board
            direction: 'push' (lokal -> GitHub), 'pull' (GitHub -> lokal), 'both'
            sync_project_status: Synchronisiere auch Project Board Status
        
        Returns:
            Statistiken über die Synchronisation
        """
        stats = {
            'pushed': 0,
            'pulled': 0,
            'project_synced': 0,
            'errors': []
        }
        
        # Lade Project Board Daten wenn nötig
        if sync_project_status:
            try:
                self._load_project_data()
            except Exception as e:
                stats['errors'].append(f"Project Board Daten laden: {str(e)}")
                sync_project_status = False
        
        if direction in ['push', 'both']:
            for issue in board.issues:
                try:
                    self.push_issue(issue, board=board)
                    stats['pushed'] += 1
                except Exception as e:
                    stats['errors'].append(f"Push Issue #{issue.id}: {str(e)}")
        
        if direction in ['pull', 'both']:
            try:
                synced = self.pull_issues(board, state='all')
                stats['pulled'] = len(synced)
                
                # Synchronisiere Project Board Status
                if sync_project_status and self._project_id:
                    # Hole alle GitHub Issues
                    gh_issues = list(self.repo.get_issues(state='all'))
                    
                    for issue in board.issues:
                        # Versuche GitHub Issue zu finden (via Titel-Match)
                        gh_issue = None
                        for gh in gh_issues:
                            if gh.title == issue.title:
                                gh_issue = gh
                                break
                        
                        if gh_issue:
                            # Hole Status aus Project Board
                            project_status = self._get_project_item_status(gh_issue.node_id)
                            if project_status and project_status != issue.status:
                                print(f"   📊 Issue #{issue.id} '{issue.title[:30]}': {issue.status} → {project_status}")
                                issue.status = project_status
                                stats['project_synced'] += 1
                    
                    # Speichere aktualisierte Issues
                    if stats['project_synced'] > 0:
                        board._save()
                
            except Exception as e:
                stats['errors'].append(f"Pull: {str(e)}")
        
        return stats
    
    @staticmethod
    def setup_token_interactive():
        """Interaktive Token-Einrichtung"""
        print("=" * 60)
        print("GitHub Token Einrichtung")
        print("=" * 60)
        print("\nUm GitHub Issues zu synchronisieren, benötigen Sie einen")
        print("Personal Access Token von GitHub.")
        print("\nSchritte:")
        print("1. Gehen Sie zu: https://github.com/settings/tokens")
        print("2. Klicken Sie auf 'Generate new token (classic)'")
        print("3. Wählen Sie 'repo' scope (voller Repository-Zugriff)")
        print("4. Kopieren Sie den generierten Token")
        print("\nSpeichermethoden:")
        print("A) Umgebungsvariable (empfohlen):")
        print("   export GITHUB_TOKEN=your_token_here")
        print("   (Fügen Sie dies zu ~/.bashrc oder ~/.zshrc hinzu)")
        print("\nB) Config-Datei:")
        print("   Speichern in ~/.vogel_config.json")
        print("\nC) CLI-Parameter:")
        print("   vogel-issues sync --github-token your_token_here")
        print("\n" + "=" * 60)
        
        choice = input("\nToken jetzt in Config-Datei speichern? [y/N]: ")
        
        if choice.lower() == 'y':
            token = input("GitHub Token eingeben: ").strip()
            if token:
                import json
                config_path = Path.home() / '.vogel_config.json'
                config = {}
                
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                
                config['github_token'] = token
                
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                # Setze sichere Berechtigungen
                config_path.chmod(0o600)
                
                print(f"\n✅ Token gespeichert in {config_path}")
                print("⚠️  WICHTIG: Teilen Sie diese Datei niemals!")
                return True
        
        return False
