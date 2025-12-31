#!/usr/bin/env python3
"""Template operations: pull, create, list."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
TEMPLATES_DIR = ROOT / "templates"
SKILLS_DIR = ROOT / ".claude" / "skills"

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
    """Print a hint for next steps."""
    print(f"{C['dim']}  → {msg}{C['reset']}")


def template_command(args: list, type_filter: str = None, dry_run: bool = False):
    """Handle template commands."""
    if not args:
        log("Usage: template <pull|create|list> [args]", "yellow")
        return

    action = args[0]

    if action == "pull":
        if len(args) < 2:
            log("Usage: template pull <git-url|path>", "yellow")
            return
        pull_template(args[1], dry_run)

    elif action == "create":
        if len(args) < 3:
            log("Usage: template create <type> <name>", "yellow")
            log("Types: agent, command, skill, hook, mcp, setting", "dim")
            return
        create_template(args[1], args[2], dry_run)

    elif action == "list":
        list_templates(type_filter)

    else:
        log(f"Unknown action: {action}", "red")


def pull_template(source: str, dry_run: bool = False):
    """Pull template from git repo or local path."""
    log(f"\nPulling from: {source}", "blue")

    # Determine source type
    is_git = source.startswith("http") or source.startswith("git@")
    is_local = Path(source).exists()

    if not is_git and not is_local:
        log(f"Source not found: {source}", "red")
        return

    pulled = []

    if is_git:
        # Clone to temp dir
        with tempfile.TemporaryDirectory() as tmpdir:
            log("  Cloning repository...", "dim")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", source, tmpdir],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                log(f"Git clone failed: {result.stderr}", "red")
                return

            pulled = scan_and_copy(Path(tmpdir), dry_run)
    else:
        pulled = scan_and_copy(Path(source), dry_run)

    # Summary
    if pulled:
        log(f"\n✓ Pulled {len(pulled)} items", "green")
        for item in pulled[:5]:
            log(f"  {item['type']}: {item['name']}", "dim")
        if len(pulled) > 5:
            log(f"  ... and {len(pulled) - 5} more", "dim")

        log("\nNext steps:", "bold")
        hint("/template list                    # View all templates")
        hint("/kit add <kit> <template>         # Add to a kit")
        hint("/sync                             # Sync when ready")
    else:
        log("No templates found in source", "yellow")


def scan_and_copy(source_dir: Path, dry_run: bool = False) -> list:
    """Scan source directory and copy templates."""
    pulled = []

    # Check for .claude folder structure
    claude_dir = source_dir / ".claude"
    if claude_dir.exists():
        # Copy skills
        skills_src = claude_dir / "skills"
        if skills_src.exists():
            for skill in skills_src.iterdir():
                if skill.is_dir() and (skill / "SKILL.md").exists():
                    dest = SKILLS_DIR / skill.name
                    if not dry_run:
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(skill, dest)
                    pulled.append({"type": "skill", "name": skill.name})
                    log(f"  + skill: {skill.name}", "dim")

        # Copy agents
        for subdir in ["agents", "commands"]:
            src = claude_dir / subdir
            if src.exists():
                for f in src.glob("*.md"):
                    dest = TEMPLATES_DIR / subdir / f.name
                    if not dry_run:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, dest)
                    pulled.append({"type": subdir[:-1], "name": f.stem})
                    log(f"  + {subdir[:-1]}: {f.stem}", "dim")

    # Check for templates folder
    templates_src = source_dir / "templates"
    if templates_src.exists():
        for subdir in templates_src.iterdir():
            if subdir.is_dir():
                for f in subdir.rglob("*"):
                    if f.is_file() and not f.name.startswith("."):
                        rel = f.relative_to(templates_src)
                        dest = TEMPLATES_DIR / rel
                        if not dry_run:
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(f, dest)
                        pulled.append({"type": subdir.name, "name": f.stem})

    return pulled


def create_template(ttype: str, name: str, dry_run: bool = False):
    """Create a new template scaffold."""
    log(f"\nCreating {ttype}: {name}", "blue")

    templates = {
        "agent": {
            "dir": TEMPLATES_DIR / "agents",
            "ext": ".md",
            "content": f"""# {name.replace('-', ' ').title()} Agent

