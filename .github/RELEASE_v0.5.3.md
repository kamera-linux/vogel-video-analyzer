# Release v0.5.3 - Issue Board & GitHub Integration 📋

**Release Date:** January 31, 2026

## 🎯 Overview

This feature release introduces a comprehensive issue tracking and project management system directly integrated into vogel-video-analyzer, with optional GitHub Issues synchronization for team collaboration.

## 🎉 What's New

### 📋 Issue Board System

A complete local issue management system for project tracking and bug reporting:

**Core Features:**
- ✅ Create, read, update, and delete issues
- 🏷️ Status tracking: `todo`, `in_progress`, `done`, `blocked`
- 🎯 Priority levels: `low`, `medium`, `high`, `critical`
- 🏴 Flexible labeling system
- 👤 Assignee support
- 💾 JSON-based local storage (`~/.vogel_issues.json`)
- 📊 Statistics and filtering

**CLI Commands:**
```bash
vogel-issues create "Title" "Description"      # Create issue
vogel-issues list                              # List all issues
vogel-issues list --status todo                # Filter by status
vogel-issues list --priority high              # Filter by priority
vogel-issues show 1                            # Show issue details
vogel-issues update 1 --status done            # Update issue
vogel-issues delete 1                          # Delete issue
vogel-issues stats                             # Show statistics
```

**Python API:**
```python
from vogel_video_analyzer.issue_board import IssueBoard

board = IssueBoard()
issue = board.create_issue(
    title="Video Export Bug",
    description="Export fails on large files",
    priority="high",
    labels=["bug", "video-export"]
)
```

### 🔄 GitHub Issues Synchronization

Optional bidirectional synchronization with GitHub Issues for team collaboration:

**Installation:**
```bash
pip install vogel-video-analyzer[github]
```

**Token Setup (3 Methods):**

1. **Environment Variable (Recommended):**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

2. **Config File:**
```bash
vogel-issues setup  # Interactive wizard
# Saves to ~/.vogel_config.json
```

3. **CLI Parameter:**
```bash
vogel-issues sync --github-token "ghp_xxxxxxxxxxxx"
```

**Synchronization Commands:**
```bash
vogel-issues sync                    # Bidirectional sync
vogel-issues sync --direction push   # Local → GitHub
vogel-issues sync --direction pull   # GitHub → Local
vogel-issues sync --repo owner/repo  # Specific repository
```

**How It Works:**
- 🏷️ Automatic label conversion (status/priority → GitHub labels)
- 🔄 Issue state synchronization (open/closed)
- 🔍 Automatic repository detection from Git config
- 💾 Non-destructive (never deletes issues)
- 📝 Maintains local issue IDs in GitHub issue body

**Label Mapping:**
- Status: `status: todo`, `status: in progress`, `status: done`, `status: blocked`
- Priority: `priority: low`, `priority: medium`, `priority: high`, `priority: critical`

### 🎨 Rich CLI Output

Beautiful terminal interface with colors and emojis:
- 📋 TODO (Yellow)
- ⚙️ IN PROGRESS (Blue)
- ✅ DONE (Green)
- 🚫 BLOCKED (Red)
- 🔵/🟡/🟠/🔴 Priority indicators

### 📚 Comprehensive Documentation

New documentation files:
- `docs/ISSUE_BOARD.md` - Complete feature documentation
- `docs/GITHUB_SYNC_QUICKSTART.md` - Quick setup guide with examples
- Example workflows and troubleshooting

## 📋 Changes

### ✨ Added
- **Issue Board System**: Complete local issue management (`issue_board.py`)
- **Issue CLI**: Full-featured command-line interface (`issue_cli.py`)
- **GitHub Sync**: Bidirectional GitHub Issues integration (`github_sync.py`)
- **New CLI Command**: `vogel-issues` entry point
- **Test Suite**: Comprehensive tests for issue board and GitHub sync
- **Documentation**: Two new comprehensive docs in `/docs`
- **Optional Dependency**: PyGithub for GitHub integration

### 🔧 Changed
- **pyproject.toml**: Added `vogel-issues` script entry point
- **pyproject.toml**: Added `github` optional dependency group
- **Version**: Bumped to 0.5.3

