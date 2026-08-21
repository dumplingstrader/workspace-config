# Review: AI CLI Discord Integration Architecture

**Reviewed file:** `ai-cli-discord-integration-architecture.md`
**Source prompt:** `ai-cli-discord-architecture-prompt.md` (sent to Grok)
**Review date:** 2026-08-21
**Reviewer method:** Read against the source prompt's own requirements, cross-checked against reviewer's knowledge of Claude Code hooks; no live fetch of the cited URLs was performed (see Finding 1).

## Summary

The document is well-organized and internally consistent, and it does the right things structurally (separates facts/design/unknowns, keeps API billing separate from subscription-authenticated CLI use, labels illustrative code). The biggest problem isn't structure -- it's that the document's central promise ("verified against official sources," "never guess," cite direct links) isn't actually demonstrated by what's on the page. A few requirements from the prompt were also dropped silently instead of being marked "not verified." Fix the verification gap before treating any row in the capability matrix as ground truth, especially for Kimi and Grok.

## Findings

### 1. (High) "Verified" claims aren't actually verifiable from what's in the document
The doc states "Verified against official sources as of August 2026" and the prompt demanded "Cite time-sensitive claims with direct official links... Never guess." What's actually cited is mostly bare domains or doc-section roots (`code.claude.com/docs/en/hooks`, `support.claude.com`, `kimi.com/code/docs`, `x.ai/docs/build/features/hooks`) with no deep link, no page title, no accessed-date, and no quoted snippet. There's no way to tell whether these pages exist as described or were pattern-completed.

The strongest tell: **Kimi Code and Grok Build CLI are described with an almost identical hook taxonomy to Claude Code** -- `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart/End`, `Notification`, `Subagent*`, `Pre/PostCompact` -- right down to Grok's hooks being called out as "Claude-compatible JSON hooks." Three independent vendors converging on the exact same event names and lifecycle shape is the signature of an LLM generalizing from the best-known example (Claude Code) rather than three separately confirmed facts. Kimi's `[[hooks]]` TOML-array syntax also mirrors Codex's `config.toml` mechanism suspiciously closely.

**Action:** Before building the Kimi or Grok native adapters (Blueprint stage 6), independently confirm the hook event names, config file location, and config syntax against the actual current docs. Don't treat the "High confidence" rating on those two matrix rows at face value -- the sourcing behind it isn't shown.

### 2. (High) Two explicitly requested items are silently missing, not marked "not verified"
The source prompt has a dedicated checklist item: *"Address... Remote Development, WSL, and SSH implications"* under VS Code integration requirements. The delivered document never mentions WSL, SSH, or Remote Development anywhere -- not even as an "unknown." Given the target environment is Windows + VS Code, and Remote-WSL is an extremely common setup for CLI-first dev, this is a real gap: hook scripts, `DISCORD_WEBHOOK_URL`, and file paths all behave differently when the integrated terminal is actually running inside a WSL guest vs. the Windows host.

Separately, the prompt asked for capability-matrix rows covering each vendor's "CLI, VS Code extension, **and API/SDK** surface." Only xAI got an API/SDK row (`Grok API / SDK`). Anthropic, OpenAI, and Moonshot/Kimi have no corresponding API/SDK row, even though the doc's own "Subscription boundary notes" talk about API billing for all four vendors. This is an inconsistency between what the matrix promises in its own column spec and what it delivers.

**Action:** Either add the missing rows/section, or add them to the "Unknowns / not verified" list at the bottom so the gap is visible instead of silent.

### 3. (Medium) Claude Code hook event names look partially invented
Rows for Claude Code, Kimi, and Grok all list `PostToolUseFailure`, `StopFailure`, and (for Claude) `PermissionRequest` as lifecycle hook events, alongside `Subagent*` and `Task*` wildcard families. From what I know of Claude Code's actual hook set (`PreToolUse`, `PostToolUse`, `Notification`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `SessionStart`, `SessionEnd`), I don't believe `PostToolUseFailure`, `StopFailure`, or a standalone `PermissionRequest` event exist as distinct hook names -- permission decisions are typically surfaced through the `PreToolUse` hook's output or the `Notification` hook, not a separate event type. This could be wrong (docs move), but it's exactly the kind of claim the prompt asked to be verified with a direct link rather than asserted, and no link resolves specifically to a hook-events list.

**Action:** Verify the current hook event list at the actual Claude Code hooks doc page before wiring stage 5 of the blueprint to these specific event names.

