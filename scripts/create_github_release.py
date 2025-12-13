#!/usr/bin/env python3
"""
Create GitHub Release from latest Git tag.

This script automatically:
1. Detects the latest Git tag
2. Finds the corresponding release notes file
3. Creates a GitHub release using gh CLI

Usage:
    python scripts/create_github_release.py              # Use latest tag
    python scripts/create_github_release.py v0.1.15      # Specific tag
    python scripts/create_github_release.py --draft      # Create as draft
    python scripts/create_github_release.py --prerelease # Mark as pre-release
"""

import argparse
import subprocess
import sys
from pathlib import Path
import re
import time
import json


def run_command(cmd, check=True, capture_output=True):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def get_latest_tag():
    """Get the latest Git tag."""
    print("🔍 Searching for latest Git tag...")
    
    # Get all tags sorted by version
    tags = run_command("git tag --sort=-v:refname")
    
    if not tags:
        print("❌ No Git tags found!")
        print("Create a tag first: git tag -a v0.1.15 -m 'Release v0.1.15'")
        sys.exit(1)
    
    latest_tag = tags.split('\n')[0]
    print(f"✅ Found latest tag: {latest_tag}")
    return latest_tag


def validate_tag_format(tag):
    """Validate tag follows semantic versioning (v0.1.15 or 0.1.15)."""
    pattern = r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$'
    if not re.match(pattern, tag):
        print(f"⚠️  Warning: Tag '{tag}' doesn't follow semantic versioning")
        print("Expected format: v0.1.15 or v0.1.15-beta.1")
        response = input("Continue anyway? [y/N]: ")
        if response.lower() != 'y':
            sys.exit(1)
    return tag


def find_release_notes(tag, release_dir):
    """Find release notes file for the given tag."""
    print(f"📝 Looking for release notes file...")
    
    # Try different filename patterns
    patterns = [
        f"RELEASE_{tag}.md",
        f"RELEASE_{tag.lstrip('v')}.md",
        f"release-{tag}.md",
        f"release-{tag.lstrip('v')}.md",
        f"RELEASE-{tag}.md",
        f"RELEASE-{tag.lstrip('v')}.md",
    ]
    
    for pattern in patterns:
        release_file = release_dir / pattern
        if release_file.exists():
            print(f"✅ Found release notes: {release_file}")
            return release_file
    
    # No release notes found
    print(f"⚠️  No release notes file found in {release_dir}/")
    print(f"Expected one of: {', '.join(patterns)}")
    
    response = input("Create release with auto-generated notes? [y/N]: ")
    if response.lower() != 'y':
        sys.exit(1)
    
    return None


def extract_title_from_notes(notes_file):
    """Extract release title from first H1 heading in notes file."""
    if not notes_file or not notes_file.exists():
        return None
    
    try:
        content = notes_file.read_text(encoding='utf-8')
        # Find first H1 heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # Remove "Release" prefix if present
            title = re.sub(r'^Release\s+', '', title, flags=re.IGNORECASE)
            return title
    except Exception as e:
        print(f"⚠️  Could not extract title from notes: {e}")
    
    return None


def check_tag_exists_on_remote(tag):
    """Check if tag exists on remote."""
    result = run_command(f"git ls-remote --tags origin {tag}", check=False)
    return bool(result)


def check_release_exists(tag):
    """Check if GitHub release already exists."""
    result = run_command(f"gh release view {tag}", check=False)
    return result != ""


def create_github_release(tag, notes_file, title=None, draft=False, prerelease=False):
    """Create GitHub release using gh CLI."""
    print(f"\n🚀 Creating GitHub release for {tag}...")
    
    # Build command
    cmd_parts = ["gh", "release", "create", tag]
    
    # Title
    if title:
        cmd_parts.extend(["--title", f'"{title}"'])
    else:
        # Generate default title
        version = tag.lstrip('v')
        default_title = f"Release {tag}"
        cmd_parts.extend(["--title", f'"{default_title}"'])
    
    # Notes
    if notes_file:
        cmd_parts.extend(["--notes-file", str(notes_file)])
    else:
        cmd_parts.append("--generate-notes")
    
    # Options
    if draft:
        cmd_parts.append("--draft")
        print("📄 Creating as DRAFT (not published)")
    
    if prerelease:
        cmd_parts.append("--prerelease")
        print("🧪 Marking as PRE-RELEASE")
    
    # Verify tag exists
    cmd_parts.append("--verify-tag")
    
    # Execute
    cmd = " ".join(cmd_parts)
    print(f"\n💻 Command: {cmd}\n")
    
    run_command(cmd, capture_output=False)
    
    print(f"\n✅ Release {tag} created successfully!")
    return True


