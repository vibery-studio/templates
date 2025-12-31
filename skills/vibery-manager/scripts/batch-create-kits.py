#!/usr/bin/env python3
"""Batch create kits with predefined configurations."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
STACKS_DIR = ROOT / "stacks"
TEMPLATES_DIR = ROOT / "templates"
SKILLS_DIR = ROOT / ".claude" / "skills"

# Colors
C = {"reset": "\033[0m", "green": "\033[32m", "yellow": "\033[33m", "blue": "\033[34m", "red": "\033[31m", "dim": "\033[2m", "bold": "\033[1m"}

def log(msg, color="reset"):
    print(f"{C.get(color, '')}{msg}{C['reset']}")

# Kit definitions
KITS = {
    "landing-page-pro": {
        "name": "Landing Page Pro",
        "description": "Ship beautiful landing pages fast with Next.js, Tailwind, and SEO optimization",
        "category": "frontend",
        "tags": ["nextjs", "tailwind", "landing-page", "seo", "marketing"],
        "agents": ["nextjs-developer", "tailwind-pro", "seo-specialist"],
        "skills": ["ui-ux-pro-max"],
        "commands": [],
        "hooks": [],
        "mcps": []
    },
    "saas-monetization": {
        "name": "SaaS Monetization",
        "description": "Integrate payments and subscriptions with Stripe and Polar for your SaaS",
        "category": "backend",
        "tags": ["stripe", "payments", "saas", "monetization", "subscriptions"],
        "agents": ["payment-integration", "stripe-pro"],
        "skills": ["better-auth"],
        "commands": ["add-authentication-system"],
        "hooks": [],
        "mcps": ["stripe"]
    },
    "auth-flow-kit": {
        "name": "Auth Flow Kit",
        "description": "Secure authentication flows with Better Auth, security auditing, and best practices",
        "category": "security",
        "tags": ["auth", "security", "jwt", "oauth", "authentication"],
        "agents": ["security-auditor"],
        "skills": ["better-auth"],
        "commands": ["add-authentication-system", "security-audit"],
        "hooks": [],
        "mcps": []
    },
    "api-builder": {
        "name": "API Builder",
        "description": "Design, build, and document REST APIs with best practices",
        "category": "backend",
        "tags": ["api", "rest", "backend", "documentation"],
        "agents": ["api-designer", "api-documenter", "backend-developer"],
        "skills": ["backend-development"],
        "commands": ["doc-api", "generate-api-documentation"],
        "hooks": [],
        "mcps": []
    },
    "brand-design": {
        "name": "Brand & Design",
        "description": "Create consistent brand identity and design systems",
        "category": "design",
        "tags": ["design", "branding", "ui", "design-system", "tailwind"],
        "agents": ["tailwind-pro"],
        "skills": ["ui-ux-pro-max", "brand-guidelines", "ui-styling"],
        "commands": [],
        "hooks": [],
        "mcps": []
    },
    "vue-complete": {
        "name": "Vue Complete",
        "description": "Full Vue.js development stack with styling and best practices",
        "category": "frontend",
        "tags": ["vue", "vuejs", "frontend", "tailwind"],
        "agents": ["vue-expert", "tailwind-pro"],
        "skills": ["ui-styling", "frontend-development"],
        "commands": [],
        "hooks": [],
        "mcps": []
    },
    "seo-optimizer": {
        "name": "SEO Optimizer",
        "description": "Improve search rankings with performance audits and SEO best practices",
        "category": "marketing",
        "tags": ["seo", "performance", "marketing", "optimization"],
        "agents": ["seo-specialist"],
        "skills": [],
        "commands": ["nextjs-performance-audit", "performance-audit", "optimize-bundle-size"],
        "hooks": [],
        "mcps": []
    }
}


def find_template(name: str, ttype: str) -> Path:
    """Find template file by name and type."""
    base_dir = TEMPLATES_DIR / f"{ttype}s"  # agent -> agents
    for ext in [".md", ".json"]:
        path = base_dir / f"{name}{ext}"
        if path.exists():
            return path
    return None


def find_skill(name: str) -> Path:
    """Find skill directory."""
    skill_dir = SKILLS_DIR / name
    if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
        return skill_dir
    return None


def find_mcp(name: str) -> Path:
    """Find MCP config file."""
    mcp_path = TEMPLATES_DIR / "mcps" / f"{name}.json"
    if mcp_path.exists():
        return mcp_path
    return None


def create_kit(kit_id: str, config: dict, dry_run: bool = False):
    """Create a single kit with all its contents."""
    kit_dir = STACKS_DIR / kit_id

    if kit_dir.exists():
        log(f"  ⚠ Kit exists, skipping: {kit_id}", "yellow")
        return False

    log(f"\n📦 Creating: {config['name']}", "blue")

    if dry_run:
        log("  [DRY RUN] Would create kit structure", "dim")
        return True

    # Create directories
    kit_dir.mkdir(parents=True)
    for subdir in ["agents", "commands", "skills", "hooks", "mcps"]:
        (kit_dir / subdir).mkdir()

    # Track what we actually add
    contents = {"agents": [], "commands": [], "skills": [], "hooks": [], "mcps": []}
    missing = []

    # Copy agents
    for agent in config.get("agents", []):
        src = find_template(agent, "agent")
        if src:
            dest = kit_dir / "agents" / src.name
            shutil.copy(src, dest)
            contents["agents"].append(src.name)
            log(f"  + agent: {agent}", "dim")
        else:
            missing.append(f"agent:{agent}")

    # Copy commands
    for cmd in config.get("commands", []):
        src = find_template(cmd, "command")
        if src:
            dest = kit_dir / "commands" / src.name
            shutil.copy(src, dest)
            contents["commands"].append(src.name)
            log(f"  + command: {cmd}", "dim")
        else:
            missing.append(f"command:{cmd}")

    # Copy skills
    for skill in config.get("skills", []):
        src = find_skill(skill)
        if src:
            dest = kit_dir / "skills" / skill
            shutil.copytree(src, dest)
            contents["skills"].append(skill)
            log(f"  + skill: {skill}", "dim")
        else:
            missing.append(f"skill:{skill}")

    # Copy hooks
    for hook in config.get("hooks", []):
        src = find_template(hook, "hook")
        if src:
            dest = kit_dir / "hooks" / src.name
            shutil.copy(src, dest)
            contents["hooks"].append(src.name)
            log(f"  + hook: {hook}", "dim")
        else:
            missing.append(f"hook:{hook}")

    # Copy MCPs
    for mcp in config.get("mcps", []):
        src = find_mcp(mcp)
        if src:
            dest = kit_dir / "mcps" / src.name
            shutil.copy(src, dest)
            contents["mcps"].append(src.name)
            log(f"  + mcp: {mcp}", "dim")
        else:
            missing.append(f"mcp:{mcp}")

    # Create kit.json manifest
    manifest = {
        "id": kit_id,
        "name": config["name"],
        "version": "1.0.0",
        "description": config["description"],
        "category": config["category"],
        "tags": config["tags"],
        "composable": [],
        "contents": contents
    }
    (kit_dir / "kit.json").write_text(json.dumps(manifest, indent=2) + "\n")

    # Create CLAUDE.md.prepend
    (kit_dir / "CLAUDE.md.prepend").write_text(f"""<!-- VIBERY-KIT:{kit_id}:v1.0.0 -->
## {config['name']}

{config['description']}

### Included
- Agents: {', '.join(config.get('agents', [])) or 'None'}
- Skills: {', '.join(config.get('skills', [])) or 'None'}
- Commands: {', '.join(config.get('commands', [])) or 'None'}
<!-- /VIBERY-KIT:{kit_id} -->
""")

    # Count items
    item_count = sum(len(v) for v in contents.values())
    log(f"  ✓ Created with {item_count} items", "green")

    if missing:
        log(f"  ⚠ Missing: {', '.join(missing)}", "yellow")

    return True


def main():
    import sys
    dry_run = "--dry-run" in sys.argv

    log("\n" + "="*50, "blue")
    log("🚀 Batch Kit Creator", "bold")
    log("="*50, "blue")

    if dry_run:
        log("[DRY RUN MODE]", "yellow")

    created = 0
    for kit_id, config in KITS.items():
        if create_kit(kit_id, config, dry_run):
            created += 1

    log(f"\n✓ Created {created}/{len(KITS)} kits", "green")

    if not dry_run:
        log("\nNext steps:", "bold")
        log("  → node scripts/sync-all.js     # Sync to website/CLI", "dim")
        log("  → npm run build                # Build website", "dim")


if __name__ == "__main__":
    main()
