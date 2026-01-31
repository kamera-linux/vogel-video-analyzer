"""
CLI für das Issue Board System
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .issue_board import IssueBoard, IssueStatus, IssuePriority


# Farben für Terminal-Ausgabe
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


def format_status(status: IssueStatus) -> str:
    """Formatiert Status mit Farbe"""
    colors = {
        "todo": f"{Colors.YELLOW}📋 TODO{Colors.RESET}",
        "in_progress": f"{Colors.BLUE}⚙️  IN PROGRESS{Colors.RESET}",
        "done": f"{Colors.GREEN}✅ DONE{Colors.RESET}",
        "blocked": f"{Colors.RED}🚫 BLOCKED{Colors.RESET}"
    }
    return colors.get(status, status)


def format_priority(priority: IssuePriority) -> str:
    """Formatiert Priorität mit Farbe"""
    colors = {
        "low": f"{Colors.CYAN}🔵 Low{Colors.RESET}",
        "medium": f"{Colors.YELLOW}🟡 Medium{Colors.RESET}",
        "high": f"{Colors.MAGENTA}🟠 High{Colors.RESET}",
        "critical": f"{Colors.RED}🔴 Critical{Colors.RESET}"
    }
    return colors.get(priority, priority)


def print_issue(board: IssueBoard, issue_id: int):
    """Gibt ein einzelnes Issue detailliert aus"""
    issue = board.get_issue(issue_id)
    if not issue:
        print(f"{Colors.RED}❌ Issue #{issue_id} nicht gefunden{Colors.RESET}")
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}Issue #{issue.id}: {issue.title}{Colors.RESET}")
    print(f"Status:       {format_status(issue.status)}")
    print(f"Priorität:    {format_priority(issue.priority)}")
    print(f"Erstellt:     {issue.created_at}")
    print(f"Aktualisiert: {issue.updated_at}")
    
    if issue.assignee:
        print(f"Zugewiesen:   {issue.assignee}")
    
    if issue.labels:
        labels_str = ", ".join([f"{Colors.CYAN}{label}{Colors.RESET}" for label in issue.labels])
        print(f"Labels:       {labels_str}")
    
    print(f"\n{Colors.BOLD}Beschreibung:{Colors.RESET}")
    print(issue.description)
    print()


def print_issues_table(issues, show_description: bool = False):
    """Gibt Issues als Tabelle aus"""
    if not issues:
        print(f"{Colors.YELLOW}ℹ️  Keine Issues gefunden{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}{'ID':<6} {'Titel':<40} {'Status':<20} {'Priorität':<20}{Colors.RESET}")
    print("=" * 86)
    
    for issue in issues:
        title = issue.title[:37] + "..." if len(issue.title) > 40 else issue.title
        print(f"{issue.id:<6} {title:<40} {format_status(issue.status):<30} {format_priority(issue.priority):<30}")
        
        if show_description and issue.description:
            desc = issue.description[:100] + "..." if len(issue.description) > 100 else issue.description
            print(f"       {Colors.CYAN}{desc}{Colors.RESET}")
    
    print()


def cmd_create(args):
    """Erstellt ein neues Issue"""
    board = IssueBoard(args.storage)
    
    issue = board.create_issue(
        title=args.title,
        description=args.description,
        status=args.status or "todo",
        priority=args.priority or "medium",
        labels=args.labels or [],
        assignee=args.assignee
    )
    
    print(f"{Colors.GREEN}✅ Issue #{issue.id} erstellt: {issue.title}{Colors.RESET}")


def cmd_list(args):
    """Listet Issues auf"""
    board = IssueBoard(args.storage)
    
    issues = board.list_issues(
        status=args.status,
        priority=args.priority,
        label=args.label,
        assignee=args.assignee
    )
    
    # Sortierung
    if args.sort == "id":
        issues.sort(key=lambda x: x.id)
    elif args.sort == "priority":
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        issues.sort(key=lambda x: priority_order.get(x.priority, 4))
    elif args.sort == "status":
        issues.sort(key=lambda x: x.status)
    
    print_issues_table(issues, show_description=args.verbose)


def cmd_show(args):
    """Zeigt ein einzelnes Issue an"""
    board = IssueBoard(args.storage)
    print_issue(board, args.id)


def cmd_update(args):
    """Aktualisiert ein Issue"""
    board = IssueBoard(args.storage)
    
    kwargs = {}
    if args.title:
        kwargs['title'] = args.title
    if args.description:
        kwargs['description'] = args.description
    if args.status:
        kwargs['status'] = args.status
    if args.priority:
        kwargs['priority'] = args.priority
    if args.labels:
        kwargs['labels'] = args.labels
    if args.assignee:
        kwargs['assignee'] = args.assignee
    
    issue = board.update_issue(args.id, **kwargs)
    
    if issue:
        print(f"{Colors.GREEN}✅ Issue #{issue.id} aktualisiert{Colors.RESET}")
        print_issue(board, issue.id)
    else:
        print(f"{Colors.RED}❌ Issue #{args.id} nicht gefunden{Colors.RESET}")
        sys.exit(1)


def cmd_delete(args):
    """Löscht ein Issue"""
    board = IssueBoard(args.storage)
    
    if not args.force:
        issue = board.get_issue(args.id)
        if issue:
            print(f"{Colors.YELLOW}⚠️  Issue #{issue.id} löschen: {issue.title}?{Colors.RESET}")
            confirm = input("Bestätigen [y/N]: ")
            if confirm.lower() != 'y':
                print("Abgebrochen")
                return
    
    if board.delete_issue(args.id):
        print(f"{Colors.GREEN}✅ Issue #{args.id} gelöscht{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Issue #{args.id} nicht gefunden{Colors.RESET}")
        sys.exit(1)


def cmd_stats(args):
    """Zeigt Statistiken an"""
    board = IssueBoard(args.storage)
    stats = board.get_statistics()
    
    print(f"\n{Colors.BOLD}📊 Issue Board Statistiken{Colors.RESET}")
    print("=" * 40)
    print(f"Gesamt: {stats['total']} Issues\n")
    
    print(f"{Colors.BOLD}Nach Status:{Colors.RESET}")
    for status, count in stats['by_status'].items():
        if count > 0:
            print(f"  {format_status(status)}: {count}")
    
    print(f"\n{Colors.BOLD}Nach Priorität:{Colors.RESET}")
    for priority, count in stats['by_priority'].items():
        if count > 0:
            print(f"  {format_priority(priority)}: {count}")
    
    print()


def cmd_sync(args):
    """Synchronisiert mit GitHub Issues"""
    try:
        from .github_sync import GitHubSync
    except ImportError:
        print(f"{Colors.RED}❌ PyGithub ist nicht installiert{Colors.RESET}")
        print("Installieren Sie es mit: pip install PyGithub")
        sys.exit(1)
    
    board = IssueBoard(args.storage)
    
    # Token-Setup wenn gewünscht
    if args.setup_token:
        GitHubSync.setup_token_interactive()
        return
    
    try:
        # Initialisiere GitHub Sync
        sync = GitHubSync(token=args.github_token, repo=args.repo)
        
        print(f"{Colors.CYAN}🔄 Synchronisiere mit GitHub Repository: {sync.repo_name}{Colors.RESET}\n")
        
        # Synchronisation durchführen
        stats = sync.sync_all(board, direction=args.direction)
        
        # Ergebnisse anzeigen
        print(f"{Colors.GREEN}✅ Synchronisation abgeschlossen{Colors.RESET}")
        if stats['pushed'] > 0:
            print(f"   ⬆️  {stats['pushed']} Issues zu GitHub gepusht")
        if stats['pulled'] > 0:
            print(f"   ⬇️  {stats['pulled']} Issues von GitHub geholt")
        if stats.get('project_synced', 0) > 0:
            print(f"   📊 {stats['project_synced']} Issue Status vom Project Board aktualisiert")
        
        if stats['errors']:
            print(f"\n{Colors.YELLOW}⚠️  Warnungen:{Colors.RESET}")
            for error in stats['errors']:
                print(f"   {error}")
        
        print()
        
    except ValueError as e:
        print(f"{Colors.RED}❌ Fehler: {e}{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unerwarteter Fehler: {e}{Colors.RESET}")
        sys.exit(1)


def cmd_setup(args):
    """Richtet GitHub Token ein"""
    try:
        from .github_sync import GitHubSync
        GitHubSync.setup_token_interactive()
    except ImportError:
        print(f"{Colors.RED}❌ PyGithub ist nicht installiert{Colors.RESET}")
        print("Installieren Sie es mit: pip install PyGithub")
        sys.exit(1)


def main():
    """Hauptfunktion für CLI"""
    parser = argparse.ArgumentParser(
        prog='vogel-issues',
        description='Issue Board für vogel-video-analyzer Projekt-Management',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--storage',
        type=Path,
        help='Pfad zur Issue-Speicherdatei (Standard: ~/.vogel_issues.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Kommandos')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Erstellt ein neues Issue')
    create_parser.add_argument('title', help='Issue-Titel')
    create_parser.add_argument('description', help='Issue-Beschreibung')
    create_parser.add_argument('--status', choices=['todo', 'in_progress', 'done', 'blocked'], help='Status')
    create_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], help='Priorität')
    create_parser.add_argument('--labels', nargs='+', help='Labels')
    create_parser.add_argument('--assignee', help='Zugewiesene Person')
    
    # List command
    list_parser = subparsers.add_parser('list', help='Listet Issues auf')
    list_parser.add_argument('--status', choices=['todo', 'in_progress', 'done', 'blocked'], help='Filter nach Status')
    list_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], help='Filter nach Priorität')
    list_parser.add_argument('--label', help='Filter nach Label')
    list_parser.add_argument('--assignee', help='Filter nach Assignee')
    list_parser.add_argument('--sort', choices=['id', 'priority', 'status'], default='id', help='Sortierung')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Zeige Beschreibungen')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Zeigt ein Issue im Detail')
    show_parser.add_argument('id', type=int, help='Issue-ID')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Aktualisiert ein Issue')
    update_parser.add_argument('id', type=int, help='Issue-ID')
    update_parser.add_argument('--title', help='Neuer Titel')
    update_parser.add_argument('--description', help='Neue Beschreibung')
    update_parser.add_argument('--status', choices=['todo', 'in_progress', 'done', 'blocked'], help='Neuer Status')
    update_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], help='Neue Priorität')
    update_parser.add_argument('--labels', nargs='+', help='Neue Labels')
    update_parser.add_argument('--assignee', help='Neue zugewiesene Person')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Löscht ein Issue')
    delete_parser.add_argument('id', type=int, help='Issue-ID')
    delete_parser.add_argument('-f', '--force', action='store_true', help='Ohne Bestätigung löschen')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Zeigt Statistiken')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Synchronisiert mit GitHub Issues')
    sync_parser.add_argument('--direction', choices=['push', 'pull', 'both'], default='both',
                            help='Synchronisationsrichtung (Standard: both)')
    sync_parser.add_argument('--github-token', help='GitHub Personal Access Token')
    sync_parser.add_argument('--repo', help='Repository im Format "owner/repo"')
    sync_parser.add_argument('--setup-token', action='store_true', 
                            help='Interaktive Token-Einrichtung')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Richtet GitHub Token ein')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Kommandos ausführen
    commands = {
        'create': cmd_create,
        'list': cmd_list,
        'show': cmd_show,
        'update': cmd_update,
        'delete': cmd_delete,
        'stats': cmd_stats,
        'sync': cmd_sync,
        'setup': cmd_setup
    }
    
    commands[args.command](args)


if __name__ == '__main__':
    main()
