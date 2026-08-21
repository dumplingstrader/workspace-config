# Feedback: Discord Integration Tooling for Kimi Code CLI

**Reviewed:** `ai-cli-discord-integration-architecture-review.md` (reviewer of `ai-cli-discord-integration-architecture.md`)  
**Date:** 2026-08-21  
**Scope:** Whether the proposed architecture can be used to add Discord notifications to Kimi Code CLI

---

## Bottom line

The *design pattern* would work for Kimi Code CLI if the claimed hook surface exists as described, but **the architecture document should not be treated as a verified build spec for Kimi Code CLI until its Kimi-specific hook claims are independently confirmed**. The safest path is to start with the generic PowerShell / VS Code Task wrapper, then add native Kimi hooks only after verifying the real hook event list and config syntax.

---

## What the architecture proposes for Kimi

The architecture doc claims Kimi Code CLI supports:

- A `[[hooks]]` array in `config.toml`
- Events: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `StopFailure`, `SessionStart/End`, `Subagent*`, `Pre/PostCompact`, `Notification`
- Session context available in hook payloads
- Membership covers CLI/extension; API-key mode is separately billed
- Native hooks as the recommended integration tier with "High" confidence

These claims mirror the Claude Code hook taxonomy almost exactly, which is the primary reason the review flags them as potentially generalized rather than independently verified.

---

## What this means for a Kimi Code CLI integration

### 1. Native hook path: build only after verification

If Kimi Code CLI does expose a hook system similar to the one described, the architecture's adapter pattern fits well:

- PowerShell scripts are a natural hook target on Windows.
- A thin normalizer can map Kimi hook JSON into the shared envelope.
- The `DISCORD_WEBHOOK_URL` secret-handling pattern works with user-level environment variables or the Windows Credential Manager.

However, I cannot confirm from the architecture document alone that the specific event names (`PostToolUseFailure`, `StopFailure`, `Pre/PostCompact`, etc.) or the `[[hooks]]` TOML syntax are correct. Building the native adapter against unverified event names risks a broken integration that fails silently or produces malformed notifications.

**Recommendation:** Treat the native Kimi hook path as the *target state*, not the starting state. Before wiring Stage 6 of the blueprint to Kimi native hooks, open the current Kimi Code docs and confirm:

1. The exact hook event names and payload schema.
2. The config file name, path, and syntax (is it really `[[hooks]]` in `config.toml`, or a different mechanism?).
3. Whether hooks are supported on Windows and in the VS Code extension host.
4. Whether hooks run synchronously and what failure semantics apply.

### 2. Generic wrapper path: works regardless of hook support

The architecture's fallback — a VS Code Task wrapper or PowerShell process wrapper — is the safest near-term option because it depends only on:

- VS Code Tasks (stable, well-documented)
- PowerShell 5.1/7 (already the target environment)
- Process exit codes

This path would work for Kimi Code CLI today even if none of the claimed native hooks exist. It provides:

- Start / complete / failed events
- Workspace and project labels
- Redaction and Discord delivery
- No dependency on Kimi-specific internals

The trade-off is less granular lifecycle visibility (no per-tool-call events, no permission notifications), but that matches the stated MVP boundary.

**Recommendation:** Implement Stage 1–4 of the blueprint (shared notifier + Task wrapper) before any vendor-specific native adapter. Validate end-to-end delivery with the wrapper, then decide whether native hooks add enough value to justify verification work.

### 3. The "non-blocking" requirement needs a real handoff

The architecture repeatedly says the notifier must be "non-blocking," but the example wrapper and sequence diagram show synchronous execution. Kimi Code CLI hook processes, if they run like Claude Code hooks, are invoked synchronously and the session waits for them to exit. A notifier that does retry/backoff inline would directly violate the non-blocking requirement.

**Recommendation:** Implement the file-backed queue + detached dequeue process described in the review's Finding 4 before claiming the integration is non-blocking. This is especially important if Kimi hooks are synchronous.

### 4. WSL/SSH gap is relevant for Kimi users on Windows

The review notes that the architecture silently drops the prompt's WSL/SSH/Remote Development requirement. Many Kimi Code CLI users on Windows run the CLI inside WSL via VS Code Remote. In that setup:

- Hook scripts may need to run in the WSL guest but post to Discord through Windows-side network.
- `DISCORD_WEBHOOK_URL` set in the Windows host profile is not automatically visible inside WSL.
- File paths for queue/logs differ between host and guest.

**Recommendation:** Add an explicit WSL/Remote section before implementation. Decide whether the notifier runs on the Windows host, inside WSL, or in both, and how secrets and queue files cross the boundary.

### 5. API billing boundary is correctly handled

The architecture's subscription-vs-API separation is sound for Kimi Code CLI: if the integration uses only local hooks or local wrapper scripts, it does not consume Kimi API credits. This is a useful guardrail and should be preserved.

---

## Suggested corrected approach for Kimi Code CLI

1. **Phase 0 (verification):** Confirm Kimi Code CLI hook capabilities from official docs. If confirmation fails, mark native hooks as "not verified" and keep the wrapper path as primary.
2. **Phase 1 (MVP):** Build the shared PowerShell notifier and a VS Code Task wrapper. This works for Kimi Code CLI immediately, with no vendor-specific assumptions.
3. **Phase 2 (native adapter, optional):** Add the Kimi native hook adapter only after verifying event names and config syntax.
4. **Phase 3 (hardening):** Fix the synchronous-queue issue, add WSL/Remote handling, and complete the redaction/retry test checklist.

---

## Verdict

The tooling *can* work for Kimi Code CLI, but the architecture document's Kimi-specific claims should not be trusted as-is. Start with the generic wrapper, verify the hook surface, then specialize. This keeps the project honest about what is known and avoids building against a possibly hallucinated vendor contract.
