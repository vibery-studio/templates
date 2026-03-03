#!/usr/bin/env python3
"""Session Sync - Export Claude Code sessions to searchable markdown.

Usage:
    session-sync setup                     # Interactive onboarding
    session-sync sync                      # Sync current session (for hooks)
    session-sync export [OPTIONS]          # Export sessions
    session-sync index                     # Re-index in QMD
    session-sync search QUERY              # Search via QMD
    session-sync vsearch QUERY             # Semantic search via QMD
    session-sync status                    # Show status
    session-sync config [OPTIONS]          # Configure settings
    session-sync list-projects             # List available projects
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

__version__ = "1.0.0"

# Paths
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
PROJECTS_DIR = Path.home() / ".claude" / "projects"
SETTINGS_FILE = Path.home() / ".claude" / "settings.json"

# Default config
DEFAULT_CONFIG = {
    "target_folder": str(Path.home() / "Documents"),
    "qmd_path": "qmd",
    "collection_name": "claude-sessions",
    "auto_sync": False,
}


def load_config() -> dict:
    """Load config from file or return defaults."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Save config to file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_output_dir(config: dict) -> Path:
    """Get output directory from config."""
    target = config.get("target_folder") or str(Path.home() / "Documents")
    return Path(target).expanduser() / "Claude-Sessions"


