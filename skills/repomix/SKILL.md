---
name: repomix
description: Package entire code repositories into single AI-friendly files using Repomix. Generate multiple output formats (XML, Markdown, plain text), preserve file structure, optimize for AI consumption with token counting, filter by file types. Use when packaging codebases for AI analysis or code review.
license: MIT
---

# Repomix

Package repositories into consolidated files optimized for LLM processing.

## When to Use

- Code review preparation
- Security audits
- Documentation generation
- Bug investigation
- Implementation planning
- Sharing codebases with AI tools

## Installation

```bash
# npm
npm install -g repomix

# Homebrew
brew install repomix
```

## Quick Start

```bash
# Pack current directory
repomix

# Pack specific directory
repomix ./src

# Pack remote repository
repomix --remote https://github.com/user/repo
```

## Output Formats

```bash
# XML (default)
repomix --output output.xml

# Markdown
repomix --style markdown --output output.md

# Plain text
repomix --style plain --output output.txt

# JSON
repomix --style json --output output.json
```

## Filtering

```bash
# Include only specific patterns
repomix --include "src/**/*.ts,src/**/*.tsx"

# Exclude patterns
repomix --exclude "node_modules,dist,*.test.ts"

# Comment removal
repomix --remove-comments
```

## Key Features

- Git-aware processing (respects .gitignore)
- Token counting for context management
- Remote repository support without cloning
- Comment removal across 18+ languages
- Secretlint integration for sensitive data detection
- Clipboard copy capability

## LLM Context Limits

| Model | Context |
|-------|---------|
| Claude Sonnet 4.5 | ~200K tokens |
| GPT-4 | ~128K tokens |
| GPT-3.5 | ~16K tokens |

## Security

- Always review output before sharing
- Use `.repomixignore` for sensitive files
- Avoid packaging `.env` files
- Enable secretlint for automatic detection

## Configuration

Create `repomix.config.json`:

```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Resources

- GitHub: https://github.com/yamadashy/repomix
- Docs: https://repomix.com

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
