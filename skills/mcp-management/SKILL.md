---
name: mcp-management
description: Manage Model Context Protocol (MCP) server integrations - discover tools/prompts/resources, analyze relevance for tasks, and execute MCP capabilities. Use when working with MCP servers, discovering available MCP tools, or implementing MCP client functionality.
license: MIT
---

# MCP Management

Comprehensive system for managing Model Context Protocol servers and capabilities.

## When to Use

- Discover MCP capabilities
- Select appropriate tools for tasks
- Execute MCP tools programmatically
- Build MCP client implementations
- Manage context efficiently through delegation

## Architecture

### Execution Tiers

1. **Gemini CLI** (preferred)
   - Automatic tool discovery
   - Natural language execution
   - Faster than subagent orchestration

2. **Direct Scripts**
   - Manual control via command-line
   - Fine-grained execution

3. **Subagent Delegation**
   - Keeps main context clean
   - Offloads MCP operations

## Configuration

Store in `.claude/.mcp.json`:

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

## Tool Discovery

```bash
# List available tools
mcp-client list-tools

# Save to catalog
mcp-client discover --output assets/tools.json
```

## Key Components

- **mcp-client.ts**: Server connections, capability listing
- **cli.ts**: Command-line operations
- **tools.json**: Persistent tool catalog

## Design Patterns

- Progressive disclosure of MCP capabilities
- Persistent tool catalog for fast reference
- Offline browsing enabled
- Version control for tool configurations

## Common Servers

- **filesystem**: File operations
- **github**: Repository operations
- **postgres**: Database queries
- **slack**: Team messaging
- **memory**: Persistent storage

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
