# Release v0.5.4 - GitHub Project Board Integration

**Release Date:** 31. Januar 2026

## 🎯 Highlights

Diese Version erweitert das Issue Board System um **vollständige GitHub Project Board Integration** und behebt wichtige Synchronisationsprobleme.

## ✨ Neue Features

### GitHub Project Board Synchronisation
- **Automatische Status-Updates** vom Project Board zu lokalen Issues
- **GraphQL API Integration** für effizientes Abrufen von Project Board Daten
- **Custom Fields Support**: Status und Priority mit Emoji-Indikatoren
- **Bidirektionale Synchronisation**: Local ↔ GitHub Issues ↔ Project Board

### Status-Indikatoren
- 📋 **Todo**: Noch nicht begonnen
- ⚙️ **In Progress**: Wird aktiv bearbeitet
- ✅ **Done**: Abgeschlossen
- 🚫 **Blocked**: Blockiert durch Abhängigkeiten

## 🐛 Bugfixes

### GitHub Synchronisation
- ✅ **Duplikate verhindert**: Issues werden nicht mehr doppelt erstellt
- ✅ **GitHub Issue Tracking**: Verbesserte Zuordnung über URL-Links statt nur Titel
- ✅ **Geschlossene Issues**: Korrekte Zuordnung zu "done" Status
- ✅ **Assignee Handling**: `None`-Werte werden jetzt korrekt behandelt
- ✅ **Issue Matching**: Robustere Erkennung über GitHub-Links

### Synchronisations-Logik
- Lokale Issues erhalten nach dem ersten Push automatisch GitHub-Links
- Titel-basiertes Matching wurde durch URL-basiertes Matching ersetzt
- Verbesserte Fehlerbehandlung und Debug-Ausgaben

## 🔄 Änderungen

### Status-Priorität
Die Reihenfolge für Status-Ermittlung wurde optimiert:
1. **Project Board Status** (höchste Priorität)
2. **GitHub Issue State** (open/closed)
3. **GitHub Labels** (niedrigste Priorität)

### Synchronisation
- `vogel-issues sync` synchronisiert jetzt standardmäßig auch Project Board Status
- Bessere Ausgabe beim Sync-Vorgang mit Status-Änderungen
- Erweiterte Statistiken: `project_synced` Counter

## 📋 Verwendung

### Lokales Issue zu GitHub pushen
```bash
vogel-issues create "Mein Issue" "Beschreibung" --priority high
vogel-issues sync --direction push
```

### GitHub Issues lokal synchronisieren
```bash
vogel-issues sync --direction pull
```

### Vollständige Synchronisation (inkl. Project Board)
```bash
vogel-issues sync
```

## 🔧 Technische Details

### Neue Funktionen
- `GitHubSync._graphql_query()`: GraphQL API Integration
- `GitHubSync._load_project_data()`: Project Board Metadaten abrufen
- `GitHubSync._get_project_item_status()`: Status eines Issues im Project Board
- Verbesserte `push_issue()` mit automatischer Link-Aktualisierung
- Erweiterte `sync_all()` mit Project Board Support

### Abhängigkeiten
- `requests` für GraphQL API Calls (bereits durch PyGithub installiert)
- GitHub Personal Access Token mit `repo` und `project` Scopes erforderlich

## 📚 Dokumentation

Die vollständige Dokumentation finden Sie in:
- [ISSUE_BOARD.md](../docs/ISSUE_BOARD.md) - Komplette Feature-Dokumentation
- [GITHUB_SYNC_QUICKSTART.md](../docs/GITHUB_SYNC_QUICKSTART.md) - Schnellstart-Guide
- [CHANGELOG.md](../CHANGELOG.md) - Detaillierte Änderungshistorie

## 🙏 Danksagung

Vielen Dank an alle Benutzer für das Feedback zum Issue Board System!

## 📦 Installation

```bash
pip install --upgrade vogel-video-analyzer[github]
```

Oder aus dem Repository:
```bash
git clone https://github.com/kamera-linux/vogel-video-analyzer.git
cd vogel-video-analyzer
pip install -e ".[github]"
```

## 🔗 Links

- **GitHub Release**: https://github.com/kamera-linux/vogel-video-analyzer/releases/tag/v0.5.4
- **PyPI Package**: https://pypi.org/project/vogel-video-analyzer/
- **Dokumentation**: https://github.com/kamera-linux/vogel-video-analyzer/tree/main/docs
- **Issue Board**: https://github.com/users/kamera-linux/projects/3

---

**Full Changelog**: https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.5.3...v0.5.4
