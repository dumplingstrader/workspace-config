# Resource Tools - Session Handoff

> **Purpose:** AI context restoration. Update at end of each session.

**Last Updated:** 2026-01-21

---

## Quick Context

Lightweight indexing system for 288 AI resources (16 Claude skills, 137 Copilot agents, 135 Copilot prompts). Reduces token cost by ~94% by searching metadata indexes instead of loading full content.

## Current State

- **Status:** Implemented and tested
- **Resources indexed:** 288 (2170 KB source → 111 KB index)
- **Core files:** `index_builder.py` (creates indexes), `resource_loader.py` (search/get/list)
- **Indexes:** Generated into `indexes/` directory (git-ignored)

## Key Commands

```bash
cd resource-tools
python index_builder.py                    # Rebuild index
python resource_loader.py search "keyword" # Search resources
python resource_loader.py get "Name"       # Load full content
python resource_loader.py list             # List all resources
python resource_loader.py stats            # View statistics
```

## Blockers

- None currently

## Next Steps

- Set up automated index rebuilding (git hook or scheduled)
- Consider pruning unused resources from the index
- MCP server integration (requires Node.js) if needed
