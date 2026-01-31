# 📋 Issue Board für vogel-video-analyzer

Ein integriertes Issue-Management-System für das vogel-video-analyzer Projekt.

## 🌟 Features

- ✅ **Issue-Verwaltung**: Erstellen, Anzeigen, Aktualisieren und Löschen von Issues
- 🏷️ **Status-Tracking**: Todo, In Progress, Done, Blocked
- 🎯 **Prioritäten**: Low, Medium, High, Critical
- 🏴 **Labels**: Flexible Kategorisierung mit mehreren Labels
- 👤 **Assignees**: Zuweisen von Issues an Personen
- 📊 **Statistiken**: Übersicht über alle Issues nach Status und Priorität
- 💾 **JSON-Speicherung**: Einfache, portable Datenspeicherung
- 🎨 **Farbiges CLI**: Übersichtliche Terminal-Ausgabe mit Emojis und Farben
- 🔄 **GitHub-Synchronisation**: Bidirektionale Synchronisation mit GitHub Issues (optional)

## 🚀 Installation

Das Issue Board ist bereits im vogel-video-analyzer Paket enthalten. Nach der Installation steht der `vogel-issues` Befehl zur Verfügung:

```bash
pip install -e .
```

### GitHub-Synchronisation (optional)

Für die Synchronisation mit GitHub Issues:

```bash
pip install -e .[github]
```

Oder:

```bash
pip install PyGithub
```

## 📖 Verwendung

### Issue erstellen

```bash
# Einfaches Issue
vogel-issues create "Video-Export fehlerhaft" "Der Video-Export schlägt bei großen Dateien fehl"

# Mit zusätzlichen Optionen
vogel-issues create "Performance verbessern" "YOLO-Modell beschleunigen" \
  --status todo \
  --priority high \
  --labels performance optimization \
  --assignee Alice
```

### Issues auflisten

```bash
# Alle Issues
vogel-issues list

# Mit Beschreibungen
vogel-issues list -v

# Nach Status filtern
vogel-issues list --status todo
vogel-issues list --status in_progress

# Nach Priorität filtern
vogel-issues list --priority high

# Nach Label filtern
vogel-issues list --label bug

# Nach Assignee filtern
vogel-issues list --assignee Alice

# Sortieren
vogel-issues list --sort priority
vogel-issues list --sort status
```

### Issue anzeigen

```bash
# Detaillierte Ansicht eines Issues
vogel-issues show 1
```

### Issue aktualisieren

```bash
# Status ändern
vogel-issues update 1 --status in_progress

# Priorität ändern
vogel-issues update 2 --priority critical

# Mehrere Felder gleichzeitig
vogel-issues update 3 \
  --status done \
  --title "Neuer Titel" \
  --assignee Bob
```

### Issue löschen

```bash
# Mit Bestätigung
vogel-issues delete 1

# Ohne Bestätigung
vogel-issues delete 1 --force
```

### Statistiken anzeigen

```bash
vogel-issues stats
```

## 🔄 GitHub-Synchronisation

### Token einrichten

Es gibt **drei Methoden**, um Ihren GitHub Token bereitzustellen:

#### 1. Umgebungsvariable (empfohlen)

```bash
export GITHUB_TOKEN="ghp_your_token_here"
# Dauerhaft machen (in ~/.bashrc oder ~/.zshrc):
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
```

#### 2. Config-Datei

```bash
# Interaktive Einrichtung
vogel-issues setup

# Oder manuell ~/.vogel_config.json erstellen:
{
  "github_token": "ghp_your_token_here"
}
```

#### 3. CLI-Parameter

```bash
vogel-issues sync --github-token "ghp_your_token_here"
```

### Token erstellen

1. Gehen Sie zu: https://github.com/settings/tokens
2. Klicken Sie auf **"Generate new token (classic)"**
3. Wählen Sie **"repo"** scope (voller Repository-Zugriff)
4. Kopieren Sie den generierten Token

### Issues synchronisieren

```bash
# Bidirektionale Synchronisation (lokal ↔️ GitHub)
vogel-issues sync

# Nur zu GitHub pushen
vogel-issues sync --direction push

# Nur von GitHub holen
vogel-issues sync --direction pull

# Spezifisches Repository
vogel-issues sync --repo "username/repository"

# Mit Token-Parameter
vogel-issues sync --github-token "ghp_..."
```

### Wie funktioniert die Synchronisation?

**Push (lokal → GitHub):**
- Erstellt neue GitHub Issues für lokale Issues
- Aktualisiert existierende GitHub Issues
- Verwendet Labels für Status und Priorität:
  - `status: todo`, `status: in progress`, `status: done`, `status: blocked`
  - `priority: low`, `priority: medium`, `priority: high`, `priority: critical`
- Schließt GitHub Issues automatisch wenn Status = "done"