Expert in [domain].

## Capabilities

- Capability 1
- Capability 2

## When to Use

Activate when user needs help with [specific tasks].

## Workflow

1. Step 1
2. Step 2
"""
        },
        "command": {
            "dir": TEMPLATES_DIR / "commands",
            "ext": ".md",
            "content": f"""# {name}

[Description]

## Usage
```
/{name} [args]
```

## Process

1. Step 1
2. Step 2

## Output

[What it produces]
"""
        },
        "skill": {
            "dir": SKILLS_DIR / name,
            "ext": None,
            "content": None
        },
        "hook": {
            "dir": TEMPLATES_DIR / "hooks",
            "ext": ".json",
            "content": json.dumps({
                "hooks": {
                    "PostToolUse": [
                        {
                            "matcher": "Edit|Write",
                            "hooks": [
                                {"type": "command", "command": "echo 'Hook triggered'"}
                            ]
                        }
                    ]
                }
            }, indent=2)
        },
        "mcp": {
            "dir": TEMPLATES_DIR / "mcps",
            "ext": ".json",
            "content": json.dumps({
                "mcpServers": {
                    name: {
                        "command": "npx",
                        "args": ["-y", f"@example/{name}-mcp"],
                        "env": {}
                    }
                }
            }, indent=2)
        }
    }

    if ttype not in templates:
        log(f"Unknown type: {ttype}", "red")
        log(f"Valid types: {', '.join(templates.keys())}", "dim")
        return

    tmpl = templates[ttype]

    if ttype == "skill":
        # Create skill folder structure
        skill_dir = tmpl["dir"]
        if not dry_run:
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(f"""---
name: {name}
description: [Description]
version: 1.0.0
---

# {name.replace('-', ' ').title()}

## Usage

[How to use this skill]

## References

- `references/` - Reference docs
""")
            (skill_dir / "scripts").mkdir(exist_ok=True)
            (skill_dir / "references").mkdir(exist_ok=True)

        log(f"✓ Created skill scaffold: {skill_dir.relative_to(ROOT)}", "green")
    else:
        filepath = tmpl["dir"] / f"{name}{tmpl['ext']}"
        if not dry_run:
            tmpl["dir"].mkdir(parents=True, exist_ok=True)
            filepath.write_text(tmpl["content"])

        log(f"✓ Created: {filepath.relative_to(ROOT)}", "green")

    log("\nNext steps:", "bold")
    hint(f"Edit the template to add content")
    hint(f"/kit add <kit> {name}              # Add to a kit")
    hint(f"/sync                              # Sync when ready")


def list_templates(type_filter: str = None):
    """List all templates."""
    log("\nTemplates:", "blue")

    counts = {}

    # List templates directory
    if TEMPLATES_DIR.exists():
        for subdir in sorted(TEMPLATES_DIR.iterdir()):
            if subdir.is_dir():
                ttype = subdir.name
                if type_filter and ttype != type_filter:
                    continue

                files = list(subdir.glob("*"))
                files = [f for f in files if f.is_file() and not f.name.startswith(".")]
                counts[ttype] = len(files)

                if files:
                    log(f"\n  {ttype}/ ({len(files)})", "green")
                    for f in sorted(files)[:10]:
                        log(f"    {f.stem}", "dim")
                    if len(files) > 10:
                        log(f"    ... +{len(files) - 10} more", "dim")

    # List skills
    if not type_filter or type_filter == "skills":
        skills = [d for d in SKILLS_DIR.iterdir()
                  if d.is_dir() and (d / "SKILL.md").exists()]
        counts["skills"] = len(skills)

        if skills:
            log(f"\n  skills/ ({len(skills)})", "green")
            for s in sorted(skills, key=lambda x: x.name)[:10]:
                log(f"    {s.name}", "dim")
            if len(skills) > 10:
                log(f"    ... +{len(skills) - 10} more", "dim")

    # Summary
    total = sum(counts.values())
    log(f"\nTotal: {total} templates", "bold")

    log("\nNext steps:", "bold")
    hint("/template pull <source>           # Add more templates")
    hint("/kit add <kit> <template>         # Organize into kits")
