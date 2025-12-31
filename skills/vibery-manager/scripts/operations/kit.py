#!/usr/bin/env python3
"""Kit operations: create, add, remove, list."""

import json
import shutil
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
STACKS_DIR = ROOT / "stacks"
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
    print(f"{C['dim']}  → {msg}{C['reset']}")


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def kit_command(args: list, dry_run: bool = False):
    """Handle kit commands."""
    if not args:
        log("Usage: kit <create|add|remove|list> [args]", "yellow")
        return

    action = args[0]

    if action == "create":
        if len(args) < 2:
            log("Usage: kit create <name>", "yellow")
            return
        create_kit(args[1], dry_run)

    elif action == "add":
        if len(args) < 3:
            log("Usage: kit add <kit-name> <item>", "yellow")
            return
        add_to_kit(args[1], args[2], dry_run)

    elif action == "remove":
        if len(args) < 3:
            log("Usage: kit remove <kit-name> <item>", "yellow")
            return
        remove_from_kit(args[1], args[2], dry_run)

    elif action == "list":
        kit_name = args[1] if len(args) > 1 else None
        list_kits(kit_name)

    else:
        log(f"Unknown action: {action}", "red")


def create_kit(name: str, dry_run: bool = False):
    """Create a new kit scaffold."""
    kit_dir = STACKS_DIR / name

    if kit_dir.exists():
        log(f"Kit already exists: {name}", "yellow")
        hint(f"/kit add {name} <item>            # Add to existing kit")
        return

    log(f"\nCreating kit: {name}", "blue")

    if not dry_run:
        # Create directories
        kit_dir.mkdir(parents=True, exist_ok=True)
        (kit_dir / "agents").mkdir()
        (kit_dir / "commands").mkdir()
        (kit_dir / "skills").mkdir()
        (kit_dir / "hooks").mkdir()
        (kit_dir / "mcps").mkdir()

        # Create kit.json
        manifest = {
            "id": name,
            "name": name.replace("-", " ").title(),
            "version": "1.0.0",
            "description": "",
            "category": "general",
            "composable": [],
            "contents": {
                "agents": [],
                "commands": [],
                "skills": [],
                "hooks": [],
                "mcps": []
            },
            "tags": []
        }
        save_json(kit_dir / "kit.json", manifest)

        # Create CLAUDE.md.prepend scaffold
        (kit_dir / "CLAUDE.md.prepend").write_text(f"""<!-- VIBERY-KIT:{name}:v1.0.0 -->
## {name.replace('-', ' ').title()}

### Stack Context
- **Purpose**: [Description]

### Key Patterns
[Add patterns and guidelines here]

### Rules
[Add rules here]
<!-- /VIBERY-KIT:{name} -->
""")

    log(f"✓ Created kit: {kit_dir.relative_to(ROOT)}", "green")
    log("\nCreated structure:", "dim")
    log(f"  {name}/", "dim")
    log(f"    kit.json", "dim")
    log(f"    CLAUDE.md.prepend", "dim")
    log(f"    agents/", "dim")
    log(f"    commands/", "dim")
    log(f"    skills/", "dim")
    log(f"    hooks/", "dim")
    log(f"    mcps/", "dim")

    log("\nNext steps:", "bold")
    hint(f"Edit {name}/kit.json to add description and tags")
    hint(f"/kit add {name} <template>         # Add templates")
    hint(f"/kit add {name} <skill>            # Add skills")


def find_item(name: str) -> dict:
    """Find a template or skill by name."""
    # Check skills first
    skill_dir = SKILLS_DIR / name
    if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
        return {"type": "skill", "path": skill_dir, "name": name}

    # Check templates directory
    for subdir in TEMPLATES_DIR.iterdir():
        if subdir.is_dir():
            for ext in [".md", ".json"]:
                filepath = subdir / f"{name}{ext}"
                if filepath.exists():
                    return {
                        "type": subdir.name.rstrip("s"),  # agents -> agent
                        "path": filepath,
                        "name": name
                    }

    return None