def find_qmd() -> str | None:
    """Find QMD executable."""
    import platform
    is_windows = platform.system() == "Windows"

    # First check PATH
    qmd_in_path = shutil.which("qmd")
    if qmd_in_path:
        return qmd_in_path

    home = Path.home()
    candidates = []

    if is_windows:
        # Windows: npm global, AppData, etc.
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        localappdata = Path(os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
        candidates = [
            appdata / "npm/qmd.cmd",
            appdata / "npm/qmd",
            localappdata / "pnpm/qmd.cmd",
            home / ".bun/bin/qmd.exe",
        ]
        # Check nvm-windows
        nvm_home = Path(os.environ.get("NVM_HOME", home / "AppData/Roaming/nvm"))
        if nvm_home.exists():
            for node_ver in nvm_home.iterdir():
                if node_ver.is_dir():
                    candidates.append(node_ver / "qmd.cmd")
    else:
        # Unix: common locations
        candidates = [
            home / ".bun/bin/qmd",
            home / ".local/bin/qmd",
            Path("/usr/local/bin/qmd"),
        ]
        # Check nvm versions dynamically
        nvm_dir = home / ".nvm/versions/node"
        if nvm_dir.exists():
            for node_ver in nvm_dir.iterdir():
                qmd_path = node_ver / "bin/qmd"
                if qmd_path.exists():
                    candidates.insert(0, qmd_path)

    for qmd in candidates:
        if qmd.exists():
            return str(qmd)

    return None


def parse_project_name(cwd: str) -> str:
    """Extract clean project name from CWD path or project dirname."""
    if not cwd:
        return "unknown"

    # If it's a full path, extract the last component
    path = Path(cwd)
    name = path.name if path.name else cwd

    # Clean up the name (remove leading dashes from Claude project dirs)
    name = name.lstrip("-")

    # Remove common prefixes (from Claude's project directory naming)
    # Handle paths like "Applications-MAMP-htdocs-project" or "Users-username-projects-project"
    parts = name.split("-")
    # Find where the actual project name starts (after common path segments)
    common_segments = {"Applications", "Users", "MAMP", "htdocs", "home", "projects", "code", "dev", "src", "repos"}
    start_idx = 0
    for i, part in enumerate(parts):
        if part in common_segments or (len(part) <= 2 and part.isalpha()):
            start_idx = i + 1
        else:
            break
    if start_idx > 0 and start_idx < len(parts):
        name = "-".join(parts[start_idx:])

    return name or "unknown"


def extract_session_data(jsonl_path: Path) -> dict | None:
    """Extract session metadata and conversation from JSONL file."""
    records = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception:
        return None

    if not records:
        return None

    data = {
        "session_id": None,
        "date": None,
        "title": None,
        "messages": 0,
        "first_timestamp": None,
        "last_timestamp": None,
        "conversation": [],
        "cwd": None,
        "git_branch": None,
    }

    for record in records:
        if record.get("sessionId") and not data["session_id"]:
            data["session_id"] = record["sessionId"]

        if record.get("type") == "user":
            timestamp = record.get("timestamp", "")
            if timestamp:
                if not data["date"]:
                    data["date"] = timestamp.split("T")[0]
                if not data["first_timestamp"]:
                    data["first_timestamp"] = timestamp
                data["last_timestamp"] = timestamp

            data["messages"] += 1

            if record.get("cwd") and not data["cwd"]:
                data["cwd"] = record["cwd"]
            if record.get("gitBranch") and not data["git_branch"]:
                data["git_branch"] = record["gitBranch"]

            msg = record.get("message", {})
            content = msg.get("content", "")
            text = ""
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text", "")
                        break

            if text and not record.get("isMeta"):
                data["conversation"].append({"role": "user", "content": text})

        if record.get("type") == "assistant":
            msg = record.get("message", {})
            contents = msg.get("content", [])
            text_parts = []
            if isinstance(contents, list):
                for item in contents:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
            if text_parts:
                data["conversation"].append({"role": "assistant", "content": "\n".join(text_parts)})

        if record.get("type") == "custom-title":
            custom_title = record.get("customTitle", "")
            if custom_title:
                data["title"] = custom_title.split("\n")[0].strip()[:100]

        if record.get("type") == "summary" and not data["title"]:
            summary = record.get("summary", "")
            if summary:
                data["title"] = summary.split("\n")[0].strip()[:100]

    if not data["title"] and data["conversation"]:
        for msg in data["conversation"]:
            if msg["role"] == "user":
                data["title"] = msg["content"].replace("\n", " ").strip()[:80]
                break

    if not data["date"]:
        data["date"] = datetime.now().strftime("%Y-%m-%d")

    return data


def generate_markdown(data: dict, project_name: str) -> str:
    """Generate markdown content from session data."""
    lines = []

    lines.append("---")
    lines.append("type: claude-session")
    lines.append(f"project: {project_name}")
    lines.append(f"date: {data['date']}")
    lines.append(f"session_id: {data['session_id']}")

    title = data["title"] or "Untitled Session"
    title_escaped = title.replace('"', '\\"').replace("\n", " ")
    lines.append(f'title: "{title_escaped}"')

    lines.append(f"messages: {data['messages']}")

    if data["first_timestamp"]:
        lines.append(f"created: {data['first_timestamp']}")
    if data["last_timestamp"]:
        lines.append(f"last_activity: {data['last_timestamp']}")
    if data["cwd"]:
        lines.append(f"cwd: {data['cwd']}")
    if data["git_branch"]:
        lines.append(f"git_branch: {data['git_branch']}")

    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Conversation")
    lines.append("")

    for msg in data["conversation"]:
        role = "**User:**" if msg["role"] == "user" else "**Assistant:**"
        content = msg["content"]
        if len(content) > 2000:
            content = content[:2000] + "\n\n*[truncated...]*"
        lines.append(role)
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def export_session(jsonl_path: Path, output_dir: Path) -> bool:
    """Export a single session to markdown."""
    data = extract_session_data(jsonl_path)
    if not data or data["messages"] == 0:
        return False

    project_name = parse_project_name(data["cwd"]) if data["cwd"] else "unknown"
    project_output = output_dir / project_name
    project_output.mkdir(parents=True, exist_ok=True)

    filename = f"{data['date']}-{data['session_id'][:8]}.md"
    output_file = project_output / filename

    md_content = generate_markdown(data, project_name)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    return True


# =============================================================================
# Commands
# =============================================================================

def cmd_status(args):
    """Show current status."""
    config = load_config()
    output_dir = get_output_dir(config)
    qmd_path = find_qmd()

    print("Session Sync Status")
    print("=" * 40)
    print()

    # Config
    print(f"Target folder: {config['target_folder']}")
    print(f"Output dir:    {output_dir}")
    print(f"Auto-sync:     {'enabled' if config.get('auto_sync') else 'disabled'}")
    print()

    # QMD
    if qmd_path:
        print(f"✓ QMD installed: {qmd_path}")
        try:
            result = subprocess.run([qmd_path, "status"], capture_output=True, text=True, timeout=10)
            if "Documents" in result.stdout:
                for line in result.stdout.split("\n"):
                    if "Total:" in line or "Vectors:" in line or "claude-sessions" in line:
                        print(f"  {line.strip()}")
        except Exception:
            pass
    else:
        print("✗ QMD not installed")
        print("  Install: npm install -g @tobilu/qmd")
    print()

    # Sessions
    if output_dir.exists():
        projects = [d for d in output_dir.iterdir() if d.is_dir()]
        total_sessions = sum(len(list(p.glob("*.md"))) for p in projects)
        print(f"✓ Exported: {total_sessions} sessions in {len(projects)} projects")
    else:
        print("✗ No sessions exported yet")
    print()

    # Hook
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE) as f:
                settings = json.load(f)
            hooks = settings.get("hooks", {}).get("Stop", [])
            has_hook = any("session-sync" in str(h) for h in hooks)
            if has_hook:
                print("✓ Auto-sync hook: enabled")
            else:
                print("✗ Auto-sync hook: not configured")
        except Exception:
            print("? Auto-sync hook: unable to check")

    return 0