### 4. (Medium) "Non-blocking" isn't actually designed for
The doc asserts the notifier is "non-blocking" and must "never block the AI session" (component description, reliability section, per-vendor failure-behavior notes). But the example wrapper code (`Send-AiNotifyEvent`, the wrapper sketch) runs inline, and hooks in these CLIs execute synchronously -- the tool call or session waits for the hook process to exit. If `Send-AiNotifyEvent` does bounded retry with exponential backoff and jitter *inside that same hook invocation*, a Discord outage or a 429 would add real, visible latency to the user's AI session, which directly contradicts the non-blocking requirement.

**Action:** The design needs an explicit detachment step -- e.g., the hook script does the minimum synchronous work (write to the file-backed queue) and returns immediately, while a separate detached process (`Start-Process -WindowStyle Hidden` or a scheduled dequeue) does the actual POST/retry/backoff. As written, "queue" and "notifier" are drawn as sequential steps in the same flow (see the sequence diagram: `N->>Q: Enqueue` then `Q->>P: Dequeue` then `P->>D: POST`), which implies one continuous synchronous call chain rather than a handoff between processes.

### 5. (Medium) In-memory queue is incompatible with the per-event process model
Component description: "Bounded local queue -- In-memory or simple file-backed queue." But every capture path (native hook, Task wrapper, process wrapper) invokes a fresh, short-lived PowerShell process per event. An in-memory queue dies with that process; it cannot accumulate anything across events. The "in-memory" option in the component description is therefore not viable for this architecture and should be dropped rather than offered as a real alternative -- only the file-backed queue actually works given how hooks/wrappers are invoked.

### 6. (Low) Unicode/em-dash usage inside a literal PowerShell code block
This workspace's `CLAUDE.md` has a standing correction: "Never use Unicode characters... in PowerShell scripts or any script that may be invoked through bash... encoding mangles them, causing function definitions to break." Line ~310 of the reviewed doc has this inside a ```powershell fence:

```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/…"
```

That's an ellipsis character (`…`) sitting inside a quoted string in an actual PowerShell code block, not just prose. It's clearly meant as a placeholder, but if anyone copy-pastes the snippet as a starting point (likely, since it's presented as the canonical secret-config example), it becomes exactly the kind of encoding hazard the workspace convention exists to prevent. Em-dashes and an ellipsis also appear in prose elsewhere in the doc (lines ~239, 263, 303, 304, 349) -- the workspace's Tony's Writing Voice rules apply to "documentation," which this is.

**Fix:** replace `…` with `...` or `<webhook-id>/<webhook-token>` style placeholders throughout, especially inside code fences.

### 7. (Low) Executive Recommendation likely runs over the requested 200-word cap
The prompt caps section 1 at 200 words. A rough count of the delivered "1. Executive Recommendation" section puts it modestly over that limit. Not a correctness issue, just a spec-compliance nit worth a trim pass.

### 8. (Low) Deduplication key may not actually dedupe the scenario it's meant for
Dedup key = `vendor + session-id (or process-id) + event-type + timestamp-bucket`. The doc's own stated failure mode is "both a native hook and a Task wrapper fire for the same underlying event." But a native hook fires at the moment of the lifecycle event, while a Task-wrapper/process-wrapper detects completion via exit code some time later -- the two are unlikely to land in the same timestamp bucket unless the bucket is quite wide (which then risks coalescing genuinely distinct rapid events). The doc's real mitigation is procedural ("prefer a single capture path per vendor/session," section 3), which is fine, but the dedup key is then mostly a safety net that won't reliably catch the one scenario it's framed around if a user leaves both paths enabled. Worth a one-line caveat rather than presenting the key as sufficient on its own.

## What's solid
- Clean separation of subscription-covered CLI/extension usage vs. separately billed API usage, applied consistently across the vendor sections and the "no-go conditions" in section 9.
- The refusal to invent two-way control ("mandatory safeguards," explicit no-go conditions, "treat terminal keystroke injection as an unsupported last resort") matches the prompt's caution requirements well.
- The phased backlog and stop/justify conditions in section 10 are concrete and actionable, not just generic "iterate later" language.
- Facts/design-choices/unknowns separation at the end (section, "Separation of concerns") is a good practice and should be kept -- it just needs to actually list the gaps above (WSL/SSH, hook-name confidence) rather than only the three items currently there.

## Recommended next step
Before using this as a build spec: re-run verification specifically on (a) the Kimi Code and Grok Build CLI hook claims, and (b) the exact Claude Code hook event list, using direct doc links you can open and quote from. Everything else in the architecture (component boundaries, blueprint stages, redaction/testing checklist) is reasonable and doesn't depend on those facts being wrong.
