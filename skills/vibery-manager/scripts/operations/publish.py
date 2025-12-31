#!/usr/bin/env python3
"""Publish operations: deploy website, push to GitHub, publish CLI to npm."""

import subprocess
import shutil
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
CLI_DIR = ROOT / "cli"
WEBSITE_DIR = ROOT / "website"
TEMPLATES_DIR = ROOT / "templates"
TEMPLATES_REPO_DIR = ROOT / "templates-repo"

# Colors
C = {
    "reset": "\033[0m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "red": "\033[31m",
    "dim": "\033[2m",
    "bold": "\033[1m",
}


def log(msg: str, color: str = "reset"):
    print(f"{C.get(color, '')}{msg}{C['reset']}")


def hint(msg: str):
    print(f"{C['dim']}  → {msg}{C['reset']}")


def run_cmd(cmd: list, cwd: Path = None, check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return True
    except subprocess.CalledProcessError as e:
        log(f"  Error: {e.stderr}", "red")
        return False


def publish_command(dry_run: bool = False):
    """Publish website, GitHub templates, and optionally CLI package."""
    log("\nPublishing Vibery...", "blue")

    success = {"github": False, "website": False}

    # 1. Sync and push to GitHub templates repo
    log("\n[1/2] Syncing templates to GitHub...", "bold")
    success["github"] = push_templates_to_github(dry_run)

    # 2. Build and deploy website
    log("\n[2/2] Deploying website...", "bold")
    success["website"] = deploy_website(dry_run)

    # Summary
    log("\n" + "=" * 50, "dim")
    if all(success.values()):
        log("✓ Publish complete!", "green")
    else:
        failed = [k for k, v in success.items() if not v]
        log(f"⚠ Partial publish: {', '.join(failed)} failed", "yellow")

    log("\nStatus:", "bold")
    log(f"  GitHub:  {'✓' if success['github'] else '✗'}", "green" if success["github"] else "red")
    log(f"  Website: {'✓' if success['website'] else '✗'}", "green" if success["website"] else "red")

    if success["github"]:
        log("\nTemplates repo:", "bold")
        hint("https://github.com/vibery-studio/templates")

    if success["website"]:
        log("\nWebsite live at:", "bold")
        hint("https://kits.vibery.app")

    log("\nCLI will auto-fetch from GitHub (no npm publish needed)", "dim")


def push_templates_to_github(dry_run: bool = False) -> bool:
    """Sync templates to templates-repo and push to GitHub."""
    if not TEMPLATES_REPO_DIR.exists():
        log("  templates-repo/ not found", "red")
        hint("Clone: git clone https://github.com/vibery-studio/templates templates-repo")
        return False

    if not (TEMPLATES_REPO_DIR / ".git").exists():
        log("  templates-repo/ is not a git repository", "red")
        return False

    # Sync each template type
    template_types = ["agents", "commands", "mcps", "hooks", "settings", "skills"]
    synced = 0

    log("  Syncing templates...", "dim")
    for ttype in template_types:
        src = TEMPLATES_DIR / ttype
        dest = TEMPLATES_REPO_DIR / ttype
        if src.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            count = len(list(src.rglob("*"))) if src.is_dir() else 1
            synced += count

    log(f"  Synced {synced} files", "dim")

    if dry_run:
        log("  [DRY] Would commit and push to GitHub", "dim")
        return True

    # Git operations
    try:
        # Check for changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=TEMPLATES_REPO_DIR,
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            log("  No changes to push", "dim")
            return True

        # Add all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=TEMPLATES_REPO_DIR,
            check=True
        )

        # Commit
        subprocess.run(
            ["git", "commit", "-m", "chore: sync templates"],
            cwd=TEMPLATES_REPO_DIR,
            capture_output=True,
            check=True
        )

        # Push
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=TEMPLATES_REPO_DIR,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            log(f"  Push failed: {result.stderr[:200]}", "red")
            return False

        log("  ✓ Pushed to GitHub", "green")
        return True

    except subprocess.CalledProcessError as e:
        log(f"  Git error: {e}", "red")
        return False


def deploy_website(dry_run: bool = False) -> bool:
    """Build and deploy website to Cloudflare Pages."""
    if not WEBSITE_DIR.exists():
        log("  Website directory not found", "red")
        return False

    # Check for package.json
    if not (WEBSITE_DIR / "package.json").exists():
        log("  No package.json in website/", "red")
        return False

    if dry_run:
        log("  [DRY] Would run: npm run build", "dim")
        log("  [DRY] Would run: wrangler pages deploy", "dim")
        return True

    # Install dependencies if needed
    if not (WEBSITE_DIR / "node_modules").exists():
        log("  Installing dependencies...", "dim")
        if not run_cmd(["npm", "install"], cwd=WEBSITE_DIR, check=False):
            log("  npm install failed", "red")
            return False

    # Build
    log("  Building website...", "dim")
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=WEBSITE_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        log(f"  Build failed: {result.stderr[:200]}", "red")
        return False

    log("  Build successful", "green")

    # Deploy to Cloudflare Pages
    log("  Deploying to Cloudflare Pages...", "dim")
    result = subprocess.run(
        ["npx", "wrangler", "pages", "deploy", "dist", "--project-name=vibery"],
        cwd=WEBSITE_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Check if wrangler is configured
        if "not logged in" in result.stderr.lower() or "authentication" in result.stderr.lower():
            log("  Not logged in to Cloudflare", "yellow")
            hint("Run: npx wrangler login")
            return False
        log(f"  Deploy failed: {result.stderr[:200]}", "red")
        return False

    log("  ✓ Website deployed", "green")
    return True


def publish_cli(dry_run: bool = False) -> bool:
    """Publish CLI package to npm."""
    if not CLI_DIR.exists():
        log("  CLI directory not found", "red")
        return False

    if not (CLI_DIR / "package.json").exists():
        log("  No package.json in cli/", "red")
        return False

    if dry_run:
        log("  [DRY] Would run: npm publish", "dim")
        return True

    # Check npm auth
    result = subprocess.run(
        ["npm", "whoami"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        log("  Not logged in to npm", "yellow")
        hint("Run: npm login")
        return False

    log(f"  Logged in as: {result.stdout.strip()}", "dim")

    # Publish
    log("  Publishing to npm...", "dim")
    result = subprocess.run(
        ["npm", "publish", "--access", "public"],
        cwd=CLI_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        if "cannot publish over the previously published" in result.stderr.lower():
            log("  Version already published (bump version first)", "yellow")
            hint("Update version in cli/package.json")
            return False
        log(f"  Publish failed: {result.stderr[:200]}", "red")
        return False

    log("  ✓ CLI published to npm", "green")
    return True