def cmd_sync(args):
    """Sync current session (called by hook or manually)."""
    config = load_config()
    output_dir = get_output_dir(config)

    session_id = None
    transcript_path = None

    # Try stdin first (for hook usage)
    if not sys.stdin.isatty():
        try:
            stdin_data = json.load(sys.stdin)
            session_id = stdin_data.get("session_id")
            transcript_path = stdin_data.get("transcript_path")
        except Exception:
            pass

    # Fallback to env vars (for manual usage)
    if not session_id:
        session_id = os.environ.get("CK_SESSION_ID")
    if not transcript_path and session_id:
        # Find transcript in projects dir
        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            jsonl = project_dir / f"{session_id}.jsonl"
            if jsonl.exists():
                transcript_path = str(jsonl)
                break

    if not session_id or not transcript_path:
        print("No session found. Use 'export --days 1' instead.")
        return 1

    jsonl_path = Path(transcript_path)
    if not jsonl_path.exists():
        print(f"Session file not found: {transcript_path}")
        return 1

    if export_session(jsonl_path, output_dir):
        print(f"✓ Synced: {session_id[:8]}")

    return 0


def cmd_export(args):
    """Export sessions with filters."""
    config = load_config()
    output_dir = get_output_dir(config)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine time filter
    cutoff = None
    if args.days:
        cutoff = time.time() - (args.days * 86400)
    elif args.since:
        try:
            cutoff = datetime.strptime(args.since, "%Y-%m-%d").timestamp()
        except ValueError:
            print(f"Invalid date format: {args.since} (use YYYY-MM-DD)")
            return 1

    # Find projects
    project_dirs = sorted(PROJECTS_DIR.glob("-*"))
    if args.project:
        project_dirs = [d for d in project_dirs if args.project in d.name]

    total = 0
    projects_processed = 0

    for project_dir in project_dirs:
        if not project_dir.is_dir():
            continue

        project_sessions = 0
        jsonl_files = list(project_dir.glob("*.jsonl"))

        for jsonl_file in jsonl_files:
            # Apply time filter
            if cutoff and jsonl_file.stat().st_mtime < cutoff:
                continue

            if export_session(jsonl_file, output_dir):
                project_sessions += 1
                total += 1

        if project_sessions > 0:
            project_name = parse_project_name(project_dir.name)
            print(f"✓ {project_name}: {project_sessions} sessions")
            projects_processed += 1

    print()
    print(f"✓ Exported {total} sessions from {projects_processed} projects")
    print(f"✓ Location: {output_dir}")

    return 0


def cmd_index(args):
    """Re-index sessions in QMD."""
    config = load_config()
    output_dir = get_output_dir(config)
    qmd_path = find_qmd()

    if not qmd_path:
        print("ERROR: QMD not installed")
        print("Install: npm install -g @tobilu/qmd")
        return 1

    collection = config.get("collection_name", "claude-sessions")

    # Remove existing collection
    subprocess.run([qmd_path, "collection", "remove", collection],
                   capture_output=True, text=True)

    # Add collection
    print(f"Adding collection: {collection}")
    result = subprocess.run(
        [qmd_path, "collection", "add", str(output_dir), "--name", collection],
        capture_output=True, text=True
    )
    print(result.stdout)

    # Embed
    print("Generating embeddings...")
    result = subprocess.run([qmd_path, "embed"], capture_output=True, text=True)
    print(result.stdout)

    return 0


