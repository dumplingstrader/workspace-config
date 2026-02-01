# E:\_Development Workspace - Session Handoff

> **Purpose:** AI context restoration. Update at end of each session.

**Last Updated:** 2026-02-01

---

## Quick Context

Home development workspace with 4 active projects plus a work documentation export. Uses Claude CLI for AI-assisted development across 3 machines via GitHub.

## Current State

### CLAUDE.md Improvements (this session)
- Added **Workflow Rules** section with 5 rules: re-plan on failure, diff against main, simplicity first, autonomous bug fixing, test-first bug fixes
- Added **Learned Corrections** section — persistent place for behavioral corrections that carry across sessions (say "add that to CLAUDE.md" when correcting Claude)
- Evaluated `claude-mem` plugin for session memory — decided against it (overkill for the problem; CLAUDE.md is the right tool for curated corrections)
- Added `_reference/claude-mem-main/` to `.gitignore`

### Project Status
| Project | State | Key Detail |
|---------|-------|------------|
| ControlsBMW | Pre-launch | Content backlog being built, persona defined |
| controls-docs | Reference library | 8.8 GB vendor docs in _USB_SYNC_sources |
| finances | Working | 66 coins, 29 tests passing, $376K portfolio value |
| healthassistant | v3.0 deployed | React PWA + FastAPI, pushed to GitHub |

## Blockers

- None at workspace level

## Next Steps

- Start populating Learned Corrections as issues come up across projects
- Practice push-before-leave, pull-when-arrive git workflow across machines
- Run `claude mcp list` to audit connected MCP servers
- Consider whether `healthassistant` folder should be renamed to `health-assistant` (convention)
- Review `.github/instructions/` at workspace root — 150+ Copilot instruction files that do nothing for Claude CLI
