# Implementation Plan: AI CLI to Discord Notifier (for Codex)

**Audience:** OpenAI Codex CLI, executing this plan stage by stage.
**Inputs this plan is built from (read these first if you need more context):**
- `ai-cli-discord-architecture-prompt.md` -- original requirements prompt
- `ai-cli-discord-integration-architecture.md` -- architecture produced from that prompt
- `ai-cli-discord-integration-architecture-review.md` -- review of that architecture; the fixes below are baked into this plan so you don't need to re-derive them

**Ground rules (from workspace CLAUDE.md -- follow exactly):**
- Simplicity first: minimal code impact, root-cause fixes, no temporary workarounds.
- No Unicode characters (em-dashes, ellipses, smart quotes, checkmarks, arrows) in any PowerShell script or anything invoked through bash. ASCII only (`...` not `...`, `[OK]` not a checkmark).
- If an approach isn't working after one attempt, stop and re-plan instead of pushing forward.
- For non-trivial changes, diff against main before marking complete.
- Don't fabricate verification -- if a claim can't be confirmed against a real, currently-loadable doc page, mark it "not verified" in code comments/README rather than asserting it.

**Do not build in this pass** (carried over from the architecture, still correct): two-way Discord control, a custom VS Code extension, a persistent daemon, a database, an MCP server for notifications, a cloud relay, or terminal keystroke injection. Stop at Phase 3 below unless the user explicitly asks for the two-way PoC.

---

## Phase 0 -- Verification gate (do this before writing any adapter code)

The architecture review flagged that the Kimi and Grok hook claims, and some of the Claude Code hook event names (`PostToolUseFailure`, `StopFailure`, standalone `PermissionRequest`), were not independently confirmed and may be pattern-completed rather than real. Do not skip this phase -- it determines what Phase 5/6 actually build.

1. Fetch and read the current Claude Code hooks documentation. Record the actual, current hook event list (expect something close to `PreToolUse`, `PostToolUse`, `Notification`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `SessionStart`, `SessionEnd` -- confirm or correct this against the live page). Note whether `PostToolUseFailure`, `StopFailure`, and `PermissionRequest` exist as real event names or not.
2. Fetch and read the current Kimi Code CLI docs for its hook/config mechanism. Confirm or correct: config file name/location, hook config syntax (`[[hooks]]` TOML array claim), and the actual event names it supports.
3. Fetch and read the current xAI Grok Build CLI (`grok`) docs for its hook mechanism. Confirm or correct: hook directory (`~/.grok/hooks` / project `.grok/hooks` claim), config format, and event names. Specifically check whether it is actually "Claude-compatible" or whether that was an assumption.
4. Fetch and read the current OpenAI Codex CLI hooks docs. Confirm current Windows support status (the architecture claims hooks are "temporarily disabled on Windows" -- verify this is still true, since it directly decides whether Codex gets a native adapter or stays wrapper-only).
5. Write findings into `_audits/verification-notes.md` (new file) as a short table: vendor, claimed event list, confirmed event list, source URL actually opened, date checked, discrepancies found. This file is the record that Phase 5/6 adapters are built against real event names, not the original architecture doc's guesses.
6. If any vendor's hook claims turn out to be wrong or unconfirmable, downgrade that vendor to wrapper-only for this implementation pass (per the architecture's own fallback rule) and note it in `verification-notes.md` rather than guessing at a fixed syntax.

**Acceptance criteria:** `verification-notes.md` exists, cites a real URL per vendor, and every hook event name used anywhere else in this plan traces back to a row in that table.

---

## Phase 1 -- Project scaffold and shared notifier core

**Location:** create `~/.ai-notify/` (user-level, non-secret) per the architecture's proposed layout. On Windows this is `$env:USERPROFILE\.ai-notify\`.

Files to create:
```
~/.ai-notify/
  notifier.ps1          # shared core: Send-AiNotifyEvent, redaction, encoding
  wrap.ps1              # generic process wrapper (Phase 3)
  dequeue.ps1            # detached dequeue/POST loop (see note below)
  queue/                 # file-backed queue, gitignored, created at runtime
  logs/                  # redacted, rotated logs, gitignored, created at runtime
```

### Design correction from the review -- read before writing `notifier.ps1`
The architecture's original design showed enqueue and POST happening in one synchronous flow inside the same process that received the event (hook or wrapper). That cannot satisfy "non-blocking, never block the AI session" and also cannot survive across hook invocations, because each hook/wrapper call is a fresh short-lived process with no shared memory. Build it this way instead:

