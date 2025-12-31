#!/usr/bin/env python3
"""Sync operations: generate registry, ZIPs, website data."""

import json
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
STACKS_DIR = ROOT / "stacks"
TEMPLATES_DIR = ROOT / "templates"
SKILLS_DIR = ROOT / ".claude" / "skills"
CLI_DIR = ROOT / "cli"
WEBSITE_DIR = ROOT / "website"

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


def file_hash(path: Path) -> str:
    """Calculate file hash for change detection."""
    if path.is_file():
        return hashlib.md5(path.read_bytes()).hexdigest()[:8]
    return ""


def sync_command(dry_run: bool = False):
    """Sync all content to website and CLI."""
    log("\nSyncing Vibery content...", "blue")

    changes = {
        "templates": [],
        "kits": [],
        "zips": []
    }

    # 1. Generate template registry for CLI
    log("\n[1/4] Generating template registry...", "bold")
    changes["templates"] = sync_templates(dry_run)

    # 2. Generate kit registry for CLI
    log("\n[2/4] Generating kit registry...", "bold")
    changes["kits"] = sync_kits(dry_run)

    # 3. Generate kit ZIPs for website downloads
    log("\n[3/4] Generating kit ZIPs...", "bold")
    changes["zips"] = generate_zips(dry_run)

    # 4. Generate website data
    log("\n[4/4] Updating website data...", "bold")
    sync_website_data(dry_run)

    # Summary
    total = len(changes["templates"]) + len(changes["kits"]) + len(changes["zips"])
    log(f"\n✓ Sync complete: {total} items updated", "green")

    if changes["templates"]:
        log(f"\n  Templates: {len(changes['templates'])}", "dim")
    if changes["kits"]:
        log(f"  Kits: {len(changes['kits'])}", "dim")
    if changes["zips"]:
        log(f"  ZIPs: {len(changes['zips'])}", "dim")

    log("\nGenerated files:", "bold")
    log("  cli/registry.json", "dim")
    log("  cli/kits.json", "dim")
    log("  website/public/kits/*.zip", "dim")
    log("  website/src/data/kits.json", "dim")

    log("\nNext steps:", "bold")
    hint("node scripts/sync-all.js          # Sync templates.json (required)")
    hint("/publish                          # Deploy to production")
    hint("git add . && git commit           # Commit changes")


def sync_templates(dry_run: bool = False) -> list:
    """Generate template registry for CLI."""
    registry = {
        "version": datetime.now().strftime("%Y%m%d"),
        "templates": []
    }

    updated = []

    # Scan templates directory
    if TEMPLATES_DIR.exists():
        for subdir in sorted(TEMPLATES_DIR.iterdir()):
            if subdir.is_dir():
                ttype = subdir.name.rstrip("s")  # agents -> agent
                for f in sorted(subdir.glob("*")):
                    if f.is_file() and not f.name.startswith("."):
                        template = {
                            "id": f.stem,
                            "name": f.stem.replace("-", " ").title(),
                            "type": ttype,
                            "file": f.name,
                            "path": str(f.relative_to(ROOT)),
                            "hash": file_hash(f)
                        }
                        registry["templates"].append(template)
                        updated.append(f.stem)
                        log(f"  + {ttype}: {f.stem}", "dim")

    # Scan skills
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                template = {
                    "id": skill_dir.name,
                    "name": skill_dir.name.replace("-", " ").title(),
                    "type": "skill",
                    "path": str(skill_dir.relative_to(ROOT)),
                    "hash": file_hash(skill_dir / "SKILL.md")
                }
                registry["templates"].append(template)
                updated.append(skill_dir.name)
                log(f"  + skill: {skill_dir.name}", "dim")

    # Save registry
    registry_file = CLI_DIR / "registry.json"
    if not dry_run:
        save_json(registry_file, registry)

    log(f"  → {len(registry['templates'])} templates indexed", "green")

    return updated


