# GitHub-Synchronisation - Schnellstart

## 🚀 Erste Schritte

### 1. Installation

```bash
cd /run/media/imme/ENCRYPTSSD/daten/git/kamera-linux-github/vogel-video-analyzer
pip install -e .[github]
```

### 2. GitHub Token erstellen

1. Gehen Sie zu: https://github.com/settings/tokens
2. Klicken Sie auf **"Generate new token (classic)"**
3. Geben Sie einen Namen ein (z.B. "vogel-issues-sync")
4. Wählen Sie **"repo"** scope (vollständiger Zugriff auf Repositories)
5. Klicken Sie auf **"Generate token"**
6. **Kopieren Sie den Token sofort** (wird nur einmal angezeigt!)

### 3. Token einrichten

**Option A: Umgebungsvariable (empfohlen für Entwicklung)**

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Dauerhaft machen:
echo 'export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> ~/.bashrc
source ~/.bashrc
```

**Option B: Config-Datei (empfohlen für Produktion)**

```bash
vogel-issues setup
# Folgen Sie den Anweisungen und geben Sie Ihren Token ein
```

**Option C: CLI-Parameter (für einmalige Nutzung)**

```bash
vogel-issues sync --github-token "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## 📋 Verwendungsbeispiele

### Lokale Issues zu GitHub pushen

```bash
# Alle lokalen Issues zu GitHub Issues konvertieren
vogel-issues sync --direction push
```

### GitHub Issues lokal importieren

```bash
# Alle GitHub Issues herunterladen
vogel-issues sync --direction pull
```

### Bidirektionale Synchronisation

```bash
# Synchronisiert in beide Richtungen (Standard)
vogel-issues sync
```

### Spezifisches Repository

```bash
# Wenn Sie nicht im Git-Repository sind oder ein anderes Repository verwenden möchten
vogel-issues sync --repo "kamera-linux/vogel-video-analyzer"
```

## 🔄 Workflow-Beispiele

### Workflow 1: Lokale Entwicklung → GitHub

```bash
# 1. Lokale Issues erstellen
vogel-issues create "Bug: Videoexport fehlerhaft" \
  "Der Export schlägt bei großen Dateien fehl" \
  --priority high \
  --labels bug video-export

vogel-issues create "Feature: CSV Export" \
  "Ergebnisse als CSV exportieren" \
  --priority medium \
  --labels enhancement

# 2. Lokale Issues ansehen
vogel-issues list

# 3. Zu GitHub pushen
vogel-issues sync --direction push

# Ergebnis: Neue Issues auf GitHub mit korrekten Labels
```

### Workflow 2: GitHub → Lokale Verwaltung

```bash
# 1. GitHub Issues importieren
vogel-issues sync --direction pull

# 2. Lokal bearbeiten
vogel-issues update 1 --status in_progress --assignee "Dein Name"

# 3. Zurück zu GitHub pushen
vogel-issues sync --direction push

# Ergebnis: GitHub Issue ist aktualisiert
```

### Workflow 3: Team-Synchronisation

```bash
# Morgens: Neueste Issues von GitHub holen
vogel-issues sync --direction pull

# Arbeiten...
vogel-issues update 5 --status done

# Abends: Änderungen zu GitHub pushen
vogel-issues sync --direction push
```

## 📊 Labels und Status

### Automatische Label-Konvertierung

**Status → GitHub Labels:**
- `todo` → `status: todo`
- `in_progress` → `status: in progress`
- `done` → `status: done`
- `blocked` → `status: blocked`

**Priorität → GitHub Labels:**
- `low` → `priority: low`
- `medium` → `priority: medium`
- `high` → `priority: high`
- `critical` → `priority: critical`

### Beispiel

```bash
# Lokales Issue mit Status und Priorität
vogel-issues create "Test" "Test Beschreibung" \
  --status in_progress \
  --priority high \
  --labels bug security

# Nach Sync auf GitHub:
# Labels: "status: in progress", "priority: high", "bug", "security"
```

## 🔍 Troubleshooting

### Problem: "GitHub Token nicht gefunden"

```bash
# Prüfen Sie Umgebungsvariable
echo $GITHUB_TOKEN

# Oder verwenden Sie CLI-Parameter
vogel-issues sync --github-token "your_token"
```

### Problem: "Repository nicht gefunden"

```bash
# Prüfen Sie Git-Konfiguration
git config --get remote.origin.url

# Oder geben Sie Repository explizit an
vogel-issues sync --repo "owner/repository"
```

### Problem: "Permission denied"

- Stellen Sie sicher, dass Ihr Token **"repo"** Berechtigung hat
- Erstellen Sie einen neuen Token mit korrekten Berechtigungen

### Problem: "PyGithub nicht installiert"

```bash
pip install PyGithub
# Oder
pip install -e .[github]
```

## ⚠️ Wichtige Hinweise

### Token-Sicherheit

- ⛔ **NIE** Token in Git committen
- ⛔ **NIE** Token in Logs ausgeben
- ⛔ **NIE** Token öffentlich teilen
- ✅ Verwenden Sie `.gitignore` für Config-Dateien:

```bash
# Fügen Sie zu .gitignore hinzu:
echo ".vogel_config.json" >> .gitignore
```

### Rate Limits

GitHub API hat Rate Limits:
- **Authentifiziert**: 5.000 Requests/Stunde
- **Nicht authentifiziert**: 60 Requests/Stunde

Bei vielen Issues kann die Synchronisation langsam sein.

### Konfliktauflösung

Die Synchronisation ist **nicht-destruktiv**:
- Lokale Issues werden **nicht** gelöscht
- GitHub Issues werden **nicht** gelöscht
- Updates überschreiben vorherige Werte

Bei Konflikten gilt:
- `push`: Lokale Version gewinnt
- `pull`: GitHub Version gewinnt
- `both`: Letzte Synchronisationsrichtung gewinnt

## 🎯 Best Practices

### 1. Regelmäßige Synchronisation

```bash
# Cronjob für tägliche Synchronisation
0 9 * * * cd /path/to/vogel-video-analyzer && vogel-issues sync
```

### 2. Backup vor Sync

```bash
# Backup erstellen
cp ~/.vogel_issues.json ~/.vogel_issues.backup.json

# Synchronisieren
vogel-issues sync

# Bei Problemen: Restore
cp ~/.vogel_issues.backup.json ~/.vogel_issues.json
```

### 3. Git-Integration

```bash
# .gitignore
.vogel_config.json
.vogel_issues.json.backup

# Versioniere nur öffentliche Issues
git add .vogel_issues.json
git commit -m "Update issues"
```

## 📝 Beispiel-Szenario

**Szenario**: Bug auf GitHub gemeldet, lokal bearbeiten, zurück synchronisieren

```bash
# 1. GitHub Issues holen
vogel-issues sync --direction pull
vogel-issues list --label bug

# 2. Bug lokal analysieren und Issue aktualisieren
vogel-issues show 42
vogel-issues update 42 \
  --status in_progress \
  --assignee "Dein Name" \
  --labels bug critical reproduction-steps

# 3. Nach Bugfix: Status ändern
vogel-issues update 42 --status done

# 4. Zurück zu GitHub
vogel-issues sync --direction push

# Ergebnis: GitHub Issue #42 ist geschlossen und aktualisiert
```

## 🔗 Weitere Ressourcen

- [GitHub Personal Access Tokens Dokumentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [PyGithub Dokumentation](https://pygithub.readthedocs.io/)
- [Issue Board Hauptdokumentation](ISSUE_BOARD.md)
