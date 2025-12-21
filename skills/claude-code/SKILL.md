---
name: claude-code
description: Activate when users ask about Claude Code installation, slash commands, creating/managing Agent Skills, configuring MCP servers, setting up hooks/plugins, IDE integration (VS Code, JetBrains), CI/CD workflows, enterprise deployment (SSO, RBAC, sandboxing), or troubleshooting authentication/performance issues.
license: MIT
---

# Claude Code Expert

Claude Code is Anthropic's agentic coding tool that lives in the terminal, combining autonomous planning, execution, and validation with extensibility through skills, plugins, MCP servers, and hooks.

## When to Use

- Understanding Claude Code features and capabilities
- Installation, setup, and authentication
- Using slash commands for development workflows
- Creating or managing Agent Skills
- Configuring MCP servers for external tool integration
- Setting up hooks and plugins
- Troubleshooting Claude Code issues
- Enterprise deployment (SSO, sandboxing, monitoring)
- IDE integration (VS Code, JetBrains)
- CI/CD integration (GitHub Actions, GitLab)
- Advanced features (extended thinking, caching, checkpointing)

## Core Architecture

- **Subagents**: Specialized AI agents (planner, code-reviewer, tester, debugger, docs-manager, etc.)
- **Agent Skills**: Modular capabilities with instructions, metadata, and resources
- **Slash Commands**: User-defined operations in `.claude/commands/`
- **Hooks**: Shell commands executing in response to events
- **MCP Servers**: Model Context Protocol integrations
- **Plugins**: Packaged collections of commands, skills, hooks, and MCP servers

## Common Workflows

### Feature Implementation
```bash
/cook implement user authentication with JWT
/plan implement payment integration with Stripe
```

### Bug Fixing
```bash
/fix:fast the login button is not working
/debug the API returns 500 errors intermittently
/fix:types  # Fix TypeScript errors
```

### Code Review & Testing
```bash
claude "review my latest commit"
/test
/fix:test the user service tests are failing
```

### Documentation
```bash
/docs:init      # Create initial documentation
/docs:update    # Update existing docs
```

### Git Operations
```bash
/git:cm         # Stage and commit
/git:cp         # Stage, commit, and push
/git:pr branch  # Create pull request
```

## Resources

- Main docs: https://docs.claude.com/claude-code
- GitHub: https://github.com/anthropics/claude-code

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