**Pull (GitHub → lokal):**
- Importiert GitHub Issues als lokale Issues
- Extrahiert Status und Priorität aus Labels
- Aktualisiert existierende lokale Issues
- Behält GitHub Issue Number als Referenz

**Automatische Repository-Erkennung:**
Das System erkennt automatisch das GitHub Repository aus der Git-Konfiguration (`git config remote.origin.url`).

## 📂 Speicherort

Issues werden standardmäßig in `~/.vogel_issues.json` gespeichert. Ein benutzerdefinierter Speicherort kann mit `--storage` angegeben werden:

```bash
vogel-issues --storage ./my-issues.json list
```

## 🎯 Status-Typen

- **todo**: Issue ist noch nicht begonnen
- **in_progress**: Issue wird gerade bearbeitet
- **done**: Issue ist abgeschlossen
- **blocked**: Issue ist blockiert und kann nicht fortgesetzt werden

## 📊 Prioritäten

- **low**: Niedrige Priorität
- **medium**: Normale Priorität (Standard)
- **high**: Hohe Priorität
- **critical**: Kritische Priorität, sofortige Bearbeitung erforderlich

## 💡 Beispiel-Workflow

```bash
# 1. Bug-Report erstellen
vogel-issues create "Fehler bei Spezies-Erkennung" \
  "Die Spezies-Erkennung liefert falsche Ergebnisse für Amseln" \
  --priority high \
  --labels bug species-detection \
  --status todo

# 2. Feature-Request erstellen
vogel-issues create "Export zu CSV hinzufügen" \
  "Möglichkeit zum Export der Ergebnisse als CSV-Datei" \
  --priority medium \
  --labels enhancement feature-request

# 3. Issues anzeigen
vogel-issues list --sort priority

# 4. Issue in Bearbeitung nehmen
vogel-issues update 1 --status in_progress --assignee "Dev Team"

# 5. Statistik anzeigen
vogel-issues stats

# 6. Erledigte Issues filtern
vogel-issues list --status done
```

## 🔧 Entwicklung

### Tests ausführen

```bash
pytest tests/test_issue_board.py -v
```

### Alle Tests mit Coverage

```bash
pytest tests/test_issue_board.py --cov=vogel_video_analyzer.issue_board
```

## 📝 Datenformat

Issues werden als JSON gespeichert:

```json
[
  {
    "id": 1,
    "title": "Video-Export fehlerhaft",
    "description": "Der Video-Export schlägt bei großen Dateien fehl",
    "status": "in_progress",
    "priority": "high",
    "labels": ["bug", "video-export"],
    "created_at": "2026-01-31T10:30:00",
    "updated_at": "2026-01-31T11:45:00",
    "assignee": "Alice"
  }
]
```

## 🤝 Integration mit Git

Das Issue Board kann gut mit Git-Workflows kombiniert werden:

```bash
# Branch für Issue erstellen
vogel-issues show 1
git checkout -b issue-1-video-export-fix

# Nach Abschluss
git commit -m "Fix #1: Video-Export für große Dateien repariert"
vogel-issues update 1 --status done
```

## 🔐 Sicherheit

- Issues werden lokal gespeichert
- **GitHub Token Sicherheit:**
  - Token wird niemals im Klartext geloggt
  - Config-Datei erhält automatisch sichere Berechtigungen (chmod 600)
  - Token kann in Umgebungsvariable gespeichert werden
  - **WICHTIG:** Teilen Sie Ihren Token niemals öffentlich!
- Einfaches Backup durch Kopieren der JSON-Datei
- Versionskontrolle der Issue-Datei möglich (aber Token ausschließen!)

## 📦 API-Nutzung

Das Issue Board kann auch programmatisch verwendet werden:

```python
from vogel_video_analyzer.issue_board import IssueBoard

# Board initialisieren
board = IssueBoard()

# Issue erstellen
issue = board.create_issue(
    title="Test Issue",
    description="Test Beschreibung",
    priority="high",
    labels=["test", "automation"]
)

# Issues auflisten
issues = board.list_issues(status="todo")

# Issue aktualisieren
board.update_issue(issue.id, status="done")

# Statistiken
stats = board.get_statistics()
print(f"Gesamt: {stats['total']} Issues")
```

## 🎨 Farben und Symbole

Das CLI verwendet Farben und Emojis für bessere Übersicht:

- 📋 **TODO** (Gelb)
- ⚙️ **IN PROGRESS** (Blau)
- ✅ **DONE** (Grün)
- 🚫 **BLOCKED** (Rot)

Prioritäten:
- 🔵 **Low** (Cyan)
- 🟡 **Medium** (Gelb)
- 🟠 **High** (Magenta)
- 🔴 **Critical** (Rot)

## 📄 Lizenz

MIT License - siehe [LICENSE](../../../LICENSE)
