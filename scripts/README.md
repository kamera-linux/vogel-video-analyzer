# Scripts

Automation scripts for vogel-video-analyzer development and release management.

## 📦 create_github_release.py

Automated GitHub release creation from Git tags with PyPI workflow monitoring.

### Features

- 🏷️ Auto-detects latest Git tag or uses specified tag
- 📝 Finds and uses release notes from `.github/RELEASE_v*.md`
- 🚀 Creates GitHub release via `gh` CLI
- 📊 Monitors PyPI publish workflow status
- ⚡ Supports draft and pre-release options
- 🔄 Handles existing releases (delete/recreate)
- ✅ Validates tag format and remote sync

### Usage

```bash
# Use latest tag
python scripts/create_github_release.py

# Specific tag
python scripts/create_github_release.py v0.3.1

# Create as draft
python scripts/create_github_release.py --draft

# Mark as pre-release
python scripts/create_github_release.py v0.4.0-beta.1 --prerelease

# Custom title
python scripts/create_github_release.py --title "Major Update v0.4.0"

# Skip confirmations
python scripts/create_github_release.py --force
```

### Requirements

- GitHub CLI (`gh`) installed and authenticated
- Git repository with tags
- Release notes in `.github/RELEASE_v*.md` (optional)

### Options

```
positional arguments:
  tag                   Git tag to release (default: latest tag)

optional arguments:
  --draft              Create release as draft
  --prerelease         Mark release as pre-release
  --title TITLE        Custom release title
  --notes-dir DIR      Directory for release notes (default: .github)
  --force              Skip all confirmation prompts
```

### Workflow

1. Detects/validates Git tag (e.g., `v0.3.1`)
2. Checks if tag exists locally and on remote
3. Searches for release notes: `.github/RELEASE_v0.3.1.md`
4. Extracts title from notes or generates default
5. Creates GitHub release with notes
6. Monitors PyPI publish workflow (if triggered)

### Example Output

```
🎯 GitHub Release Creator
============================================================

🔍 Searching for latest Git tag...
✅ Found latest tag: v0.3.1
✅ Tag exists on remote
📝 Looking for release notes file...
✅ Found release notes: .github/RELEASE_v0.3.1.md
📋 Extracted title: v0.3.1 - Summary Video Feature

📊 Release Summary:
============================================================
Tag:         v0.3.1
Title:       v0.3.1 - Summary Video Feature
Notes:       .github/RELEASE_v0.3.1.md
Draft:       False
Pre-release: False
============================================================

Create this release? [y/N]: y

🚀 Creating GitHub release for v0.3.1...
✅ Release created: https://github.com/kamera-linux/vogel-video-analyzer/releases/tag/v0.3.1

============================================================
Checking for PyPI publish workflow...
============================================================
✅ Workflow found for v0.3.1 (Run ID: 12345678)

============================================================
📊 PyPI Publish Workflow Status
============================================================
Workflow:   Publish to PyPI
Title:      Release v0.3.1
Status:     ✅ completed
Result:     ✅ SUCCESS
URL:        https://github.com/kamera-linux/vogel-video-analyzer/actions/runs/12345678
============================================================

💡 Useful commands:
   Watch live:  gh run watch 12345678
   View logs:   gh run view 12345678 --log
   Open web:    gh run view 12345678 --web
```

### Notes

- Script automatically pushes unpushed tags if confirmed
- Validates semantic versioning format (`v0.3.1` or `0.3.1`)
- Can delete and recreate existing releases
- Monitors GitHub Actions workflow for PyPI publishing
- Uses auto-generated notes if release notes file not found