### 📦 New Files
- `src/vogel_video_analyzer/issue_board.py`
- `src/vogel_video_analyzer/issue_cli.py`
- `src/vogel_video_analyzer/github_sync.py`
- `tests/test_issue_board.py`
- `tests/test_github_sync.py`
- `docs/ISSUE_BOARD.md`
- `docs/GITHUB_SYNC_QUICKSTART.md`

## 🚀 Installation

### Basic Installation
```bash
pip install vogel-video-analyzer==0.5.3
```

### With GitHub Support
```bash
pip install vogel-video-analyzer[github]==0.5.3
```

### From Source
```bash
git clone https://github.com/kamera-linux/vogel-video-analyzer.git
cd vogel-video-analyzer
pip install -e .[github]
```

## 📖 Usage Examples

### Local Issue Management

```bash
# Create issues
vogel-issues create "Performance Issue" \
  "Video processing is slow on large files" \
  --priority high \
  --labels performance optimization

# List and filter
vogel-issues list --status todo --priority high
vogel-issues list --label bug

# Update
vogel-issues update 1 --status in_progress --assignee "Developer"

# Statistics
vogel-issues stats
```

### GitHub Integration

```bash
# Setup token
export GITHUB_TOKEN="ghp_your_token_here"

# Sync with GitHub
vogel-issues sync

# Push local issues to GitHub
vogel-issues sync --direction push

# Import GitHub issues locally
vogel-issues sync --direction pull
```

### Python API

```python
from vogel_video_analyzer.issue_board import IssueBoard

# Local issue management
board = IssueBoard()
issue = board.create_issue(
    title="Add CSV Export",
    description="Export results as CSV file",
    priority="medium",
    labels=["enhancement", "feature-request"]
)

# List issues
todo_issues = board.list_issues(status="todo")

# Update issue
board.update_issue(issue.id, status="in_progress")

# GitHub sync (optional)
from vogel_video_analyzer.github_sync import GitHubSync

sync = GitHubSync(token="ghp_...", repo="owner/repo")
sync.push_issue(issue)
```

## 🔒 Security

**Token Safety:**
- Config file automatically chmod 600
- Token never logged or printed
- Multiple secure storage options
- `.gitignore` recommendations included

**Important:**
- ⛔ Never commit tokens to Git
- ⛔ Never share tokens publicly
- ✅ Use environment variables or secure config file

## 📚 Documentation

- **Full Documentation:** [README.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/README.md)
- **Issue Board Guide:** [docs/ISSUE_BOARD.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/docs/ISSUE_BOARD.md)
- **GitHub Sync Guide:** [docs/GITHUB_SYNC_QUICKSTART.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/docs/GITHUB_SYNC_QUICKSTART.md)

## 🔗 Links

- **PyPI:** https://pypi.org/project/vogel-video-analyzer/0.5.3/
- **Changelog:** [CHANGELOG.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/main/CHANGELOG.md)
- **Issues:** https://github.com/kamera-linux/vogel-video-analyzer/issues
- **Repository:** https://github.com/kamera-linux/vogel-video-analyzer

## 📝 Upgrade Instructions

```bash
# Standard upgrade
pip install --upgrade vogel-video-analyzer

# With GitHub support
pip install --upgrade vogel-video-analyzer[github]
```

## 🎯 Use Cases

- **Bug Tracking**: Track bugs locally during development
- **Feature Planning**: Plan and prioritize new features
- **Team Collaboration**: Sync with GitHub for team access
- **Offline Work**: Work on issues without internet connection
- **Personal Projects**: Simple issue tracking without GitHub account

## ⚠️ Notes

- Issue Board works completely offline by default
- GitHub sync is optional and requires PyGithub
- Local storage in `~/.vogel_issues.json` (portable JSON format)
- Non-destructive sync (never deletes issues)
- Auto-detects repository from Git config

## 🙏 Acknowledgments

Thanks to the community for requesting better project management tools!

---

**Full Changelog:** https://github.com/kamera-linux/vogel-video-analyzer/blob/main/CHANGELOG.md