def sync_kits(dry_run: bool = False) -> list:
    """Generate kit registry for CLI."""
    kits = {
        "version": datetime.now().strftime("%Y%m%d"),
        "kits": []
    }

    updated = []

    if STACKS_DIR.exists():
        for kit_dir in sorted(STACKS_DIR.iterdir()):
            if kit_dir.is_dir():
                manifest_file = kit_dir / "kit.json"
                if manifest_file.exists():
                    manifest = load_json(manifest_file)
                    manifest["path"] = str(kit_dir.relative_to(ROOT))

                    # Count items
                    contents = manifest.get("contents", {})
                    manifest["item_count"] = sum(
                        len(v) for v in contents.values() if isinstance(v, list)
                    )

                    kits["kits"].append(manifest)
                    updated.append(manifest.get("id", kit_dir.name))
                    log(f"  + kit: {manifest.get('id', kit_dir.name)}", "dim")

    # Save registry
    kits_file = CLI_DIR / "kits.json"
    if not dry_run:
        save_json(kits_file, kits)

    log(f"  → {len(kits['kits'])} kits indexed", "green")

    return updated


def generate_zips(dry_run: bool = False) -> list:
    """Generate downloadable ZIP files for each kit."""
    zips_dir = WEBSITE_DIR / "public" / "kits"
    if not dry_run:
        zips_dir.mkdir(parents=True, exist_ok=True)

    generated = []

    if STACKS_DIR.exists():
        for kit_dir in sorted(STACKS_DIR.iterdir()):
            if kit_dir.is_dir() and (kit_dir / "kit.json").exists():
                kit_name = kit_dir.name
                zip_path = zips_dir / f"{kit_name}.zip"

                if not dry_run:
                    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                        for file in kit_dir.rglob("*"):
                            if file.is_file() and not file.name.startswith("."):
                                arcname = file.relative_to(kit_dir.parent)
                                zf.write(file, arcname)

                generated.append(kit_name)
                log(f"  + {kit_name}.zip", "dim")

    log(f"  → {len(generated)} ZIPs generated", "green")

    return generated


def sync_website_data(dry_run: bool = False):
    """Update website JSON data files (kits only - templates handled by JS sync)."""
    data_dir = WEBSITE_DIR / "src" / "data"
    if not dry_run:
        data_dir.mkdir(parents=True, exist_ok=True)

    # Generate kits.json for website (ONLY kits, not templates)
    kits_data = {
        "lastUpdated": datetime.now().isoformat(),
        "kits": []
    }

    if STACKS_DIR.exists():
        for kit_dir in sorted(STACKS_DIR.iterdir()):
            if kit_dir.is_dir():
                manifest_file = kit_dir / "kit.json"
                if manifest_file.exists():
                    manifest = load_json(manifest_file)
                    # Read USE-CASES.md if exists
                    use_cases_file = kit_dir / "USE-CASES.md"
                    use_cases_content = ""
                    if use_cases_file.exists():
                        use_cases_content = use_cases_file.read_text()

                    kit_data = {
                        "id": manifest.get("id", kit_dir.name),
                        "name": manifest.get("name", ""),
                        "version": manifest.get("version", "1.0.0"),
                        "description": manifest.get("description", ""),
                        "category": manifest.get("category", "general"),
                        "tags": manifest.get("tags", []),
                        "composable": manifest.get("composable", []),
                        "downloadUrl": f"/kits/{kit_dir.name}.zip",
                        "contents": manifest.get("contents", {}),
                        "itemCount": sum(
                            len(v) for v in manifest.get("contents", {}).values()
                            if isinstance(v, list)
                        ),
                        "useCases": use_cases_content
                    }
                    kits_data["kits"].append(kit_data)

    if not dry_run:
        save_json(data_dir / "kits.json", kits_data)

    log(f"  + website/src/data/kits.json", "dim")
    # NOTE: templates.json is handled ONLY by node scripts/sync-all.js
    # DO NOT generate templates.json here - it causes conflicts
    log(f"  → Website kits data updated", "green")
    log(f"  ⚠ templates.json: use 'node scripts/sync-all.js' separately", "yellow")
