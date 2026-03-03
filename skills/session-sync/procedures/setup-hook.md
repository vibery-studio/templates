# Setup Auto-Sync Hook Procedure

Configure Claude Code to auto-sync sessions on exit.

## Check Current State

```bash
cat ~/.claude/settings.json | grep -A5 '"Stop"'
```

If output contains `session-sync.py sync`, hook is already configured.

## Add Hook

1. Read current settings:
```bash
cat ~/.claude/settings.json
```

2. Edit `~/.claude/settings.json` to add Stop hook.

If `hooks` key exists, add to it:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/session-sync/scripts/session-sync.py sync",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

If `hooks.Stop` already exists, append to the array.

3. Validate JSON syntax:
```bash
python3 -c "import json; json.load(open('$HOME/.claude/settings.json'))"
```

If error, fix JSON syntax before proceeding.

## Update Config

Mark auto_sync as enabled:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py config --auto-sync true
```

## Verify

```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py status
```

Should show: `✓ Auto-sync hook: enabled`

## How It Works

On session Stop event, Claude Code:
1. Passes `{"session_id": "...", "transcript_path": "..."}` via stdin
2. Script reads current session JSONL
3. Exports to `{target_folder}/Claude-Sessions/{project}/`
4. Outputs "Synced: {session_id}"

## Disable Hook

Remove the Stop hook entry from `~/.claude/settings.json`.

Then update config:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py config --auto-sync false
```
