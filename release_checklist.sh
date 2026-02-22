#!/bin/bash
# Release Checklist für v0.5.6
# ==============================

echo "📋 Release Preparation Checklist für v0.5.6"
echo "=============================================="
echo ""

# 1. Check git status
echo "✅ Step 1: Git Status"
echo "---"
git status
echo ""

# 2. Check version
echo "✅ Step 2: Version Check"
echo "---"
python3 -c "from vogel_video_analyzer import __version__; print(f'Version: {__version__}')" 2>/dev/null || echo "Paket nicht installiert"
echo ""

# 3. Check CHANGELOG
echo "✅ Step 3: CHANGELOG.md Check"
echo "---"
head -30 CHANGELOG.md | grep -A5 "0.5.6"
echo ""

# 4. Check pyproject.toml
echo "✅ Step 4: pyproject.toml Check"
echo "---"
grep "YOLOv26" pyproject.toml | head -3
echo ""

# 5. Check if release notes file exists
echo "✅ Step 5: Release Notes File"
echo "---"
if [ -f ".github/RELEASE_v0.5.6.md" ]; then
    echo "✓ .github/RELEASE_v0.5.6.md exists"
else
    echo "✗ .github/RELEASE_v0.5.6.md NOT found - needs to be created!"
fi
echo ""

# 6. Check GitHub CLI
echo "✅ Step 6: GitHub CLI Check"
echo "---"
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI (gh) installed"
    gh --version
else
    echo "✗ GitHub CLI not found - install from: https://cli.github.com/"
fi
echo ""

# 7. Check authentication
echo "✅ Step 7: GitHub Authentication"
echo "---"
gh auth status 2>&1 | head -3 || echo "⚠ gh auth login needed"
echo ""

echo "=============================================="
echo "📋 Next Steps:"
echo "=============================================="
echo ""
echo "1. Verify all changes are committed:"
echo "   git log --oneline -5"
echo ""
echo "2. Create release notes file:"
echo "   cp .github/RELEASE_v0.5.5.md .github/RELEASE_v0.5.6.md"
echo "   # Then edit: RELEASE_v0.5.6.md"
echo ""
echo "3. Create and push Git tag:"
echo "   git tag -a v0.5.6 -m 'Release v0.5.6: YOLOv26 Upgrade'"
echo "   git push origin v0.5.6"
echo ""
echo "4. Create GitHub release:"
echo "   python scripts/create_github_release.py v0.5.6"
echo ""
echo "Or with auto-watch for PyPI workflow:"
echo "   python scripts/create_github_release.py v0.5.6 --watch"
echo ""
