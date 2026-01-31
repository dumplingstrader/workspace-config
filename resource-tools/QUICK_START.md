# Quick Start Guide

## What This Does

This tool reduces AI token costs by **94.9%** when working with your skills, agents, and prompts. Instead of loading 2+ MB of content, you search a lightweight 111 KB index and only load what you need.

## Setup (One Time)

Build the index of all your resources:

```bash
cd resource-tools
python index_builder.py
```

**Output:**
```
Building resource index...

[OK] Indexed 16 Claude skills
[OK] Indexed 137 Copilot agents
[OK] Indexed 135 Copilot prompts
[OK] Indexed 0 Copilot instructions

[OK] Master index written to resource-tools\indexes\master-index.json
[OK] Separate indexes written

Statistics:
  Total resources: 288
  Total content size: 2170.23 KB
  Index size: 111.53 KB
  Space savings: 94.9%
```

## Usage

### Search for Resources

```bash
# Search for anything related to "react"
python resource_loader.py search react

# Search only agents
python resource_loader.py search react --type=copilot-agent

# Search only skills
python resource_loader.py search "frontend" --type=claude-skill

# Get full content in search results (not recommended - defeats the purpose!)
python resource_loader.py search react --content
```

### Get Specific Resource

After finding what you need, load the full content:

```bash
# Get by exact name
python resource_loader.py get "Expert React Frontend Engineer"

# Specify type to disambiguate
python resource_loader.py get "frontend-design" --type=claude-skill
```

### List All Resources

Browse everything available:

```bash
# List everything
python resource_loader.py list

# List only skills
python resource_loader.py list claude-skill

# List only agents
python resource_loader.py list copilot-agent

# List only prompts
python resource_loader.py list copilot-prompt
```

### Get Statistics

```bash
python resource_loader.py stats
```

## Common Workflows

### As an AI Model

**Old approach (expensive):**
- Load all 288 resources = 2170 KB = ~542,500 tokens
- Cost: $5.43 per interaction (at $10/M tokens)

**New approach (cheap):**
1. Search index: `python resource_loader.py search "react performance"`
   - Returns metadata only (~1 KB)
2. Load specific resource: `python resource_loader.py get "Expert React Frontend Engineer"`
   - Returns 25 KB
3. Total: 26 KB = ~6,500 tokens
4. Cost: $0.065 per interaction

**Savings: 98.8% reduction in tokens and cost!**

### Example: Finding Help with React

```bash
# Step 1: Search
$ python resource_loader.py search "react hooks" --type=copilot-agent

# Returns:
# - "Expert React Frontend Engineer" - looks perfect!

# Step 2: Load the resource
$ python resource_loader.py get "Expert React Frontend Engineer"

# Returns full content with detailed React 19.2 guidance
```

### Example: Discovering Available Skills

```bash
# See all Claude skills
$ python resource_loader.py list claude-skill

# Output shows:
# - algorithmic-art
# - brand-guidelines
# - canvas-design
# - doc-coauthoring
# - docx
# - frontend-design
# - ... and 10 more
```

## When to Rebuild Index

Rebuild when you:
- Add new skills, agents, or prompts
- Update existing resource descriptions
- Pull updates from the awesome-copilot repo

```bash
cd resource-tools
python index_builder.py
```

## Pro Tips

1. **Search First, Load Later** - Always search before loading full content
2. **Use Type Filters** - Narrow results with `--type=` for faster searches
3. **Check Stats** - Run `python resource_loader.py stats` to see what's indexed
4. **Automate Indexing** - Add to git hooks to rebuild on pulls

## Troubleshooting

### "Index not found" error

Run the index builder first:
```bash
cd resource-tools
python index_builder.py
```

### "Resource not found" error

The resource might have been renamed or moved. Search for it:
```bash
python resource_loader.py search "part of the name"
```

### Slow searches

The indexes are cached in memory. First search might be slower, subsequent searches are fast.

## Next Steps

- See [README.md](README.md) for full documentation
- Integrate with MCP for AI tool access (see README.md)
- Set up automated index rebuilding
