# E:\_Development Workspace - Session Handoff

> **Purpose:** AI context restoration. Update at end of each session.

**Last Updated:** 2026-02-15

---

## Quick Context

Home development workspace with 4 active projects plus a work documentation export. Uses Claude CLI for AI-assisted development across 3 machines via GitHub.

## Current State

### OpenClaw Model Migration (2026-02-15)
- **Promoted `minimax/MiniMax-M2.5` to primary model** — qwen3:8b was underpowered for agent tasks
- **Created `local` agent** (`ollama/qwen3:8b`) for lightweight tasks (lookups, math, boilerplate)
- **Fallback chain:** `ollama/qwen3:8b` -> `moonshot/kimi-k2.5`
- **Added delegation rules** in `~/.openclaw/workspace/AGENTS.md` — main agent auto-delegates simple tasks to local agent via `sessions_spawn`
- **Cost validated:** ~$0.0003/turn cached, projected <$2/mo heavy use
- **Tested end-to-end:** Discord and Telegram confirmed working on MiniMax M2.5
- **MiniMax API funds added** — balance confirmed working

### Git Setup (2026-02-15)
- Global git identity: `controlsbmw-sys <controlsbmw@gmail.com>`
- Claude settings committed (tool permissions for brew, pip3, python3, npm, WebSearch, WebFetch)

### Strategic Plan Decisions (2026-02-15)
- **LanceDB stays disabled** — not needed until digital products / micro-SaaS phase (6-12 months)
- **`Documentation/` not yet ingested into OpenClaw** — must first identify top 3 time-consuming doc types at work per Lane 1 priorities, then selectively ingest

### Project Status
| Project | State | Key Detail |
|---------|-------|------------|
| ControlsBMW | Pre-launch | Content backlog being built, OpenClaw now on MiniMax M2.5 |
| controls-docs | Reference library | 8.8 GB vendor docs in _USB_SYNC_sources |
| finances | Working | 66 coins, 29 tests passing, $376K portfolio value |
| healthassistant | v3.0 deployed | React PWA + FastAPI, pushed to GitHub |

## Blockers

- None at workspace level

## Next Steps

- Identify top 3 time-consuming documentation tasks at work (Lane 1 — strategic plan priority 1)
- Selectively ingest relevant doc types from `Documentation/` into OpenClaw
- Monitor MiniMax M2.5 API usage and credit burn rate over next week
- Build out ControlsBMW content backlog and establish posting cadence
- Start populating Learned Corrections as issues come up across projects
- Consider whether `healthassistant` folder should be renamed to `health-assistant` (convention)
