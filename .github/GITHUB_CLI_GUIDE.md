# GitHub CLI (gh) - Workflow Guide

Comprehensive guide for using GitHub CLI with vogel-video-analyzer project.

## 📋 Table of Contents

- [Installation & Setup](#installation--setup)
- [Repository Management](#repository-management)
- [Releases](#releases)
- [Pull Requests](#pull-requests)
- [GitHub Actions & Workflows](#github-actions--workflows)
- [Issues](#issues)
- [Gists & Secrets](#gists--secrets)
- [Useful Aliases](#useful-aliases)

---

## 🚀 Installation & Setup

### Installation

```bash
# Debian/Ubuntu
sudo apt install gh

# macOS
brew install gh

# Arch Linux
sudo pacman -S github-cli
```

### Authentication

```bash
# Login mit Browser
gh auth login

# Login mit Token
gh auth login --with-token < token.txt

# Status prüfen
gh auth status

# Zu anderem Account wechseln
gh auth switch
```

### Repository Setup

```bash
# Repository clonen
gh repo clone kamera-linux/vogel-video-analyzer

# In existierendem Repo arbeiten
cd vogel-video-analyzer
gh repo view
```

---

## 📦 Repository Management

### Repository Info

```bash
# Repository Details anzeigen
gh repo view

# Im Browser öffnen
gh repo view --web

# README anzeigen
gh repo view --readme

# Statistiken
gh repo view --json name,description,stargazerCount,forkCount,pushedAt
```

### Repository Bearbeiten

```bash
# Beschreibung ändern
gh repo edit --description "YOLOv26-based video analysis tool for automated bird content detection"

# Topics/Tags setzen
gh repo edit --add-topic machine-learning,bird-recognition,yolo

# Visibility ändern
gh repo edit --visibility public
```

---

## 🎯 Releases

### Release Erstellen

#### Einfaches Release

```bash
# Release aus aktuellem Tag erstellen
gh release create v0.1.15 \
  --title "Release v0.1.15: Enhanced Training & PNG Support" \
  --notes-file .github/release-v0.1.15.md

# Release mit Auto-Generated Notes
gh release create v0.1.16 \
  --generate-notes \
  --title "Release v0.1.16"
```

#### Release mit Assets

```bash
# Release mit Dateien
gh release create v0.1.15 \
  --title "Release v0.1.15" \
  --notes-file .github/release-v0.1.15.md \
  dist/vogel-trainer-*.whl \
  dist/vogel-trainer-*.tar.gz
```

#### Pre-Release & Draft

```bash
# Pre-Release (Beta/RC)
gh release create v0.2.0-beta.1 \
  --prerelease \
  --title "v0.2.0 Beta 1" \
  --notes "Beta release for testing"

# Draft Release (nicht öffentlich)
gh release create v0.2.0 \
  --draft \
  --title "v0.2.0 Draft" \
  --notes-file RELEASE_NOTES.md
```

### Release Management

```bash
# Alle Releases auflisten
gh release list

# Neuestes Release anzeigen
gh release view

# Spezifisches Release anzeigen
gh release view v0.1.15

# Release im Browser öffnen
gh release view v0.1.15 --web

# Release löschen
gh release delete v0.1.15 --yes

# Release bearbeiten
gh release edit v0.1.15 \
  --title "Updated Title" \
  --notes "Updated release notes"
```

### Release Assets

```bash
# Assets hochladen
gh release upload v0.1.15 \
  dist/*.whl \
  dist/*.tar.gz

# Assets herunterladen
gh release download v0.1.15

# Spezifisches Asset herunterladen
gh release download v0.1.15 --pattern "*.whl"

# Asset löschen
gh release delete-asset v0.1.15 vogel-trainer-0.1.15.whl
```

### Release Workflow (Komplett)

```bash
#!/bin/bash
# Complete release workflow

VERSION="v0.1.15"
NOTES_FILE=".github/release-${VERSION}.md"

# 1. Erstelle Tag lokal
git tag -a $VERSION -m "Release $VERSION"

# 2. Push Tag
git push origin $VERSION

# 3. Erstelle GitHub Release
gh release create $VERSION \
  --title "Release $VERSION: Enhanced Training & PNG Support" \
  --notes-file $NOTES_FILE \
  --verify-tag

# 4. Optional: Upload Assets
gh release upload $VERSION \
  dist/vogel_video_analyzer-*.whl \
  dist/vogel-video-analyzer-*.tar.gz

echo "✅ Release $VERSION created successfully!"
```

---

## 🔀 Pull Requests

### PR Erstellen

```bash
# PR aus aktuellem Branch erstellen
gh pr create \
  --title "Add crop-padding feature" \
  --body "Implements configurable padding for background removal" \
  --base main

# PR mit Template
gh pr create --fill

# PR mit Labels & Assignees
gh pr create \
  --title "Fix PNG transparency bug" \
  --body "Fixes #123" \
  --label bug,high-priority \
  --assignee @me \
  --reviewer username

# Draft PR
gh pr create --draft \
  --title "WIP: New training feature"
```

### PR Management

```bash
# Alle PRs auflisten
gh pr list

# Eigene PRs
gh pr list --author @me

# PRs mit Status
gh pr list --state open
gh pr list --state closed
gh pr list --state merged

# PR Details anzeigen
gh pr view 42

# PR im Browser öffnen
gh pr view 42 --web

# PR Diff anzeigen
gh pr diff 42

# PR Checks anzeigen
gh pr checks 42
```

### PR Bearbeiten

```bash
# PR Titel/Body ändern
gh pr edit 42 \
  --title "Updated Title" \
  --body "Updated description"

# Labels hinzufügen
gh pr edit 42 --add-label enhancement,documentation

# Reviewer hinzufügen
gh pr edit 42 --add-reviewer username

# Draft zu Ready umwandeln
gh pr ready 42

# PR schließen
gh pr close 42

# PR wieder öffnen
gh pr reopen 42
```

### PR Review

```bash
# Review abgeben
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Please fix XYZ"
gh pr review 42 --comment --body "Looks good, minor suggestions"

# PR mergen
gh pr merge 42 --merge
gh pr merge 42 --squash
gh pr merge 42 --rebase

# Auto-merge aktivieren
gh pr merge 42 --auto --squash

# PR auschecken lokal
gh pr checkout 42
```

### PR Workflow (Komplett)

```bash
#!/bin/bash
# Complete PR workflow

BRANCH="feature/crop-padding"
TITLE="Add crop-padding parameter for background removal"
BODY="Implements configurable padding around detected birds to preserve details like feet, beak, and feathers."

# 1. Branch erstellen und wechseln
git checkout -b $BRANCH

# 2. Änderungen machen
# ... code changes ...

# 3. Commit & Push
git add .
git commit -m "Add crop-padding feature"
git push -u origin $BRANCH

# 4. PR erstellen
gh pr create \
  --title "$TITLE" \
  --body "$BODY" \
  --label enhancement \
  --assignee @me \
  --base main

# 5. PR Status checken
gh pr checks

# 6. Nach Review: Merge
gh pr merge --squash --delete-branch
```

---

## ⚙️ GitHub Actions & Workflows

### Workflow Liste

```bash
# Alle Workflows anzeigen
gh workflow list

# Workflow mit Filter
gh workflow list --all

# Disabled Workflows anzeigen
gh workflow list --disabled
```

### Workflow Ausführen

```bash
# Workflow manuell triggern
gh workflow run tests.yml

# Workflow mit Inputs
gh workflow run release.yml \
  --field version=0.1.15 \
  --field environment=production

# Workflow auf bestimmtem Branch
gh workflow run tests.yml --ref feature-branch
```

### Workflow Status

```bash
# Workflow Runs auflisten
gh run list

# Letzte 10 Runs
gh run list --limit 10

# Runs für bestimmten Workflow
gh run list --workflow=tests.yml

# Runs mit Status
gh run list --status completed
gh run list --status failure

# Run Details anzeigen
gh run view 1234567890

# Run Logs anzeigen
gh run view 1234567890 --log

# Gescheiterten Run anzeigen
gh run view 1234567890 --log-failed
```

### Workflow Management

```bash
# Run neu starten
gh run rerun 1234567890

# Nur gescheiterte Jobs neu starten
gh run rerun 1234567890 --failed

# Run abbrechen
gh run cancel 1234567890

# Run Logs herunterladen
gh run download 1234567890

# Workflow aktivieren/deaktivieren
gh workflow enable tests.yml
gh workflow disable tests.yml

# Workflow im Browser öffnen
gh workflow view tests.yml --web
```

### Workflow Watch (Live-Monitoring)

```bash
# Aktuellen Run beobachten
gh run watch

# Spezifischen Run beobachten
gh run watch 1234567890

# Mit Details
gh run watch --interval 5
```

### Workflow Testing

```bash
#!/bin/bash
# Test workflow after changes

WORKFLOW="tests.yml"

# 1. Workflow triggern
echo "🚀 Triggering workflow: $WORKFLOW"
RUN_ID=$(gh workflow run $WORKFLOW --json id --jq .id)

# 2. Warten auf Start
echo "⏳ Waiting for workflow to start..."
sleep 5

# 3. Status beobachten
echo "👀 Watching workflow execution..."
gh run watch $RUN_ID

# 4. Ergebnis prüfen
STATUS=$(gh run view $RUN_ID --json conclusion --jq .conclusion)

if [ "$STATUS" = "success" ]; then
    echo "✅ Workflow completed successfully!"
else
    echo "❌ Workflow failed!"
    gh run view $RUN_ID --log-failed
    exit 1
fi
```

---

## 🐛 Issues

### Issue Erstellen

```bash
# Einfaches Issue
gh issue create \
  --title "PNG transparency not working with deduplicate" \
  --body "When using --deduplicate with --bg-transparent, images are saved as JPG"

# Issue mit Template
gh issue create --web

# Issue mit Labels
gh issue create \
  --title "Add support for RAW images" \
  --body "Feature request for RAW image support" \
  --label enhancement,feature-request \
  --assignee @me
```

### Issue Management

```bash
# Issues auflisten
gh issue list

# Offene Issues
gh issue list --state open

# Eigene Issues
gh issue list --assignee @me

# Issues mit Label
gh issue list --label bug

# Issue Details
gh issue view 123

# Issue im Browser
gh issue view 123 --web

# Issue schließen
gh issue close 123 --reason completed

# Issue wieder öffnen
gh issue reopen 123

# Issue kommentieren
gh issue comment 123 --body "Fixed in v0.1.15"
```

---

## 🔐 Gists & Secrets

### Gists

```bash
# Gist erstellen
gh gist create script.py --desc "Useful script"

# Öffentlichen Gist erstellen
gh gist create --public README.md

# Gist auflisten
gh gist list

# Gist anzeigen
gh gist view abc123

# Gist klonen
gh gist clone abc123
```

### Repository Secrets

```bash
# Secret erstellen (interaktiv)
gh secret set API_KEY

# Secret aus Datei
gh secret set API_KEY < api_key.txt

# Secret mit Wert
echo "secret-value" | gh secret set API_KEY

# Secrets auflisten
gh secret list

# Secret löschen
gh secret delete API_KEY
```

---

## 🔧 Useful Aliases

Erstelle Aliases in `~/.config/gh/config.yml`:

```yaml
aliases:
    # Release shortcuts
    release-create: release create --notes-file .github/release-$1.md
    release-latest: release view --json tagName,name,body --jq '{tag: .tagName, name: .name, notes: .body}'
    
    # PR shortcuts
    pr-mine: pr list --author @me
    pr-review: pr view --comments
    pr-merge-squash: pr merge --squash --delete-branch
    
    # Workflow shortcuts
    wf-list: workflow list
    wf-run: workflow run
    wf-watch: run watch
    wf-logs: run view --log-failed
    
    # Issue shortcuts
    issue-mine: issue list --assignee @me
    issue-bugs: issue list --label bug
    
    # Quick actions
    co: pr checkout
    view: repo view --web
    sync: '!git pull origin main && git fetch --all --tags'
```

### Verwendung:

```bash
# Release erstellen
gh release-create v0.1.15

# Eigene PRs anzeigen
gh pr-mine

# Workflow logs bei Fehler
gh wf-logs 1234567890

# PR checkout und review
gh co 42
gh pr-review
```

---

## 📝 Praktische Beispiele

### Release Workflow (Production)

```bash
#!/bin/bash
# production-release.sh - Complete production release

set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

echo "🚀 Starting release process for $VERSION"

# 1. Checks
echo "1️⃣ Running pre-release checks..."
git fetch --all --tags
if git tag | grep -q "^$VERSION$"; then
    echo "❌ Tag $VERSION already exists!"
    exit 1
fi

# 2. Run tests
echo "2️⃣ Running tests..."
gh workflow run tests.yml --ref main
sleep 10
LATEST_RUN=$(gh run list --workflow=tests.yml --limit 1 --json databaseId --jq .[0].databaseId)
gh run watch $LATEST_RUN || exit 1

# 3. Create tag
echo "3️⃣ Creating tag..."
git tag -a $VERSION -m "Release $VERSION"
git push origin $VERSION

# 4. Create release
echo "4️⃣ Creating GitHub release..."
gh release create $VERSION \
    --title "Release $VERSION" \
    --notes-file ".github/release-${VERSION}.md" \
    --verify-tag

# 5. Build & upload assets
echo "5️⃣ Building and uploading assets..."
python -m build
gh release upload $VERSION dist/*

echo "✅ Release $VERSION completed successfully!"
gh release view $VERSION --web
```

### PR Review Workflow

```bash
#!/bin/bash
# pr-review.sh - Review PR locally

PR_NUMBER=$1

if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <pr-number>"
    exit 1
fi

echo "📥 Checking out PR #$PR_NUMBER"
gh pr checkout $PR_NUMBER

echo "📊 PR Information:"
gh pr view $PR_NUMBER

echo "🔍 Running checks..."
gh pr checks $PR_NUMBER

echo "🧪 Running tests locally..."
pytest tests/

echo "📝 Review PR:"
echo "  Approve: gh pr review $PR_NUMBER --approve"
echo "  Request changes: gh pr review $PR_NUMBER --request-changes"
echo "  Comment: gh pr review $PR_NUMBER --comment"
```

### Workflow Monitoring Dashboard

```bash
#!/bin/bash
# workflow-status.sh - Monitor all workflows

echo "📊 GitHub Actions Status Dashboard"
echo "===================================="
echo ""

# Recent runs
echo "🏃 Recent Workflow Runs:"
gh run list --limit 5 --json number,conclusion,workflowName,createdAt \
    --jq '.[] | "\(.workflowName): \(.conclusion) (\(.createdAt))"'

echo ""

# Failed runs
echo "❌ Recent Failed Runs:"
gh run list --status failure --limit 3 --json number,workflowName,url \
    --jq '.[] | "  #\(.number) \(.workflowName): \(.url)"'

echo ""

# Active workflows
echo "⚙️  Active Workflows:"
gh workflow list --json name,state,path \
    --jq '.[] | select(.state=="active") | "  ✓ \(.name)"'
```

---

## 🎓 Best Practices

### 1. Authentication

- Nutze `gh auth login` für sichere Token-Speicherung
- Verwende unterschiedliche Accounts mit `gh auth switch`
- Token mit minimalen Permissions (Principle of Least Privilege)

### 2. Releases

- Immer Release Notes bereitstellen (`--notes-file`)
- Verwende semantische Versionierung (SemVer)
- Pre-Releases für Beta/RC markieren (`--prerelease`)
- Assets immer mit Upload (Wheels, Binaries)

### 3. Pull Requests

- Aussagekräftige Titel und Beschreibungen
- Labels für einfache Filterung
- Draft PRs für Work-in-Progress
- Auto-merge nur nach erfolgreichen Checks

### 4. Workflows

- Workflow-Ausführungen vor Merge testen
- Logs bei Fehlern prüfen (`--log-failed`)
- Secrets für sensitive Daten nutzen
- Workflow-Permissions minimal halten

### 5. Scripting

- Set `set -e` für Fehlerabbruch
- JSON output mit `jq` parsen (`--json`, `--jq`)
- Wrapper-Scripts für komplexe Workflows
- Aliase für häufige Befehle

---

## 📚 Weitere Ressourcen

- **Offizielle Dokumentation**: https://cli.github.com/manual/
- **GitHub API**: https://docs.github.com/en/rest
- **gh Cookbook**: https://cli.github.com/examples
- **Community Discussions**: https://github.com/cli/cli/discussions

---

**Version**: 1.0  
**Letzte Aktualisierung**: 17. November 2025  
**Projekt**: vogel-video-analyzer
