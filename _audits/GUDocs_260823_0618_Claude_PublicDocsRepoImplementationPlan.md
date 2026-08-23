# Public-facing Gods Unchained tools documentation repo -- implementation plan

**Date:** 2026-08-23 06:18 PDT
**Prepared by:** Claude
**For:** Claude (a future execution session -- this plan is not a Codex
handoff; there is no separate "Codex executes, Claude reviews" split here)
**Scope:** Create a new, separate, public GitHub repo containing curated
documentation only. Does **not** modify `github.com/dumplingstrader/gaming`
(private as of 2026-08-23, see `Gaming/CLAUDE.md`), does not touch any
wallet or `.env` file, does not publish source code, and does not train or
run any bot.
**Status:** Plan for review -- **not yet authorized**. Two explicit
go/no-go checkpoints (Task B, Task G) require the user's sign-off before
proceeding past them; do not skip either one because the rest of the plan
went smoothly.

## 0. Why / context

`github.com/dumplingstrader/gaming` went private on 2026-08-23 specifically
so a docs-vs-code split could happen on a calm timeline instead of under
exposure pressure (see that session's decision). Git/GitHub have no
path-level or file-level visibility control -- a repo is all-or-nothing, and
anyone with read access can clone everything in it. The only way to let
people read documentation without being able to clone code is two separate
repos. This plan is the concrete execution of that second half of the
decision: build the public one.

Naming convention for this document and any future document produced by
this initiative: `GUDocs_YYMMDD_HHMM_<Author>_<Topic>.md`, the same
timestamp-tagged pattern developed in `GodsUnchained/Coach/audits/`
(`Coach_YYMMDD_HHMM_Author_Topic.md` and its
`audits/prompts/codex_YYMMDD_HHMM_<topic>_kickoff_prompt.md` sibling), with
`GUDocs` standing in for `Coach` since this initiative isn't scoped to a
single existing project. `E:\_Development\_audits\` does not yet have an
index README distinguishing this convention from the untagged documents
already in it (`ai-cli-discord-*`, `workspace-ai-automation-*`) -- Task I
below covers adding one.

## 1. Ground rules (must-nots) -- read before doing anything

- Never copy a source code file into the new repo. Prose documentation
  only.
- Never include SellingBot's `extracted_source/` or any detail of its
  decompilation -- see Task B, this needs its own explicit sign-off, not an
  inference from this plan.
- Never include real wallet addresses beyond "uses a burner wallet," real
  account/alt-account labels, API keys, tokens, or `.env` contents/examples
  with real-looking values.
- Never include the real local Windows username or any absolute local
  path in published content.
- Never copy `audits/`, `HANDOFF.md`, or `_TODO.md` content wholesale --
  those are internal decision records (mistakes, wrong hypotheses, private
  reasoning), not customer-facing material.
- Never add a heavyweight publishing dependency (a static-site generator,
  GitHub Pages build pipeline, etc.) without separate sign-off, consistent
  with this workspace's existing convention of gating new dependencies.
- Never make the new repo's first commit before Task D's redaction
  checklist has been run against every drafted file, with real command
  output shown, not just asserted.

## 2. Task A -- Inventory and triage

Read the **current** `README.md` of every project below fresh (not from
memory or from this plan's starting guesses) and classify each as
**Include** / **Partial** / **Exclude**, with a one-line reason. Produce
this as an actual table in the output document (Section 10).

Current `GodsUnchained/` subprojects (confirmed via directory listing,
2026-08-23): `DealsBot`, `SellingBot`, `Forging`, `GUOptimizer`, `GUVrs`,
`CardOwners`, `DeckTracker`, `Coach`, `GameModes`, `Gameplay`, `DirectMatch`,
`Cardsunchained`, `FasterForge`, `Peakd`, `OfficialBlog`,
`gods-unchained-api`, `Music`.

Starting recommendation, to confirm or override during execution --
**do not treat this list as a substitute for actually reading each
README**:

| Project | Starting call | Reason |
|---|---|---|
| DealsBot | Include | Read-only market scanner, no wallet, genuinely useful to describe to other players |
| GUOptimizer | Include | Personal stats + community meta dashboard, no wallet |
| GUVrs | Include | Third-party MIT overlay tool; already open-source elsewhere |
| DeckTracker | Include | Companion overlay + deck renderer, no wallet |
| GameModes | Include | Generated reference data, low sensitivity |
| Gameplay | Include | Already reference documentation, low risk |
| gods-unchained-api | Include | Vendored notes about a public official API |
| Coach | Partial | Describe the advisory-overlay concept; omit vision/detection implementation detail and all audit history |
| CardOwners | Partial | Describe the tool; never publish a real wallet address it has looked up |
| Forging | Partial, **checkpoint** | Forge ratios (2 Plain->Meteorite, 5/tier) are public game mechanics and fine to explain; the automation internals and wallet handling are not -- see Task B |
| SellingBot | **Exclude by default, checkpoint** | Live wallet automation decompiled from a third-party `.exe` -- see Task B before writing anything |
| Peakd, OfficialBlog | Ask before including | These are lead-indexes under a specific citation model (brief quotes, no wholesale copies); confirm that model still holds if republished elsewhere |
| DirectMatch, Cardsunchained, FasterForge | Exclude | Research/comparison folders, not user-facing products |
| Music | Unclear from name alone | Read it fresh, do not assume purpose |

## 3. Task B -- Explicit checkpoint: SellingBot and Forging

**STOP.** Before drafting any public content for SellingBot or Forging,
show the user the exact proposed text (even two sentences) and get an
explicit yes. This is a harder gate than the others for two distinct
reasons:

1. SellingBot's `extracted_source/` is decompiled from a third-party
   executable. Describing or redistributing decompiled code in a public
   venue is a real legal/IP exposure, separate from and in addition to "I
   don't want my own code cloned."
2. Both tools operate a live wallet with a real private key. Even a
   high-level description of setup steps could hand a bad actor a roadmap
   to a mistake that costs the user real money.

If the user says no to either, mark it **Exclude** in the Task A table and
move on -- do not substitute a vaguer description as a compromise without
asking first.

## 4. Task C -- New repo setup

- Propose a repo name that does not read as official/affiliated --
  recommend `dumplingstrader/gu-tools-docs` (confirm with the user; avoid
  a name implying endorsement by Immutable or Gods Unchained).
- `gh repo create dumplingstrader/gu-tools-docs --public --description "..."`
- Add a `LICENSE`. Recommend CC-BY-4.0 for documentation content (there is
  no code in this repo, so a code license like MIT/Apache is the wrong
  choice) -- confirm with the user, this is their call, not a default to
  apply silently.
- Root `README.md`: what this repo is, an index linking to each included
  project's doc page, and an explicit disclaimer that this is fan-made,
  unofficial, and not affiliated with Immutable or Gods Unchained.
- `.gitignore`: minimal -- this is a docs-only repo, there should be
  nothing to ignore beyond OS/editor cruft.

## 5. Task D -- Redaction checklist

Run every item below against **every drafted file** before the first
commit. Show the actual grep command and its (expected-empty) output in the
output document -- "I checked" is not sufficient, per this workspace's own
verification-first convention.

- [ ] no real local Windows username anywhere
- [ ] no real email addresses -- cross-check against the
      `github-commit-identity-privacy` memory
- [ ] no `0x`-prefixed wallet address strings
- [ ] no API keys or tokens (grep for common key-shaped patterns)
- [ ] no reference to `extracted_source`, decompilation, or SellingBot
      internals beyond exactly what Task B explicitly approved
- [ ] no copied `audits/`, `HANDOFF.md`, or `_TODO.md` content
- [ ] no absolute local file paths (`E:\_Development\...` or similar)
- [ ] no real account/alt-account labels
- [ ] no aspirational/unreleased claims presented as shipped -- cross-check
      each drafted page against that project's actual current README, not
      memory of an earlier session

## 6. Task E -- Draft content

For each Include/Partial project from the confirmed Task A table: write a
docs page (or root-README section) covering what it does, why someone would
want it, and general usage -- written for a reader who has never seen the
private repo. Do not copy-paste the internal README verbatim; internal
READMEs assume repo-internal context (sibling project paths, internal
jargon, references to other tools) that means nothing to an external
reader and may itself violate Task D's checklist.

## 7. Task F -- Publishing approach

Recommend: a plain public repo with clean, well-organized markdown,
browsable natively on GitHub. **Do not** set up GitHub Pages or a
static-site generator in this pass -- that is an added-dependency decision
needing its own sign-off, and a plain repo already satisfies the actual
requirement ("customers can read this; they can't clone the code repo").
Revisit only if the user later wants a nicer reading experience.

## 8. Task G -- Final review checkpoint before first push

**STOP.** Before the first `git push`, re-run Task D's full checklist
against the complete diff one more time, then show the user the complete
file list plus a one-line summary of what each file contains. Get an
explicit go-ahead. Publishing is easy to do and hard to fully undo (forks,
caches, search-engine indexing) -- this is the same "confirm before
outward-facing action" rule that governed making the private-repo decision
itself, applied to its public counterpart.

## 9. Task H -- Ongoing sync process (define, do not automate yet)

Document a repeatable manual process for future updates: whenever a
project's real README changes meaningfully, re-run Task D (redaction) and
Task E (drafting) for that project only, then push an update. Do **not**
set up CI/automation that auto-publishes from the private repo without a
separate, explicit sign-off -- an automated pipeline that could accidentally
publish something unredacted is a materially bigger risk than a manual
step, and this workspace's convention is to earn automation after the
manual process is proven, not before.

## 10. Output

Record execution results in a new document in this same folder, named
`GUDocs_YYMMDD_HHMM_Claude_<Topic>.md`. Include: the completed Task A
triage table (as actually confirmed, not the starting guesses above), the
Task B sign-off record, the new repo's URL, the Task D checklist results
with real command output, and the Task G sign-off record.

## 11. Task I -- Add an index note to this folder

`E:\_Development\_audits\` currently has no `README.md` distinguishing this
initiative's timestamp-tagged documents (`GUDocs_*`) from the existing
untagged ones (`ai-cli-discord-*`, `workspace-ai-automation-*`). Add a short
`README.md` documenting the `GUDocs_YYMMDD_HHMM_Author_Topic.md` convention
and listing documents under it, mirroring the pattern (not the full
content) of `GodsUnchained/Coach/audits/prompts/README.md`. Do not rename or
restructure the existing untagged documents -- they follow the workspace's
general `lowercase-hyphens.md` convention and are out of this plan's scope.

## 12. Definition of done for this plan's execution

- [ ] Task A table reflects a fresh read of every project's current
      README, not this plan's starting guesses
- [ ] Task B: explicit user sign-off captured in the output document for
      SellingBot and Forging content (or their exclusion)
- [ ] New repo exists, public, named per Task C, with LICENSE and
      disclaimer
- [ ] Every drafted file passes every Task D checklist item, with actual
      grep output shown
- [ ] Task G: explicit user sign-off on the full file list recorded before
      first push
- [ ] Output document written per Section 10
- [ ] Section 11's index README added
