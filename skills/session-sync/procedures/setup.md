# Setup Procedure

Interactive onboarding for session-sync skill.

## Pre-flight Check

1. Run status to detect current install state:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py status
```

2. Parse output to determine what's configured:
   - Target folder set? Look for "Target folder:" line
   - QMD installed? Look for "✓ QMD installed" or "✗ QMD not installed"
   - Sessions exported? Look for "✓ Exported:" or "✗ No sessions"
   - Hook configured? Look for "✓ Auto-sync hook" or "✗ Auto-sync hook"

## Step 1: Set Target Folder

If target folder is default (`~/Documents`), ask user:
> "Where should I save your session exports? Default is ~/Documents/Claude-Sessions"

Run:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py config --target-folder "USER_PATH"
```

## Step 2: Install QMD

If QMD not installed, inform user:
> "QMD enables semantic search across your sessions. Install it?"

If yes, see procedures/install-qmd.md

If no, skip search features.

## Step 3: Export Sessions

Ask user what to export:
> "Export sessions from: (1) All time, (2) Last 30 days, (3) Last 90 days, (4) Specific project"

Run appropriate command:
```bash
# All
python3 ~/.claude/skills/session-sync/scripts/session-sync.py export --all

# Last N days
python3 ~/.claude/skills/session-sync/scripts/session-sync.py export --days 30

# Specific project - list first
python3 ~/.claude/skills/session-sync/scripts/session-sync.py list-projects
python3 ~/.claude/skills/session-sync/scripts/session-sync.py export --project PROJECT_NAME
```

## Step 4: Index in QMD

If QMD installed and sessions exported:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py index
```

## Step 5: Setup Auto-Sync Hook

Ask user:
> "Enable auto-sync on session end? This saves each session when you exit."

If yes, see procedures/setup-hook.md

## Completion

Run final status check:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py status
```

Report summary to user with checkmarks for each component.
