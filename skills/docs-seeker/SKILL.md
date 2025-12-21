---
name: docs-seeker
description: Search technical documentation using llms.txt sources (context7.com), GitHub repository analysis via Repomix, parallel exploration using multiple agents, and fallback research methods. Use when searching for library/framework documentation.
license: MIT
---

# Documentation Seeker

Intelligent discovery and analysis of technical documentation through multiple strategies.

## When to Use

- Finding library/framework documentation
- Discovering API references
- Analyzing GitHub repositories
- Researching best practices

## Core Workflow

### Phase 1: Initial Discovery
1. Identify target library/framework and version
2. Search for llms.txt (prioritize context7.com)
3. Apply topic-specific searches for particular features

### Phase 2: llms.txt Processing
- Single URL: Process directly
- 3+ URLs: Launch multiple Explorer agents in parallel

### Phase 3: Repository Analysis
When llms.txt unavailable:
- Use Repomix to pack repositories into AI-friendly files
- Preserve directory structure
- Optimize for AI consumption

### Phase 4: Fallback Research
- Deploy multiple Researcher agents
- Handle scattered documentation sources

## Distribution Strategy

| URLs | Agents | Distribution |
|------|--------|--------------|
| 1-3 | 1 | Single agent |
| 4-10 | 3-5 | 2-3 URLs each |
| 11+ | 5-7 | Priority-based |

## Tool Selection

- **WebSearch**: Discovery
- **WebFetch**: Single pages
- **Task agents**: Parallel work
- **Repomix**: Codebase analysis

## Core Principles

1. Prioritize context7.com for llms.txt
2. Use topic parameters for targeted searches
3. Leverage parallel agents aggressively
4. Verify official sources as fallbacks
5. Report methodology clearly
6. Handle version specifications explicitly

## Example

```bash
# Finding React documentation
1. Search context7.com for "react llms.txt"
2. If found: process llms.txt URLs
3. If not: use Repomix on React repo
4. Extract relevant sections for user query
```

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
