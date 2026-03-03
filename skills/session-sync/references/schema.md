# Session Markdown Schema

## Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `claude-session` |
| `project` | string | yes | Project name extracted from CWD |
| `date` | string | yes | Session date `YYYY-MM-DD` |
| `session_id` | string | yes | Full UUID of session |
| `title` | string | yes | First user message or custom title (max 100 chars) |
| `messages` | number | yes | Count of user messages |
| `created` | string | no | ISO timestamp of first message |
| `last_activity` | string | no | ISO timestamp of last message |
| `cwd` | string | no | Working directory path |
| `git_branch` | string | no | Git branch name |

## Example

```yaml
---
type: claude-session
project: vibelabs-agentic-platform
date: 2026-03-03
session_id: abc12345-1234-5678-9abc-def012345678
title: "Implement authentication module"
messages: 42
created: 2026-03-03T10:00:00.000Z
last_activity: 2026-03-03T12:30:45.123Z
cwd: /Applications/MAMP/htdocs/vibelabs/agentic-platform
git_branch: feature/auth
---

# Implement authentication module

## Conversation

**User:**

Add JWT authentication to the API...

---

**Assistant:**

I'll implement JWT authentication...

---
```

## Body Structure

1. H1 heading with title
2. `## Conversation` section
3. Alternating `**User:**` and `**Assistant:**` blocks
4. Horizontal rules between messages
5. Long messages (>2000 chars) truncated with `*[truncated...]*`

## File Naming

Pattern: `{date}-{session_id_prefix}.md`

Example: `2026-03-03-abc12345.md`

- Date: `YYYY-MM-DD`
- Session ID prefix: first 8 characters of UUID

## Directory Structure

```
{target_folder}/
└── Claude-Sessions/
    ├── project-a/
    │   ├── 2026-03-01-abc12345.md
    │   └── 2026-03-02-def67890.md
    ├── project-b/
    │   └── 2026-03-03-ghi11111.md
    └── unknown/
        └── 2026-03-03-jkl22222.md
```

Project names derived from CWD by stripping common prefixes:
- `Applications-MAMP-htdocs-`
- `Users-{username}-`