def add_to_kit(kit_name: str, item_name: str, dry_run: bool = False):
    """Add a template or skill to a kit."""
    kit_dir = STACKS_DIR / kit_name
    manifest_file = kit_dir / "kit.json"

    if not manifest_file.exists():
        log(f"Kit not found: {kit_name}", "red")
        hint(f"/kit create {kit_name}            # Create it first")
        return

    # Find the item
    item = find_item(item_name)
    if not item:
        log(f"Item not found: {item_name}", "red")
        hint("/template list                   # View available templates")
        return

    log(f"\nAdding to {kit_name}: {item['type']} '{item_name}'", "blue")

    manifest = load_json(manifest_file)
    item_type = item["type"]

    # Map type to manifest key
    type_to_key = {
        "skill": "skills",
        "agent": "agents",
        "command": "commands",
        "hook": "hooks",
        "mcp": "mcps"
    }
    key = type_to_key.get(item_type, f"{item_type}s")

    # Check if already in kit
    if key not in manifest.get("contents", {}):
        manifest["contents"][key] = []

    if item_type == "skill":
        # Copy entire skill folder
        dest = kit_dir / "skills" / item_name
        if not dry_run:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item["path"], dest)

        # Add to manifest
        if item_name not in manifest["contents"][key]:
            manifest["contents"][key].append(item_name)

        log(f"  + Copied skill folder to kit", "dim")

    else:
        # Copy single file
        dest = kit_dir / f"{key}" / item["path"].name
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item["path"], dest)

        # Add to manifest
        filename = item["path"].name
        if filename not in manifest["contents"][key]:
            manifest["contents"][key].append(filename)

        log(f"  + Copied {filename} to kit", "dim")

    # Save manifest
    if not dry_run:
        save_json(manifest_file, manifest)

    log(f"\n✓ Added '{item_name}' to '{kit_name}'", "green")

    log("\nChanged:", "bold")
    log(f"  {kit_name}/kit.json", "dim")
    if item_type == "skill":
        log(f"  {kit_name}/skills/{item_name}/", "dim")
    else:
        log(f"  {kit_name}/{key}/{item['path'].name}", "dim")

    log("\nNext steps:", "bold")
    hint(f"/kit add {kit_name} <more-items>   # Add more to this kit")
    hint(f"/kit list {kit_name}               # View kit contents")
    hint(f"/sync                              # Sync to web + CLI when ready")


def remove_from_kit(kit_name: str, item_name: str, dry_run: bool = False):
    """Remove an item from a kit."""
    kit_dir = STACKS_DIR / kit_name
    manifest_file = kit_dir / "kit.json"

    if not manifest_file.exists():
        log(f"Kit not found: {kit_name}", "red")
        return

    log(f"\nRemoving from {kit_name}: {item_name}", "blue")

    manifest = load_json(manifest_file)
    removed = False

    # Search in all content types
    for key in ["agents", "commands", "skills", "hooks", "mcps"]:
        items = manifest.get("contents", {}).get(key, [])
        matching = [i for i in items if item_name in i]

        for match in matching:
            if not dry_run:
                # Remove from manifest
                manifest["contents"][key].remove(match)

                # Remove file/folder
                if key == "skills":
                    path = kit_dir / "skills" / item_name
                    if path.exists():
                        shutil.rmtree(path)
                else:
                    path = kit_dir / key / match
                    if path.exists():
                        path.unlink()

            log(f"  - Removed {key}/{match}", "dim")
            removed = True

    if removed:
        if not dry_run:
            save_json(manifest_file, manifest)
        log(f"\n✓ Removed '{item_name}' from '{kit_name}'", "green")

        log("\nNext steps:", "bold")
        hint(f"/kit list {kit_name}               # View updated contents")
        hint(f"/sync                              # Sync to web + CLI when ready")
    else:
        log(f"Item not found in kit: {item_name}", "yellow")
        hint(f"/kit list {kit_name}               # View kit contents")


def list_kits(kit_name: str = None):
    """List all kits or contents of a specific kit."""
    if not STACKS_DIR.exists():
        log("No kits found", "yellow")
        hint("/kit create <name>                # Create your first kit")
        return

    if kit_name:
        # Show specific kit contents
        kit_dir = STACKS_DIR / kit_name
        manifest_file = kit_dir / "kit.json"

        if not manifest_file.exists():
            log(f"Kit not found: {kit_name}", "red")
            return

        manifest = load_json(manifest_file)
        log(f"\n{manifest.get('name', kit_name)} v{manifest.get('version', '?')}", "blue")
        log(f"  {manifest.get('description', 'No description')}", "dim")

        contents = manifest.get("contents", {})
        for key in ["agents", "commands", "skills", "hooks", "mcps"]:
            items = contents.get(key, [])
            if items:
                log(f"\n  {key}/", "green")
                for item in items:
                    log(f"    {item}", "dim")

        if manifest.get("composable"):
            log(f"\n  Composable with: {', '.join(manifest['composable'])}", "dim")

        log("\nNext steps:", "bold")
        hint(f"/kit add {kit_name} <item>         # Add more items")
        hint(f"/kit remove {kit_name} <item>      # Remove items")

    else:
        # List all kits
        kits = []
        for kit_dir in sorted(STACKS_DIR.iterdir()):
            if kit_dir.is_dir():
                manifest_file = kit_dir / "kit.json"
                if manifest_file.exists():
                    manifest = load_json(manifest_file)
                    kits.append({
                        "id": kit_dir.name,
                        "name": manifest.get("name", kit_dir.name),
                        "version": manifest.get("version", "?"),
                        "description": manifest.get("description", ""),
                        "contents": manifest.get("contents", {})
                    })

        if not kits:
            log("\nNo kits found", "yellow")
            hint("/kit create <name>                # Create your first kit")
            return

        log(f"\nKits ({len(kits)}):", "blue")
        for kit in kits:
            # Count contents
            total = sum(len(v) for v in kit["contents"].values() if isinstance(v, list))
            log(f"\n  {kit['id']} v{kit['version']} ({total} items)", "green")
            log(f"    {kit['description']}", "dim")

        log("\nNext steps:", "bold")
        hint("/kit list <kit-name>              # View kit contents")
        hint("/kit create <name>                # Create new kit")
        hint("/sync                             # Sync to web + CLI")
