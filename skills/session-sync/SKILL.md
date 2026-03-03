---
name: session-sync
description: Export Claude Code sessions to searchable markdown with QMD integration. Use when user says "sync sessions", "export sessions", "search sessions", "session history", or wants to backup/search past conversations. Don't use for live note-taking, meeting transcripts, or non-Claude-Code content.
---

# Session Sync

Export Claude Code sessions to project-organized markdown. Integrates with QMD for semantic search.

## Quick Start

```bash
# First time setup (cross-platform)
python ~/.claude/skills/session-sync/scripts/session-sync.py setup

# Export all sessions
python ~/.claude/skills/session-sync/scripts/session-sync.py export --all

# Search sessions
python ~/.claude/skills/session-sync/scripts/session-sync.py search "authentication"
```

> **Note:** Use `python` on Windows, `python3` on macOS/Linux. The setup command auto-detects your platform.

## Commands

| Command | Description |
|---------|-------------|
| `setup` | Interactive onboarding (auto-detects platform) |
| `status` | Show config, QMD status, export stats |
| `export` | Export sessions. Filters: `--all`, `--days N`, `--project NAME`, `--since DATE` |
| `index` | Re-index exported sessions in QMD |
| `search QUERY` | BM25 keyword search via QMD |
| `vsearch QUERY` | Semantic vector search via QMD |
| `config` | Set `--target-folder`, `--collection-name` |
| `list-projects` | List available Claude Code projects |
| `sync` | Sync current session (used by Stop hook or manually) |

## Cross-Platform Paths

| Platform | Claude Data | Default Output |
|----------|-------------|----------------|
| macOS    | `~/.claude` | `~/Documents/Claude-Sessions` |
| Linux    | `~/.claude` | `~/Documents/Claude-Sessions` |
| Windows  | `C:\Users\<user>\.claude` | `C:\Users\<user>\Documents\Claude-Sessions` |

## Procedures

### Setup (First Time)

1. Run setup (auto-detects platform):
   ```bash
   # macOS/Linux
   python3 ~/.claude/skills/session-sync/scripts/session-sync.py setup

   # Windows (PowerShell)
   python $env:USERPROFILE\.claude\skills\session-sync\scripts\session-sync.py setup
   ```

2. Follow prompts to set target folder and install QMD if needed

3. Export sessions:
   ```bash
   python ~/.claude/skills/session-sync/scripts/session-sync.py export --all
   ```

### Export Sessions

1. Determine filter from user request:
   - "all sessions" → `--all`
   - "last N days" → `--days N`
   - "project X" → `--project X`
   - "since DATE" → `--since YYYY-MM-DD`

2. Run export:
   ```bash
   python ~/.claude/skills/session-sync/scripts/session-sync.py export [FLAGS]
   ```

3. Re-index QMD:
   ```bash
   python ~/.claude/skills/session-sync/scripts/session-sync.py index
   ```

### Search Sessions

1. Keyword search:
   ```bash
   python ~/.claude/skills/session-sync/scripts/session-sync.py search "QUERY" -n 10
   ```

2. Semantic search:
   ```bash
   python ~/.claude/skills/session-sync/scripts/session-sync.py vsearch "QUERY" -n 10
   ```

### Sync Current Session

For manual sync (without hook):
```bash
export CK_SESSION_ID=<session-id>
python ~/.claude/skills/session-sync/scripts/session-sync.py sync
```

## Troubleshooting

### QMD Not Found

**macOS/Linux:**
```bash
npm install -g qmd
# or
bun install -g qmd
```

**Windows:**
```powershell
npm install -g qmd
```

If using nvm, ensure QMD is installed in active Node version.

### QMD Vector Search Crash (Bun)

If you see `NAPI finalizer` errors with `vsearch`:
```bash
# Add to shell profile (~/.zshrc, ~/.bashrc, or PowerShell $PROFILE)
alias qmd="QMD_RUNTIME=node qmd"
```

### No Sessions Found

Check Claude Code data exists:
- macOS/Linux: `ls ~/.claude/projects/`
- Windows: `dir $env:USERPROFILE\.claude\projects\`

## Output Format

Sessions exported to `{target_folder}/Claude-Sessions/{project-name}/`:

```yaml
---
type: claude-session
project: vibelabs-agentic-platform
date: 2026-03-03
session_id: abc12345-...
title: "Implement auth module"
messages: 42
created: 2026-03-03T10:00:00Z
last_activity: 2026-03-03T12:30:00Z
cwd: /path/to/project
git_branch: main
---
```

## Configuration

Config file: `~/.claude/skills/session-sync/config.json`

| Key | Default | Description |
|-----|---------|-------------|
| `target_folder` | `~/Documents` | Parent folder for Claude-Sessions |
| `collection_name` | `claude-sessions` | QMD collection name |
| `auto_sync` | `false` | Whether hook is configured |

## References

- procedures/setup.md - Detailed setup steps
- procedures/install-qmd.md - QMD installation guide
- procedures/setup-hook.md - Auto-sync hook configuration
- references/schema.md - Session markdown schema
