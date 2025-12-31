#!/usr/bin/env python3
"""Validate kit structures and contents."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
STACKS_DIR = ROOT / "stacks"
TEMPLATES_DIR = ROOT / "templates"
SKILLS_DIR = ROOT / ".claude" / "skills"

# Colors
C = {"reset": "\033[0m", "green": "\033[32m", "yellow": "\033[33m", "red": "\033[31m", "dim": "\033[2m", "bold": "\033[1m"}

def log(msg, color="reset"):
    print(f"{C.get(color, '')}{msg}{C['reset']}")


def validate_kit(kit_dir: Path) -> dict:
    """Validate a single kit and return results."""
    kit_id = kit_dir.name
    results = {"id": kit_id, "valid": True, "errors": [], "warnings": [], "items": 0}

    # Check kit.json exists
    manifest_file = kit_dir / "kit.json"
    if not manifest_file.exists():
        results["errors"].append("Missing kit.json")
        results["valid"] = False
        return results

    # Parse kit.json
    try:
        manifest = json.loads(manifest_file.read_text())
    except json.JSONDecodeError as e:
        results["errors"].append(f"Invalid kit.json: {e}")
        results["valid"] = False
        return results

    # Required fields
    required = ["id", "name", "version", "description", "contents"]
    for field in required:
        if field not in manifest:
            results["errors"].append(f"Missing required field: {field}")
            results["valid"] = False

    # Check CLAUDE.md.prepend
    if not (kit_dir / "CLAUDE.md.prepend").exists():
        results["warnings"].append("Missing CLAUDE.md.prepend")

    # Validate contents match actual files
    contents = manifest.get("contents", {})

    # Check agents
    declared_agents = contents.get("agents", [])
    actual_agents = list((kit_dir / "agents").glob("*.md")) if (kit_dir / "agents").exists() else []
    for agent in declared_agents:
        agent_name = agent if agent.endswith(".md") else f"{agent}.md"
        if not (kit_dir / "agents" / agent_name).exists():
            results["errors"].append(f"Declared agent not found: {agent}")
            results["valid"] = False
    results["items"] += len(actual_agents)

    # Check commands
    declared_cmds = contents.get("commands", [])
    actual_cmds = list((kit_dir / "commands").glob("*.md")) if (kit_dir / "commands").exists() else []
    for cmd in declared_cmds:
        cmd_name = cmd if cmd.endswith(".md") else f"{cmd}.md"
        if not (kit_dir / "commands" / cmd_name).exists():
            results["errors"].append(f"Declared command not found: {cmd}")
            results["valid"] = False
    results["items"] += len(actual_cmds)

    # Check skills
    declared_skills = contents.get("skills", [])
    actual_skills = [d for d in (kit_dir / "skills").iterdir() if d.is_dir()] if (kit_dir / "skills").exists() else []
    for skill in declared_skills:
        skill_dir = kit_dir / "skills" / skill
        if not skill_dir.exists():
            results["errors"].append(f"Declared skill not found: {skill}")
            results["valid"] = False
        elif not (skill_dir / "SKILL.md").exists():
            results["warnings"].append(f"Skill missing SKILL.md: {skill}")
    results["items"] += len(actual_skills)

    # Check hooks
    declared_hooks = contents.get("hooks", [])
    actual_hooks = list((kit_dir / "hooks").glob("*.json")) if (kit_dir / "hooks").exists() else []
    for hook in declared_hooks:
        hook_name = hook if hook.endswith(".json") else f"{hook}.json"
        if not (kit_dir / "hooks" / hook_name).exists():
            results["errors"].append(f"Declared hook not found: {hook}")
            results["valid"] = False
    results["items"] += len(actual_hooks)

    # Check MCPs
    declared_mcps = contents.get("mcps", [])
    actual_mcps = list((kit_dir / "mcps").glob("*.json")) if (kit_dir / "mcps").exists() else []
    for mcp in declared_mcps:
        mcp_name = mcp if mcp.endswith(".json") else f"{mcp}.json"
        if not (kit_dir / "mcps" / mcp_name).exists():
            results["errors"].append(f"Declared MCP not found: {mcp}")
            results["valid"] = False
    results["items"] += len(actual_mcps)

    # Check for empty description
    if not manifest.get("description"):
        results["warnings"].append("Empty description")

    # Check for empty tags
    if not manifest.get("tags"):
        results["warnings"].append("No tags defined")

    return results


def main():
    log("\n" + "="*50, "bold")
    log("🔍 Kit Validation Report", "bold")
    log("="*50 + "\n")

    if not STACKS_DIR.exists():
        log("No stacks directory found!", "red")
        return 1

    kits = [d for d in STACKS_DIR.iterdir() if d.is_dir() and (d / "kit.json").exists()]

    if not kits:
        log("No kits found!", "yellow")
        return 0

    total_valid = 0
    total_items = 0

    for kit_dir in sorted(kits):
        results = validate_kit(kit_dir)

        status = "✓" if results["valid"] else "✗"
        color = "green" if results["valid"] else "red"

        log(f"{status} {results['id']} ({results['items']} items)", color)

        for err in results["errors"]:
            log(f"    ✗ {err}", "red")

        for warn in results["warnings"]:
            log(f"    ⚠ {warn}", "yellow")

        if results["valid"]:
            total_valid += 1
        total_items += results["items"]

    log(f"\n{'='*50}", "dim")
    log(f"Total: {total_valid}/{len(kits)} valid kits, {total_items} items", "bold")

    if total_valid < len(kits):
        log("\n⚠ Some kits have validation errors!", "yellow")
        return 1

    log("\n✓ All kits valid!", "green")
    return 0


if __name__ == "__main__":
    exit(main())
