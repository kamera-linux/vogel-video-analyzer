"""
GitHub Issues Synchronisation für das Issue Board
"""

import getpass
import json
import os
import re
import stat
import subprocess
from pathlib import Path
from typing import Optional, List, Dict

try:
    from github import Github, GithubException
    from github.Issue import Issue as GHIssue
    import requests
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

from .issue_board import IssueBoard, Issue

# Accepted remote URL formats:
#   git@github.com:owner/repo(.git)
#   ssh://git@github.com/owner/repo(.git)
#   https://github.com/owner/repo(.git)  (optionally with user:token@)
_REMOTE_RE = re.compile(
    r'github\.com[:/]+(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?/?$'
)

CONFIG_FILE_NAME = '.vogel_config.json'


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
        config_path = Path.home() / CONFIG_FILE_NAME
        if config_path.exists():
            try:
                mode = config_path.stat().st_mode
                if os.name == 'posix' and mode & (stat.S_IRWXG | stat.S_IRWXO):
                    print(f"⚠️  Warnung: {config_path} ist für andere Benutzer lesbar. "
                          f"Bitte ausführen: chmod 600 {config_path}")
                with open(config_path, 'r', encoding='utf-8') as f:
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
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                capture_output=True,
                text=True,
                check=True
            )
            
            parsed = self._parse_remote_url(result.stdout.strip())
            if parsed:
                return parsed
        except Exception:
            pass
        
        # Fallback auf vogel-video-analyzer Repository
        return "kamera-linux/vogel-video-analyzer"
    
    @staticmethod
    def _parse_remote_url(url: str) -> Optional[str]:
        """Parse a GitHub remote URL into "owner/repo" (None if not a GitHub URL)."""
        match = _REMOTE_RE.search(url.strip())
        if not match:
            return None
        return f"{match.group('owner')}/{match.group('repo')}"

    def _issue_url(self, number: int) -> str:
        """URL of a GitHub issue in the configured repository."""
        return f"https://github.com/{self.repo_name}/issues/{number}"

    def _github_link_block(self, number: int) -> str:
        """Link block appended to local issue descriptions."""
        return f"\n\n---\n**GitHub Issue:** {self._issue_url(number)}"

    def _linked_issue_number(self, description: str) -> Optional[int]:
        """
        Extract the GitHub issue number linked in a local description.

        Only links to issues of the configured repository are considered
        (links to other repositories or other issues in the text are ignored);
        the last link wins, because the sync appends its link at the end.
        """
        pattern = re.compile(
            r'https://github\.com/' + re.escape(self.repo_name) + r'/issues/(\d+)(?!\d)',
            re.IGNORECASE,
        )
        matches = pattern.findall(description or "")
        return int(matches[-1]) if matches else None

    @staticmethod
    def _local_id_from_body(body: str) -> Optional[int]:
        """Extract the local issue ID that push_issue() writes into the GitHub body."""
        match = re.search(r'\*\*Local Issue ID:\*\* #(\d+)(?!\d)', body or "")
        return int(match.group(1)) if match else None

    def _iter_repo_issues(self, state: str = 'all'):
        """Iterate repository issues, skipping pull requests (the API returns both)."""
        for gh_issue in self.repo.get_issues(state=state):
            if getattr(gh_issue, 'pull_request', None):
                continue
            yield gh_issue

    def _build_local_id_index(self) -> Dict[int, 'GHIssue']:
        """Map local issue IDs (from GitHub issue bodies) to GitHub issues - one API pass."""
        index = {}
        for gh_issue in self._iter_repo_issues('all'):
            local_id = self._local_id_from_body(gh_issue.body)
            if local_id is not None and local_id not in index:
                index[local_id] = gh_issue
        return index

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
        """Extrahiert GitHub Issue Number aus dem Body (nur Links auf dieses Repository)"""
        return self._linked_issue_number(description)
    
    def _github_to_local_issue(self, gh_issue: 'GHIssue', local_id: Optional[int] = None) -> Dict:
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
        if self._linked_issue_number(description) != gh_issue.number:
            description += self._github_link_block(gh_issue.number)
        
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
    
    def push_issue(self, issue: Issue, update_existing: bool = True, board: Optional[IssueBoard] = None,
                   local_id_index: Optional[Dict[int, 'GHIssue']] = None) -> 'GHIssue':
        """
        Pusht ein lokales Issue zu GitHub
        
        Args:
            issue: Lokales Issue
            update_existing: Aktualisiere existierende Issues
            board: Issue Board (optional, für lokales Update nach Push)
            local_id_index: Vorab erstellter Index lokale ID -> GitHub Issue
                            (vermeidet einen kompletten API-Durchlauf pro Issue)
        
        Returns:
            GitHub Issue Objekt
        """
        gh_data = self._issue_to_github_format(issue)
        
        # Suche nach existierendem Issue (anhand Link auf dieses Repo oder ID im Body)
        existing = None
        if update_existing:
            issue_num = self._linked_issue_number(issue.description)
            if issue_num is not None:
                try:
                    existing = self.repo.get_issue(issue_num)
                except GithubException:
                    existing = None
            
            # Fallback: Suche nach Local Issue ID
            if not existing:
                if local_id_index is None:
                    local_id_index = self._build_local_id_index()
                existing = local_id_index.get(issue.id)
        
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
            if local_id_index is not None:
                local_id_index[issue.id] = gh_issue
            
            # Aktualisiere lokales Issue mit GitHub Link
            if board and self._linked_issue_number(issue.description) != gh_issue.number:
                board.update_issue(
                    issue.id,
                    description=issue.description + self._github_link_block(gh_issue.number)
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
        
        # Index: GitHub Issue Number -> lokale ID (exakter Vergleich, kein Substring)
        number_to_local = {}
        for local_issue in board.issues:
            number = self._linked_issue_number(local_issue.description)
            if number is not None and number not in number_to_local:
                number_to_local[number] = local_issue.id
        
        for gh_issue in self._iter_repo_issues(state):
            # Prüfe ob Issue bereits lokal existiert (anhand GitHub Issue Link im Body)
            local_id = number_to_local.get(gh_issue.number)
            
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
                number_to_local[gh_issue.number] = issue.id
            
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
            json=payload,
            timeout=30
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
                        status = self._map_status_name(option['name'])
                        if status:
                            self._status_options[status] = option['id']
                    break
        
        except Exception as e:
            print(f"⚠️  Warnung: Konnte Project Board Daten nicht laden: {e}")
    
    @staticmethod
    def _map_status_name(status_name: str) -> Optional[str]:
        """Map a project board status option name to the internal status."""
        if 'Todo' in status_name:
            return 'todo'
        if 'Progress' in status_name:
            return 'in_progress'
        if 'Done' in status_name:
            return 'done'
        if 'Blocked' in status_name:
            return 'blocked'
        return None

    def _get_project_status_map(self) -> Dict[str, str]:
        """
        Holt den Status aller Issues im Project Board (mit Pagination).

        Returns:
            Dict Issue Node ID -> Status ('todo', 'in_progress', 'done', 'blocked')
        """
        if not self._project_id:
            return {}

        query = '''
        query($projectId: ID!, $cursor: String) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100, after: $cursor) {
                pageInfo {
                  hasNextPage
                  endCursor
                }
                nodes {
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

        status_map: Dict[str, str] = {}
        cursor = None
        while True:
            data = self._graphql_query(query, {'projectId': self._project_id, 'cursor': cursor})
            items = (data.get('node') or {}).get('items')
            if not items:
                break
            for item in items.get('nodes', []):
                node_id = (item.get('content') or {}).get('id')
                if not node_id:
                    continue
                for field_value in (item.get('fieldValues') or {}).get('nodes', []):
                    if (field_value.get('field') or {}).get('name') == 'Status':
                        status = self._map_status_name(field_value.get('name', ''))
                        if status:
                            status_map[node_id] = status
                        break
            page_info = items.get('pageInfo') or {}
            if not page_info.get('hasNextPage'):
                break
            cursor = page_info.get('endCursor')
        return status_map

    def _get_project_item_status(self, issue_node_id: str) -> Optional[str]:
        """
        Holt den Status eines Issues im Project Board
        
        Args:
            issue_node_id: GitHub Issue Node ID
        
        Returns:
            Status string ('todo', 'in_progress', 'done', 'blocked') oder None
        """
        try:
            return self._get_project_status_map().get(issue_node_id)
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
            try:
                # Einmaliger API-Durchlauf statt einer kompletten Suche pro Issue
                local_id_index = self._build_local_id_index()
            except Exception as e:
                stats['errors'].append(f"Issue-Index laden: {str(e)}")
                local_id_index = None
            for issue in list(board.issues):
                try:
                    self.push_issue(issue, board=board, local_id_index=local_id_index)
                    stats['pushed'] += 1
                except Exception as e:
                    stats['errors'].append(f"Push Issue #{issue.id}: {str(e)}")
        
        if direction in ['pull', 'both']:
            try:
                synced = self.pull_issues(board, state='all')
                stats['pulled'] = len(synced)
                
                # Synchronisiere Project Board Status
                if sync_project_status and self._project_id:
                    status_map = self._get_project_status_map()
                    
                    for issue in board.issues:
                        # GitHub Issue über den Link in der lokalen Beschreibung finden
                        number = self._linked_issue_number(issue.description)
                        if number is None:
                            continue
                        try:
                            gh_issue = self.repo.get_issue(number)
                        except GithubException:
                            continue
                        
                        project_status = status_map.get(gh_issue.node_id)
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
    def save_token(token: str, config_path: Optional[Path] = None) -> Path:
        """
        Speichert den Token in der Config-Datei mit Berechtigung 0600.

        Die Datei wird direkt mit restriktiven Rechten angelegt (kein Zeitfenster,
        in dem sie für andere lesbar ist) und atomar ersetzt.
        """
        config_path = Path(config_path) if config_path else Path.home() / CONFIG_FILE_NAME
        config = {}
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config['github_token'] = token

        tmp_path = config_path.with_name(config_path.name + '.tmp')
        fd = os.open(str(tmp_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            os.chmod(tmp_path, 0o600)  # in case the file already existed
            os.replace(tmp_path, config_path)
        except Exception:
            try:
                tmp_path.unlink()
            except OSError:
                pass
            raise
        return config_path

    @staticmethod
    def setup_token_interactive():
        """Interaktive Token-Einrichtung"""
        print("=" * 60)
        print("GitHub Token Einrichtung")
        print("=" * 60)
        print("\nUm GitHub Issues zu synchronisieren, benötigen Sie einen")
        print("Personal Access Token von GitHub.")
        print("\nSchritte:")
        print("1. Gehen Sie zu: https://github.com/settings/personal-access-tokens")
        print("2. Erstellen Sie einen 'Fine-grained token' nur für dieses Repository")
        print("3. Berechtigungen: 'Issues: Read and write' (und ggf. 'Projects')")
        print("4. Kopieren Sie den generierten Token")
        print("\nSpeichermethoden:")
        print("A) Umgebungsvariable (empfohlen):")
        print("   export GITHUB_TOKEN=your_token_here")
        print("   (Fügen Sie dies zu ~/.bashrc oder ~/.zshrc hinzu)")
        print("\nB) Config-Datei:")
        print(f"   Speichern in ~/{CONFIG_FILE_NAME} (Berechtigung 600)")
        print("\n" + "=" * 60)
        
        choice = input("\nToken jetzt in Config-Datei speichern? [y/N]: ")
        
        if choice.lower() == 'y':
            # getpass: Token wird bei der Eingabe nicht angezeigt
            token = getpass.getpass("GitHub Token eingeben (Eingabe unsichtbar): ").strip()
            if token:
                config_path = GitHubSync.save_token(token)
                print(f"\n✅ Token gespeichert in {config_path}")
                print("⚠️  WICHTIG: Teilen Sie diese Datei niemals!")
                return True
        
        return False