def wait_for_workflow_trigger(tag, workflow_name="publish-pypi.yml", timeout=60):
    """Wait for workflow to be triggered after release creation."""
    print(f"\n⏳ Waiting for '{workflow_name}' workflow to start for {tag}...")
    
    # Extract version from tag for matching (e.g., v0.1.15 -> 0.1.15)
    version = tag.lstrip('v')
    
    start_time = time.time()
    dots = 0
    while time.time() - start_time < timeout:
        # Get recent workflow runs with title
        result = subprocess.run(
            f'gh run list --workflow="{workflow_name}" --limit 5 --json status,databaseId,createdAt,displayTitle',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                runs = json.loads(result.stdout)
                # Look for run matching our tag/version
                for run in runs:
                    title = run.get('displayTitle', '')
                    # Check if this run is for our release
                    if tag in title or version in title:
                        print(f"\n✅ Workflow triggered (Run ID: {run.get('databaseId')})")
                        return run.get('databaseId')
            except json.JSONDecodeError:
                pass
        
        # Show progress
        dots = (dots + 1) % 4
        print(f"\r⏳ Waiting{'.' * dots}{' ' * (3 - dots)}", end='', flush=True)
        time.sleep(3)
    
    print(f"\n⚠️  Workflow for {tag} did not start within {timeout}s timeout")
    return None


def watch_workflow_completion(run_id, workflow_name="publish-pypi.yml", timeout=600):
    """Watch workflow until completion with live status updates."""
    print(f"\n🔄 Watching workflow completion (timeout: {timeout}s)...")
    
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < timeout:
        result = subprocess.run(
            f'gh run view {run_id} --json status,conclusion',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"\n⚠️  Failed to get workflow status")
            return None, None
        
        try:
            run_info = json.loads(result.stdout)
            status = run_info.get('status', 'unknown')
            conclusion = run_info.get('conclusion')
            
            # Update status if changed
            if status != last_status:
                timestamp = time.strftime('%H:%M:%S')
                if status == 'queued':
                    print(f"[{timestamp}] ⏳ Queued...")
                elif status == 'in_progress':
                    print(f"[{timestamp}] 🔄 Running...")
                elif status == 'completed':
                    if conclusion == 'success':
                        print(f"[{timestamp}] ✅ Completed successfully!")
                        return 'completed', 'success'
                    elif conclusion == 'failure':
                        print(f"[{timestamp}] ❌ Failed!")
                        return 'completed', 'failure'
                    elif conclusion == 'cancelled':
                        print(f"[{timestamp}] 🚫 Cancelled")
                        return 'completed', 'cancelled'
                    else:
                        print(f"[{timestamp}] ✅ Completed: {conclusion}")
                        return 'completed', conclusion
                
                last_status = status
            
            # Check if completed
            if status == 'completed':
                break
            
            time.sleep(5)
            
        except json.JSONDecodeError:
            print(f"\n⚠️  Failed to parse workflow data")
            return None, None
    
    if time.time() - start_time >= timeout:
        print(f"\n⏱️  Workflow watch timeout after {timeout}s")
        return 'timeout', None
    
    return status, conclusion


def check_workflow_status(run_id=None, workflow_name="publish-pypi.yml"):
    """Check and display workflow status."""
    if not run_id:
        # Get latest workflow run
        result = subprocess.run(
            f'gh run list --workflow="{workflow_name}" --limit 1 --json status,conclusion,databaseId,workflowName,displayTitle,createdAt,url',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            print(f"⚠️  No workflow runs found for '{workflow_name}'")
            return None, None
        
        try:
            runs = json.loads(result.stdout)
            if not runs:
                print("⚠️  No workflow runs found")
                return None, None
            
            run = runs[0]
            run_id = run.get('databaseId')
        except json.JSONDecodeError:
            print("⚠️  Failed to parse workflow data")
            return None, None
    
    # Get detailed run information
    result = subprocess.run(
        f'gh run view {run_id} --json status,conclusion,workflowName,displayTitle,url,createdAt',
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0 or not result.stdout.strip():
        print("⚠️  Failed to get workflow details")
        return None, None
    
    try:
        run_info = json.loads(result.stdout)
        
        print("\n" + "=" * 60)
        print("📊 PyPI Publish Workflow Status")
        print("=" * 60)
        print(f"Workflow:   {run_info.get('workflowName', 'N/A')}")
        print(f"Title:      {run_info.get('displayTitle', 'N/A')}")
        
        status = run_info.get('status', 'N/A')
        status_emoji = {
            'queued': '⏳',
            'in_progress': '🔄',
            'completed': '✅'
        }.get(status, '❓')
        print(f"Status:     {status_emoji} {status}")
        
        conclusion = run_info.get('conclusion')
        if conclusion:
            conclusion_emoji = {
                'success': '✅',
                'failure': '❌',
                'cancelled': '🚫',
                'skipped': '⏭️'
            }.get(conclusion, '❓')
            print(f"Result:     {conclusion_emoji} {conclusion.upper()}")
        
        print(f"URL:        {run_info.get('url', 'N/A')}")
        print("=" * 60)
        
        # Show commands for further actions
        print(f"\n💡 Useful commands:")
        print(f"   Watch live:  gh run watch {run_id}")
        print(f"   View logs:   gh run view {run_id} --log")
        print(f"   Open web:    gh run view {run_id} --web")
        
        return status, conclusion
        
    except json.JSONDecodeError:
        print("⚠️  Failed to parse workflow information")
        return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Create GitHub release from Git tag",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use latest tag
  python scripts/create_github_release.py
  
  # Specific tag
  python scripts/create_github_release.py v0.1.15
  
  # Create and watch workflow completion
  python scripts/create_github_release.py v0.1.15 --watch
  
  # Create as draft
  python scripts/create_github_release.py --draft
  
  # Mark as pre-release
  python scripts/create_github_release.py v0.2.0-beta.1 --prerelease
  
  # Custom title and watch with longer timeout
  python scripts/create_github_release.py --title "My Custom Title" --watch --watch-timeout 900
        """
    )
    
    parser.add_argument(
        'tag',
        nargs='?',
        help='Git tag to release (default: latest tag)'
    )
    parser.add_argument(
        '--draft',
        action='store_true',
        help='Create release as draft'
    )
    parser.add_argument(
        '--prerelease',
        action='store_true',
        help='Mark release as pre-release'
    )
    parser.add_argument(
        '--title',
        help='Custom release title (default: extracted from notes or auto-generated)'
    )
    parser.add_argument(
        '--notes-dir',
        default='.github',
        help='Directory containing release notes (default: .github)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip all confirmation prompts'
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch workflow completion until finished (default: show status and exit)'
    )
    parser.add_argument(
        '--watch-timeout',
        type=int,
        default=600,
        help='Workflow watch timeout in seconds (default: 600)'
    )
    
    args = parser.parse_args()
    
    # Check gh CLI is installed
    if not run_command("which gh", check=False):
        print("❌ GitHub CLI (gh) not found!")
        print("Install: https://cli.github.com/")
        sys.exit(1)
    
    # Check authentication
    auth_status = run_command("gh auth status", check=False)
    if not auth_status or "Logged in" not in auth_status:
        print("❌ Not authenticated with GitHub!")
        print("Run: gh auth login")
        sys.exit(1)
    
    print("=" * 60)
    print("🎯 GitHub Release Creator")
    print("=" * 60)
    print()
    
    # Get or validate tag
    if args.tag:
        tag = args.tag
        validate_tag_format(tag)
    else:
        tag = get_latest_tag()
    
    # Check if tag exists locally
    local_tags = run_command("git tag")
    if tag not in local_tags.split('\n'):
        print(f"❌ Tag '{tag}' not found locally!")
        print("Available tags:")
        print(local_tags)
        sys.exit(1)
    
    # Check if tag is pushed
    if not check_tag_exists_on_remote(tag):
        print(f"⚠️  Tag '{tag}' not found on remote!")
        if not args.force:
            response = input(f"Push tag '{tag}' to remote? [y/N]: ")
            if response.lower() == 'y':
                run_command(f"git push origin {tag}")
                print(f"✅ Tag pushed to remote")
            else:
                print("❌ Cannot create release without pushing tag first")
                sys.exit(1)
        else:
            run_command(f"git push origin {tag}")
    else:
        print(f"✅ Tag exists on remote")
    
    # Check if release already exists
    if check_release_exists(tag):
        print(f"⚠️  Release '{tag}' already exists on GitHub!")
        print(f"View: gh release view {tag}")
        if not args.force:
            response = input("Delete and recreate? [y/N]: ")
            if response.lower() == 'y':
                run_command(f"gh release delete {tag} --yes")
                print("✅ Existing release deleted")
            else:
                sys.exit(1)
        else:
            run_command(f"gh release delete {tag} --yes")
    
    # Find release notes
    release_dir = Path(args.notes_dir)
    notes_file = find_release_notes(tag, release_dir)
    
    # Determine title
    title = args.title
    if not title and notes_file:
        title = extract_title_from_notes(notes_file)
        if title:
            print(f"📋 Extracted title: {title}")
    
    # Confirm
    if not args.force:
        print("\n" + "=" * 60)
        print("📊 Release Summary:")
        print("=" * 60)
        print(f"Tag:         {tag}")
        print(f"Title:       {title or f'Release {tag}'}")
        print(f"Notes:       {notes_file or 'Auto-generated'}")
        print(f"Draft:       {args.draft}")
        print(f"Pre-release: {args.prerelease}")
        print("=" * 60)
        print()
        
        response = input("Create this release? [y/N]: ")
        if response.lower() != 'y':
            print("❌ Release creation cancelled")
            sys.exit(0)
    
    # Create release
    success = create_github_release(
        tag=tag,
        notes_file=notes_file,
        title=title,
        draft=args.draft,
        prerelease=args.prerelease
    )
    
    if success:
        print(f"\n🌐 View release: gh release view {tag} --web")
        print(f"📝 Edit release: gh release edit {tag}")
        print(f"🗑️  Delete release: gh release delete {tag}")
        
        # Check for PyPI publish workflow (only for published releases, not drafts)
        if not args.draft:
            print("\n" + "=" * 60)
            print("Checking for PyPI publish workflow...")
            print("=" * 60)
            
            # Wait for workflow to be triggered
            run_id = wait_for_workflow_trigger(tag, "publish-pypi.yml", timeout=60)
            
            if run_id:
                print(f"✅ Workflow triggered for {tag}")
                
                if args.watch:
                    # Watch workflow until completion
                    status, conclusion = watch_workflow_completion(
                        run_id, 
                        "publish-pypi.yml", 
                        timeout=args.watch_timeout
                    )
                    
                    # Show final detailed status
                    print("\n" + "=" * 60)
                    print("📊 Final Workflow Status")
                    print("=" * 60)
                    check_workflow_status(run_id)
                    
                    if conclusion == 'success':
                        print("\n🎉 PyPI publish successful!")
                        print("📦 Package should be available at: https://pypi.org/project/vogel-video-analyzer/")
                    elif conclusion == 'failure':
                        print("\n❌ PyPI publish failed! Check workflow logs:")
                        print(f"   gh run view {run_id} --log-failed")
                else:
                    # Just show current status
                    time.sleep(3)  # Give workflow time to update status
                    check_workflow_status(run_id)
                    print("\n💡 To watch workflow completion, use: --watch")
                    print(f"   python scripts/create_github_release.py {tag} --watch")
            else:
                # Check if there's a recent workflow run anyway
                print(f"⚠️  No workflow found for {tag}, showing latest run:")
                check_workflow_status(workflow_name="publish-pypi.yml")


if __name__ == "__main__":
    main()
