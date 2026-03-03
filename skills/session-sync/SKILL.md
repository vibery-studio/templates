---
name: session-sync
description: Export Claude Code sessions to searchable markdown with QMD integration. Use when user says "sync sessions", "export sessions", "search sessions", "session history", or wants to backup/search past conversations. Don't use for live note-taking, meeting transcripts, or non-Claude-Code content.
---

# Session Sync

Export Claude Code sessions to project-organized markdown. Integrates with QMD for semantic search.

## Quick Start

```bash
# First time setup
python3 ~/.claude/skills/session-sync/scripts/session-sync.py setup

# Export all sessions
python3 ~/.claude/skills/session-sync/scripts/session-sync.py export --all

# Search sessions
python3 ~/.claude/skills/session-sync/scripts/session-sync.py search "authentication"
```

## Commands

| Command         | Description                                                                     |
| --------------- | ------------------------------------------------------------------------------- |
| `setup`         | Interactive onboarding. See procedures/setup.md                                 |
| `status`        | Show config, QMD status, export stats                                           |
| `export`        | Export sessions. Filters: `--all`, `--days N`, `--project NAME`, `--since DATE` |
| `index`         | Re-index exported sessions in QMD                                               |
| `search QUERY`  | BM25 keyword search via QMD                                                     |
| `vsearch QUERY` | Semantic vector search via QMD                                                  |
| `config`        | Set `--target-folder`, `--collection-name`                                      |
| `list-projects` | List available Claude Code projects                                             |
| `sync`          | Sync current session (used by Stop hook)                                        |

## Procedures

### Setup (First Time)

1. Run status check: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py status`
2. If target folder not set, ask user for path (default: `~/Documents`)
3. Run: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py config --target-folder PATH`
4. If QMD not installed, see procedures/install-qmd.md
5. Export sessions: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py export --all`
6. Index in QMD: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py index`
7. Ask user if they want auto-sync hook. If yes, see procedures/setup-hook.md

### Export Sessions

1. Determine filter from user request:
   - "all sessions" → `--all`
   - "last N days" → `--days N`
   - "project X" → `--project X`
   - "since DATE" → `--since YYYY-MM-DD`
2. Run: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py export [FLAGS]`
3. After export, ask if user wants to re-index QMD
4. If yes: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py index`

### Search Sessions

1. Determine search type:
   - Exact keywords → `search`
   - Conceptual/semantic → `vsearch`
2. Run: `python3 ~/.claude/skills/session-sync/scripts/session-sync.py [search|vsearch] "QUERY" -n 10`
3. If no results, suggest alternative query or check if sessions are indexed

### Troubleshooting

- QMD not found: See procedures/install-qmd.md
- Hook not working: See procedures/setup-hook.md
- No sessions exported: Check `~/.claude/projects/` contains JSONL files

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

| Key               | Default           | Description                       |
| ----------------- | ----------------- | --------------------------------- |
| `target_folder`   | `~/Documents`     | Parent folder for Claude-Sessions |
| `collection_name` | `claude-sessions` | QMD collection name               |
| `auto_sync`       | `false`           | Whether hook is configured        |

## References

- procedures/setup.md - Detailed setup steps
- procedures/install-qmd.md - QMD installation guide
- procedures/setup-hook.md - Auto-sync hook configuration
- references/schema.md - Session markdown schema