1. `notifier.ps1` exposes `Send-AiNotifyEvent` which does the *minimum synchronous work*: build the envelope, redact it, append one JSON line to a file-backed queue (`queue/pending.jsonl`, or one file per event if that's simpler to make atomic), and return immediately. No network call happens in this step. No in-memory queue -- file-backed only, always.
2. A separate, detached process handles delivery: `dequeue.ps1` reads `queue/pending.jsonl`, POSTs each entry to the Discord webhook with retry/backoff/jitter, honors 429/`Retry-After`, and removes/archives entries it successfully delivered (or drops them after max retries, per the queue-overflow rule). `Send-AiNotifyEvent` should kick this off via `Start-Process -WindowStyle Hidden -FilePath powershell -ArgumentList ...dequeue.ps1` (only if a dequeue process isn't already running -- use a lock file or `Get-Process` check to avoid spawning duplicates) rather than doing the POST inline.
3. This means the hook/wrapper call returns fast (write one line to disk) and the actual Discord delivery, retries, and backoff happen out-of-band. This is the fix for review finding 4 (non-blocking not designed for) and finding 5 (in-memory queue incompatible with per-event processes).

Functions to implement in `notifier.ps1`:
- `New-AiNotifyEnvelope` -- builds the JSON envelope matching the schema in the architecture doc section 4 (schemaVersion, vendor, toolOrSurface, workspaceName, workspacePathAlias, project, task, eventType, severity, safeSummary, timestamp, machineAlias, vscodeWindowId, terminalId, vendorSessionId, approvalRequestId, processExitCode, deduplicationKey, redactedMetadata).
- `Protect-AiNotifyPayload` (redaction) -- strips absolute paths, known secret patterns (tokens, API keys, webhook URLs themselves), and truncates `safeSummary` to ~200 chars. Write this with an explicit denylist of patterns and a test file (Phase 7) that proves each pattern is caught -- don't hand-wave this one, it's the actual security boundary.
- `Send-AiNotifyEvent` -- entry point described above.
- Secret read: `$env:DISCORD_WEBHOOK_URL` first; only add a Windows Credential Manager path later if a real need shows up (avoid the extra module dependency for the MVP -- env var is sufficient and is what the architecture calls "preferred").

**Acceptance criteria:** Calling `Send-AiNotifyEvent` from a throwaway PowerShell prompt with a fake envelope returns in well under 1 second and results in a message appearing in a test Discord channel within a few seconds via the detached dequeue process. Killing network access mid-call does not throw an error back to the caller.

---

## Phase 2 -- Mock webhook receiver (test harness, not shipped)

Stand up a minimal local HTTP listener (plain `System.Net.HttpListener` in PowerShell, no new dependency) that logs whatever JSON it receives. Use this for all testing in Phases 1, 3, 4 before pointing anything at a real Discord webhook. Put it at `~/.ai-notify/tools/mock-receiver.ps1`, not shipped as part of the notifier itself.

**Acceptance criteria:** `dequeue.ps1` pointed at the mock receiver's local URL successfully delivers a queued test event and the receiver logs the exact JSON body.

---

## Phase 3 -- Generic PowerShell process wrapper

`wrap.ps1`: wraps any command, times it, captures exit code, calls `Send-AiNotifyEvent` for `started` and `completed`/`failed`/`unexpected_exit`. This is the fallback path for every vendor that doesn't get a confirmed native hook in Phase 0.

```powershell
# wrap.ps1 usage: wrap.ps1 -Vendor <name> -- <command> <args...>
```

Keep this ASCII-only, ships as the safety net regardless of what Phase 0 finds.

**Acceptance criteria:** Running a known-good command (`exit 0`) and a known-fail command (`exit 1`) through `wrap.ps1` each produce exactly one Discord message with the correct `eventType` and `processExitCode`.

---

## Phase 4 -- Reusable VS Code Task template

Create `.vscode/tasks.json` fragment (project-level, portable, no secrets) that calls `wrap.ps1`. Place a copy in a `templates/` folder under `_audits` output or wherever the actual project scaffolding tool lives in this workspace -- confirm with the user which project this should ship as a template into before committing it broadly, since this workspace hosts multiple unrelated repos (ControlsBMW, finances, healthassistant, etc.) and the task template should not be dropped into all of them by default.

**Acceptance criteria:** Running the Task from the Command Palette in a real VS Code window produces a Discord message on completion/failure.

---

## Phase 5 -- First native adapter: Claude Code

Only proceed with hook event names confirmed in Phase 0's `verification-notes.md`. Wire hook entries in `.claude/settings.json` (or `~/.claude/settings.json` for user-level) for at minimum `SessionStart`, `Stop`, and whatever failure/permission-related event Phase 0 actually confirmed exists (do not assume `PermissionRequest`/`StopFailure` are real names -- use what Phase 0 found). Each hook command pipes stdin JSON into a small normalizer that maps Claude's payload shape into `New-AiNotifyEnvelope` and calls `Send-AiNotifyEvent`.

**Acceptance criteria:** Triggering `SessionStart` and `Stop` in a real Claude Code session produces correctly-shaped Discord messages with vendor=`claude` and a real session ID in `vendorSessionId`.

---

## Phase 6 -- Remaining adapters (Kimi, Grok native; Codex wrapper)

- Kimi and Grok: only build native hook adapters if Phase 0 confirmed the mechanism. If unconfirmed, use `wrap.ps1` (Phase 3) instead and note in `verification-notes.md` that the vendor is wrapper-only pending future verification.
- Codex: per the architecture, hooks are likely Windows-limited -- default to `wrap.ps1` unless Phase 0 found current docs saying otherwise.

**Acceptance criteria:** Every configured vendor produces a correctly-shaped envelope through exactly one capture path (never both a native hook and a wrapper for the same session -- pick one per vendor and document the choice).

---

## Phase 7 -- Reliability and redaction hardening

- Queue bounds: cap `queue/pending.jsonl` at N entries (architecture suggests 50-100); drop-oldest or coalesce on overflow -- implement and write a test that overflows it on purpose.
- Redaction tests: a Pester (or simple assert-script) test file that feeds known secret-shaped strings (a fake webhook URL, a fake API key, an absolute Windows path like `C:\Users\...\secret.txt`) through `Protect-AiNotifyPayload` and asserts they're stripped.
- Dedup test: two events with the same `deduplicationKey` within the dedup window should produce exactly one Discord message. Per the review, also add a short comment in the dedup code noting that the timestamp-bucket key is a safety net, not a guarantee, if both a native hook and a wrapper are accidentally left enabled for the same vendor/session -- the real prevention is "one capture path per vendor" from Phase 5/6.
- 429 handling test: point `dequeue.ps1` at a mock endpoint that returns 429 with a `Retry-After` header once, then succeeds; assert it retries and eventually delivers.
- Network-failure test: kill the mock receiver mid-queue and assert `dequeue.ps1` doesn't crash and leaves the entry queued for the next run.
- Concurrent-session test: fire two overlapping `wrap.ps1` runs and confirm each gets a distinct `deduplicationKey` / session identity and no message is dropped or merged incorrectly.

**Acceptance criteria:** every test above has an explicit pass/fail result recorded (a short `test-results.md` next to the scripts is enough -- no test framework needs to be introduced if a plain assert-and-exit-code script covers it).

---

## Phase 8 -- Operational rollout

- Write a short `README.md` in `~/.ai-notify/` covering setup (`$env:DISCORD_WEBHOOK_URL`), per-vendor enable/disable, and the "one capture path per vendor" rule.
- Confirm no secrets exist in any committed file (`.vscode/tasks.json`, `.claude/settings.json`, etc.) -- grep for `discord.com/api/webhooks` across anything that would get committed and fail the rollout if found.
- Run it across at least two real projects in this workspace for a day and confirm no duplicate or missing notifications before calling this done.

**Acceptance criteria:** stable under real use across concurrent terminals/sessions for the trial period, README exists, no secrets committed.

---

## Explicit gap this plan does not close

The architecture review noted the original doc never addressed Remote Development / WSL / SSH, even though the source prompt asked for it. This plan doesn't resolve that either -- it's scoped to the local Windows + VS Code integrated terminal case. Before rolling this out to any project that runs inside WSL or a Remote-SSH window, stop and re-check: file paths (`~/.ai-notify` resolves differently inside a WSL guest), whether `$env:DISCORD_WEBHOOK_URL` is visible inside that remote context, and whether hook scripts configured for a Windows path even fire correctly across the WSL boundary. Flag this to the user rather than guessing an approach.

## What to report back when this plan is executed
- Which vendors ended up with confirmed native hooks vs. wrapper-only, and why (link back to `verification-notes.md`).
- Any hook event names that turned out to differ from what the original architecture assumed.
- Test results from Phase 7.
- Anything in this plan that had to change once real docs/behavior didn't match what's written here -- don't silently patch around a wrong assumption, surface it.
