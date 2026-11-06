#!/bin/bash
# Release Checklist
# ==============================
# Version is read from src/vogel_video_analyzer/__init__.py.
# Usage: ./release_checklist.sh [VERSION]   (default: current __version__)

set -u
cd "$(dirname "$0")"

VERSION="${1:-$(sed -n 's/^__version__ = "\(.*\)"/\1/p' src/vogel_video_analyzer/__init__.py)}"
if [ -z "$VERSION" ]; then
    echo "❌ Could not determine version"
    exit 1
fi
TAG="v${VERSION}"
NOTES=".github/RELEASE_${TAG}.md"
PREV_NOTES="$(ls .github/RELEASE_v*.md 2>/dev/null | sort -V | grep -v "RELEASE_${TAG}.md" | tail -1)"

echo "📋 Release Preparation Checklist für ${TAG}"
echo "=============================================="
echo ""

# 1. Check git status
echo "✅ Step 1: Git Status"
echo "---"
git status --short
echo ""

# 2. Check version
echo "✅ Step 2: Version Check"
echo "---"
echo "__init__.py: ${VERSION}"
python3 -c "from vogel_video_analyzer import __version__; print(f'Installed: {__version__}')" 2>/dev/null || echo "Paket nicht installiert"
echo ""

# 3. Check CHANGELOG
echo "✅ Step 3: CHANGELOG.md Check"
echo "---"
if grep -q "\[${VERSION}\]" CHANGELOG.md; then
    grep -A5 "\[${VERSION}\]" CHANGELOG.md | head -6
else
    echo "✗ No CHANGELOG entry for ${VERSION}"
fi
echo ""

# 4. Run tests
echo "✅ Step 4: Tests"
echo "---"
python3 -m pytest -q --no-cov 2>&1 | tail -3 || echo "⚠ pytest not available"
echo ""

# 5. Check if release notes file exists
echo "✅ Step 5: Release Notes File"
echo "---"
if [ -f "${NOTES}" ]; then
    echo "✓ ${NOTES} exists"
else
    echo "✗ ${NOTES} NOT found - needs to be created!"
fi
echo ""

# 6. Check GitHub CLI
echo "✅ Step 6: GitHub CLI Check"
echo "---"
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI (gh) installed"
    gh --version | head -1
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
if [ -n "${PREV_NOTES}" ]; then
    echo "   cp ${PREV_NOTES} ${NOTES}"
fi
echo "   # Then edit: ${NOTES}"
echo ""
echo "3. Create and push Git tag:"
echo "   git tag -a ${TAG} -m 'Release ${TAG}'"
echo "   git push origin ${TAG}"
echo ""
echo "4. Create GitHub release:"
echo "   python scripts/create_github_release.py ${TAG}"
echo ""
echo "Or with auto-watch for PyPI workflow:"
echo "   python scripts/create_github_release.py ${TAG} --watch"
echo ""