def cmd_search(args):
    """Search sessions via QMD."""
    config = load_config()
    qmd_path = find_qmd()

    if not qmd_path:
        print("ERROR: QMD not installed")
        return 1

    collection = config.get("collection_name", "claude-sessions")
    cmd = [qmd_path, "search", args.query, "-c", collection, "-n", str(args.n)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode


def cmd_vsearch(args):
    """Semantic search via QMD."""
    config = load_config()
    qmd_path = find_qmd()

    if not qmd_path:
        print("ERROR: QMD not installed")
        return 1

    collection = config.get("collection_name", "claude-sessions")
    cmd = [qmd_path, "vsearch", args.query, "-c", collection, "-n", str(args.n)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode


def cmd_config(args):
    """Configure settings."""
    config = load_config()

    if args.target_folder:
        config["target_folder"] = args.target_folder
        print(f"Set target_folder: {args.target_folder}")

    if args.collection_name:
        config["collection_name"] = args.collection_name
        print(f"Set collection_name: {args.collection_name}")

    if args.auto_sync is not None:
        config["auto_sync"] = args.auto_sync
        print(f"Set auto_sync: {args.auto_sync}")

    save_config(config)
    print(f"Config saved to: {CONFIG_FILE}")

    return 0


def cmd_list_projects(args):
    """List available projects."""
    project_dirs = sorted(PROJECTS_DIR.glob("-*"))

    print("Available projects:")
    print()

    for project_dir in project_dirs:
        if not project_dir.is_dir():
            continue

        jsonl_count = len(list(project_dir.glob("*.jsonl")))
        if jsonl_count > 0:
            project_name = parse_project_name(project_dir.name)
            print(f"  {project_name}: {jsonl_count} sessions")

    return 0


def cmd_setup(args):
    """Interactive setup."""
    import platform
    is_windows = platform.system() == "Windows"
    py_cmd = "python" if is_windows else "python3"
    skill_path = str(SKILL_DIR / "scripts" / "session-sync.py")

    print("Session Sync Setup")
    print("=" * 40)
    print()

    # This is meant to be run by the agent interactively
    # Just show what needs to be done

    print("To complete setup, the agent should:")
    print()
    print("1. DETECT INSTALL STATUS")
    print(f"   Run: {py_cmd} \"{skill_path}\" status")
    print()
    print("2. SET TARGET FOLDER")
    print("   Ask user for target folder (default: ~/Documents)")
    print(f"   Run: {py_cmd} \"{skill_path}\" config --target-folder PATH")
    print()
    print("3. INSTALL QMD (if not installed)")
    print("   Run: npm install -g @tobilu/qmd")
    if is_windows:
        print("   If errors: npm rebuild better-sqlite3 -g")
    else:
        print("   If errors on macOS/Linux: npm rebuild better-sqlite3 -g")
    print()
    print("4. EXPORT SESSIONS")
    print(f"   Run: {py_cmd} \"{skill_path}\" export --all")
    print("   Or with filter: export --days 90")
    print()
    print("5. INDEX IN QMD")
    print(f"   Run: {py_cmd} \"{skill_path}\" index")
    print()
    print("6. SETUP AUTO-SYNC HOOK (optional)")
    settings_path = "~/.claude/settings.json" if not is_windows else "%USERPROFILE%\\.claude\\settings.json"
    print(f"   Add to {settings_path} hooks.Stop:")
    print(f'   {{"type": "command", "command": "{py_cmd} \\"{skill_path}\\" sync", "timeout": 10}}')
    print()

    return 0


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Session Sync - Export Claude sessions to markdown")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # setup
    p_setup = subparsers.add_parser("setup", help="Interactive setup")
    p_setup.set_defaults(func=cmd_setup)

    # status
    p_status = subparsers.add_parser("status", help="Show status")
    p_status.set_defaults(func=cmd_status)

    # sync
    p_sync = subparsers.add_parser("sync", help="Sync current session (for hooks)")
    p_sync.set_defaults(func=cmd_sync)

    # export
    p_export = subparsers.add_parser("export", help="Export sessions")
    p_export.add_argument("--all", action="store_true", help="Export all sessions")
    p_export.add_argument("--days", type=int, help="Export sessions from last N days")
    p_export.add_argument("--since", help="Export sessions since date (YYYY-MM-DD)")
    p_export.add_argument("--project", help="Export specific project only")
    p_export.set_defaults(func=cmd_export)

    # index
    p_index = subparsers.add_parser("index", help="Re-index in QMD")
    p_index.set_defaults(func=cmd_index)

    # search
    p_search = subparsers.add_parser("search", help="Search sessions (keyword)")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("-n", type=int, default=10, help="Number of results")
    p_search.set_defaults(func=cmd_search)

    # vsearch
    p_vsearch = subparsers.add_parser("vsearch", help="Search sessions (semantic)")
    p_vsearch.add_argument("query", help="Search query")
    p_vsearch.add_argument("-n", type=int, default=10, help="Number of results")
    p_vsearch.set_defaults(func=cmd_vsearch)

    # config
    p_config = subparsers.add_parser("config", help="Configure settings")
    p_config.add_argument("--target-folder", help="Set target folder")
    p_config.add_argument("--collection-name", help="Set QMD collection name")
    p_config.add_argument("--auto-sync", type=bool, help="Enable/disable auto-sync")
    p_config.set_defaults(func=cmd_config)

    # list-projects
    p_list = subparsers.add_parser("list-projects", help="List available projects")
    p_list.set_defaults(func=cmd_list_projects)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
