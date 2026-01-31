# Resource Tools - Cost-Effective AI Resource Management

A lightweight system for indexing and retrieving skills, agents, prompts, and instructions with minimal token usage. This reduces AI model costs by providing metadata-first search and lazy loading of full content.

## Problem Statement

When working with large collections of skills, agents, and prompts:
- Loading all content upfront wastes tokens (~500+ files, several MB)
- AI models need to search through massive context windows
- Costs increase significantly with full content loading

## Solution

This tool provides:
1. **Lightweight indexing** - Metadata catalog (names, descriptions, tags) without full content
2. **Smart search** - Find relevant resources by keyword with minimal tokens
3. **Lazy loading** - Load full content only when needed
4. **MCP Server** - Exposes tools for AI models to use efficiently

## Architecture

```
┌─────────────────────────────────────────┐
│  Resources (~500 files, several MB)     │
│  • .claude/skills/*.md                  │
│  • .github/awesome-copilot-main/agents  │
│  • prompts, instructions, etc.          │
└────────────────┬────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ Index Builder │  (Run once, or when resources change)
         └───────┬───────┘
                 │
                 ▼
    ┌────────────────────────┐
    │  Lightweight Indexes    │  (~50KB total)
    │  • master-index.json    │
    │  • skills-index.json    │
    │  • agents-index.json    │
    │  • prompts-index.json   │
    └────────┬───────────────┘
             │
             ▼
    ┌─────────────────┐
    │ Resource Loader │  (Search, List, Get)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   MCP Server    │  (Tools for AI)
    └─────────────────┘
```

## Quick Start

### 1. Build the Index

First, create lightweight indexes of all resources:

```bash
npm run build-index
```

This scans your resources and creates JSON indexes in `resource-tools/indexes/`.

**Output:**
```
Building resource index...

✓ Indexed 16 Claude skills
✓ Indexed 150+ Copilot agents
✓ Indexed 50+ Copilot prompts
✓ Indexed 30+ Copilot instructions

✓ Master index written to resource-tools/indexes/master-index.json

Statistics:
  Total resources: 250+
  Total content size: 2500 KB
  Index size: 45 KB
  Space savings: 98.2%
```

### 2. Search Resources

Search for relevant resources by keyword:

```bash
# Search for React-related resources
npm run search react

# Search only agents
node resource-loader.js search react --type=copilot-agent

# Include full content in results
node resource-loader.js search react --content
```

**Example output:**
```json
[
  {
    "name": "Expert React Frontend Engineer",
    "type": "copilot-agent",
    "description": "Expert React 19.2 frontend engineer specializing in modern hooks...",
    "path": ".github/awesome-copilot-main/agents/expert-react-frontend-engineer.agent.md",
    "size": "15.2 KB"
  }
]
```

### 3. Get Specific Resource

Load full content of a specific resource:

```bash
npm run get "Expert React Frontend Engineer"
```

### 4. List All Resources

Browse all available resources:

```bash
# List all resources
npm run list

# List only skills
npm run list claude-skill

# List only agents
npm run list copilot-agent
```

### 5. View Statistics

```bash
npm run stats
```

**Output:**
```json
{
  "totalResources": 250,
  "skills": 16,
  "agents": 150,
  "prompts": 50,
  "instructions": 34,
  "generatedAt": "2026-01-21T12:00:00.000Z"
}
```

## MCP Server Integration

The MCP server exposes these capabilities as tools for AI models:

### Available Tools

1. **search_resources** - Search by keyword (metadata only)
2. **get_resource** - Load full content by name
3. **list_resources** - Browse all resources
4. **get_resource_stats** - View statistics

### Start the MCP Server

```bash
npm run mcp
```

### MCP Configuration

Add to your Claude Desktop or VS Code MCP settings:

```json
{
  "mcpServers": {
    "resource-tools": {
      "command": "node",
      "args": ["c:\\_Development\\resource-tools\\mcp-server.js"]
    }
  }
}
```

Or use npx:

```json
{
  "mcpServers": {
    "resource-tools": {
      "command": "npx",
      "args": ["-y", "resource-tools", "mcp"],
      "cwd": "c:\\_Development"
    }
  }
}
```

## Usage Patterns for AI Models

### Cost-Effective Workflow

1. **Discovery** - Search for relevant resources (metadata only, ~1-2 KB)
   ```
   search_resources("react hooks") → Returns list with names & descriptions
   ```

2. **Selection** - User or AI picks the most relevant resource

3. **Loading** - Load only the selected resource's full content (~10-20 KB)
   ```
   get_resource("Expert React Frontend Engineer") → Returns full content
   ```

**Token Savings:**
- Traditional: Load all 250 resources (~2500 KB) = ~625K tokens
- This approach: Load index (45 KB) + 1 resource (15 KB) = ~15K tokens
- **Savings: 97%+ reduction in token usage**

### Example AI Interaction

```
User: "I need help with React performance optimization"

AI: [Searches resources]
    search_resources("react performance")

    Found 5 resources:
    1. Expert React Frontend Engineer
    2. React Performance Optimization prompt
    3. Frontend Performance instruction
    ...

    Loading "Expert React Frontend Engineer" for detailed guidance...
    get_resource("Expert React Frontend Engineer")

    [Uses loaded content to provide expert guidance]
```

## File Structure

```
resource-tools/
├── index-builder.js      # Scans resources, creates indexes
├── resource-loader.js    # Search, get, list functions
├── mcp-server.js         # MCP server exposing tools
├── package.json          # NPM scripts and metadata
├── README.md             # This file
└── indexes/              # Generated indexes (git-ignored)
    ├── master-index.json
    ├── skills-index.json
    ├── agents-index.json
    ├── prompts-index.json
    └── instructions-index.json
```

## Maintenance

### When to Rebuild Index

Rebuild the index when you:
- Add new skills, agents, prompts, or instructions
- Modify existing resource metadata
- Update resource descriptions

```bash
npm run build-index
```

### Automated Rebuilding

Add to your git hooks or CI/CD:

```bash
# .git/hooks/post-merge
#!/bin/bash
cd resource-tools
npm run build-index
```

## Resource Types

- **claude-skill** - Claude Code skills from `.claude/skills/`
- **copilot-agent** - GitHub Copilot agents (`.agent.md`)
- **copilot-prompt** - Reusable prompts (`.prompt.md`)
- **copilot-instruction** - File pattern instructions (`.instruction.md`)

## Benefits

1. **Cost Reduction** - 97%+ token savings on resource discovery
2. **Fast Search** - Query metadata without loading full content
3. **Scalable** - Works efficiently with 100s or 1000s of resources
4. **MCP Integration** - Easy integration with AI tools
5. **Lazy Loading** - Only load what you need
6. **Extensible** - Easy to add new resource types

## Technical Details

- **Index Format**: JSON with metadata (name, description, type, path, size, tags)
- **Search**: Case-insensitive substring matching on name and description
- **Sorting**: Exact matches first, then name matches, then description matches
- **Size Tracking**: Monitors content size for cost estimation
- **Node.js**: Pure Node.js implementation, no external dependencies

## License

MIT
