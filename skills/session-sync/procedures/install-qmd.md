# Install QMD Procedure

QMD provides semantic search for session exports.

## Check Current State

```bash
which qmd || echo "NOT_INSTALLED"
```

If installed, verify working:
```bash
qmd --version
qmd status
```

## Install via npm (Recommended)

```bash
npm install -g @tobilu/qmd
```

## Install via bun

```bash
bun install -g @tobilu/qmd
```

## Post-Install Verification

```bash
qmd --version
```

Expected output: version number like `1.x.x`

## Common Errors

### better-sqlite3 Module Error

Error message contains: `NODE_MODULE_VERSION` mismatch

Fix:
```bash
npm rebuild better-sqlite3 -g
```

Or reinstall:
```bash
npm uninstall -g @tobilu/qmd && npm install -g @tobilu/qmd
```

### Command Not Found After Install

The npm/bun bin path may not be in PATH.

Find QMD location:
```bash
npm root -g
# QMD at: $(npm root -g)/../bin/qmd
```

Or use full path in commands:
```bash
/Users/$(whoami)/.nvm/versions/node/v20.20.0/bin/qmd status
```

### Permission Denied

```bash
sudo npm install -g @tobilu/qmd
```

Or use nvm to manage Node without sudo.

## Verify Integration

After successful install:
```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py status
```

Should show: `✓ QMD installed: /path/to/qmd`
