# claude-config

Canonical Claude Code user-level settings, kept here so they can be synced
across every workstation instead of drifting independently in each
machine's `%USERPROFILE%\.claude\settings.json`.

## Why this exists

Permission-allowlist rules approved with "don't ask again" during a session
mostly land in **project-scoped** settings files
(`.claude/settings.local.json`), not the durable, cross-project
`~/.claude/settings.json`. Those project files are also gitignored and
machine-specific, so nothing actually transfers between workstations, and
some accumulate stale entries referencing paths that only exist on the
machine they were created on.

This folder holds the one file that's meant to be identical everywhere:
the user-level settings that should apply on every machine, for every
project.

## Files

- **`settings.user.json`** -- the canonical Claude Code user settings
  (`permissions.allow`, `defaultMode`, and general preferences). This is
  what gets copied into place as `~/.claude/settings.json`.
- **`sync_claude_settings.ps1`** -- copies `settings.user.json` into
  `%USERPROFILE%\.claude\settings.json` on the current machine, backing up
  whatever's already there first (`settings.json.bak`, overwritten each
  run -- it's a one-generation safety net, not a history).

## Usage

**On a new or existing workstation, after pulling the latest changes:**

```powershell
cd C:\_Development
git pull
powershell -File claude-config\sync_claude_settings.ps1
```

Permission rules reload live in Claude Code -- no restart needed after
syncing, even mid-session.

**When you want to change the permanent, cross-machine ruleset:** edit
`settings.user.json` directly (or ask Claude to add a specific rule to it),
then commit + push from whichever machine you're on, and run the sync
script (or `git pull` + sync) on every other machine to pick it up.

## What deliberately does NOT belong here

- **Anything machine-specific** -- e.g. `permissions.additionalDirectories`
  pointing at a path that only exists on one machine. Those belong in that
  project's own `.claude/settings.local.json` on that machine, not here.
- **Anything security-sensitive or mutating** -- this file only ever grants
  read-only command patterns (git status/diff/log/show, node --check,
  PowerShell `Get-*`/`Select-Object`/etc.) plus a deliberately-chosen small
  set of git-mutating commands (`add`/`commit`/`pull`/`branch`, not `push`).
  Never add `permissions.deny` overrides here casually, and never widen a
  rule to arbitrary code execution (a bare interpreter, shell, or package
  runner) -- see the reasoning trail in the session that created this file
  if you need the full rationale for what's included and excluded.

## History

Created 2026-07-07 out of a Fable 5-assisted planning session that scanned
real Claude Code transcripts across all local projects to ground the
allowlist in actual usage rather than guesses. See root `HANDOFF.md` for
the dated session entry.
