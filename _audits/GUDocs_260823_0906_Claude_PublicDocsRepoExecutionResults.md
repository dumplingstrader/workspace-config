# Public GU tools docs repo -- execution results

**Date:** 2026-08-23 09:06 PDT
**Prepared by:** Claude
**Executes:** `GUDocs_260823_0618_Claude_PublicDocsRepoImplementationPlan.md`
**Status:** Complete through Task I. Task H (ongoing sync process) is
documented, not built -- see below, nothing further to execute there.

## Repo

**https://github.com/dumplingstrader/gu-tools-docs** -- public,
CC-BY-4.0, description "Documentation for community-made Gods Unchained
tools. Unofficial, fan-made, not affiliated with Immutable or Gods
Unchained." Local working copy: `C:\_Development\gu-tools-docs\`.

Repo-local git identity was pinned to the GitHub noreply address
(`255458596+dumplingstrader@users.noreply.github.com`) rather than
inheriting the global config's real email, so the public commit history
doesn't carry a personal email address. This override is local to this
one repo only.

## Task A -- final triage table

Read fresh from each project's current README (or HANDOFF.md where no
README existed) on 2026-08-23, not from the plan's starting guesses.

**Include** (own tools, published):

| Project | Notes |
|---|---|
| DealsBot | Included as drafted -- read-only, no wallet code |
| GUOptimizer | Included, rewritten from scratch -- source README is a 514-line internal build/research log, not customer-facing |
| CardOwners | Included -- no real wallet address used in the doc's examples |
| DeckTracker | Included, rewritten -- source README is full of internal release/build process detail, trimmed for a public reader |
| GameModes | Included as drafted |
| Gameplay | Included as drafted |
| gods-unchained-api | Included as a link to Immutable's own upstream repo (`immutable/gods-unchained-api`) rather than re-vendoring their README into a second public repo |
| Coach | Included, concept-level only -- omitted phase/research/audit-history detail from the source README |

**Exclude** (nothing from these went into the public repo):

| Project | Reason |
|---|---|
| SellingBot | User declined at the Task B checkpoint -- wallet automation |
| Forging | User declined at the Task B checkpoint -- wallet automation |
| GUVrs | User call -- GitHub replication of a third party's project (Timothy Meadows / TimothyMeadows/GUvrs), not the user's own work |
| DirectMatch | User call -- same reasoning; vendored from `sewlie/directmatch` |
| Peakd | User call -- index of a third party's blog content, not a tool |
| OfficialBlog | User call -- index of official (Immutable) blog content, not a tool |
| Cardsunchained | Internal research notes evaluating a third-party site's features, not a tool of the user's |
| FasterForge | Contains a `decompiled/` directory of another company's compiled app (ilspycmd output) -- same IP/legal exposure class as SellingBot's `extracted_source/`, even though the original plan only named SellingBot explicitly |
| Music | Out of scope entirely -- personal archive of a third party's (CaptainAvocado's) copyrighted songs and lyric transcripts, not a GU tool |

## Task B -- checkpoint sign-off

User's explicit answer (2026-08-23 session): **no** to both SellingBot
and Forging. Per the plan's own rule for a "no," both were marked
Exclude outright -- no vaguer substitute description was drafted or
proposed.

In the same message the user also excluded GUVrs, Peakd, OfficialBlog,
and DirectMatch as "GitHub replications" of other people's projects --
folded into the Task A table above as explicit user calls rather than
starting guesses.

## Task C -- repo setup

Confirmed with the user before creation:

- Name: `dumplingstrader/gu-tools-docs`
- Description: "Documentation for community-made Gods Unchained tools.
  Unofficial, fan-made, not affiliated with Immutable or Gods
  Unchained."
- License: CC-BY-4.0 (full official legal text from
  `creativecommons.org/licenses/by/4.0/legalcode.txt`)
- Sequencing: create with skeleton (LICENSE, minimal disclaimer README,
  minimal `.gitignore`) first, add the project index once Task E
  content existed

Created via `gh repo create dumplingstrader/gu-tools-docs --public
--source=. --push`, first commit `e6ddfba`.

## Task D -- redaction checklist

Run twice: once against the 3 skeleton files before the first commit,
once against all 9 files (README + 8 doc pages) before the Task G push.
Both runs were clean. Checks run (grep, real output, not just
asserted):

```
grep -rniE "levia" ...                                    -> (none found)
grep -rniE "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}" ...     -> (none found)
grep -rniE "0x[a-fA-F0-9]{8,}" ...                          -> (none found)
grep -rniE "(api[_-]?key|secret|token|bearer)\s*[:=]\s*[A-Za-z0-9]{10,}" ... -> (none found)
grep -rniE "extracted_source|decompil|sellingbot|fasterforge|ilspycmd" ...   -> (none found)
grep -rniE "HANDOFF\.md|_TODO\.md|audits/" ...              -> (none found)
grep -rniE "[A-Za-z]:\\\\|/c/_Development|E:\\\\_Development|%APPDATA%|%LOCALAPPDATA%" ... -> (none found)
grep -rniE "dumplingstrader|tchiutrading" ...               -> (none found)
grep -rniE "PRIVATE_KEY|WALLET_ADDRESS|\.env" ...           -> (none found)
```

Also caught outside the file-content checklist: the local git commit
identity itself (see "Repo" above, real-email fix).

## Task E -- drafted content

8 doc pages written under `docs/` in `dumplingstrader/gu-tools-docs`,
each an original rewrite (not copy-pasted) covering what the tool does,
why someone would want it, and how it works at a level a reader with no
access to the private repo can follow. Source code was never included
or linked -- the private `gaming` repo stays private, so these pages are
descriptive/showcase documentation, not install instructions (no
`git clone` / `npm install` / `pip install` steps, since the reader has
no way to obtain the source).

## Task F -- publishing approach

Plain public GitHub repo, browsable natively as markdown. No GitHub
Pages, no static-site generator -- per the plan, that would need its own
separate sign-off and wasn't requested.

## Task G -- final push sign-off

Full file list and one-line summary per file shown to the user before
the push (see chat transcript, same session); user replied "commit and
push." Files pushed exactly matched the Task A Include list -- nothing
from an Excluded project was in the diff. Commit `316f282`, pushed to
`main`.

## Task H -- ongoing sync process (documented, not automated)

When a project's real README changes meaningfully: manually re-run Task
D (redaction) and Task E (drafting) for that project only, then commit
and push just that update. No CI or automation publishes from the
private repo to the public one -- that would need its own separate
sign-off per the plan's ground rules, and hasn't been requested.

## Task I -- index README

Added `C:\_Development\_audits\README.md`, documenting the
`GUDocs_YYMMDD_HHMM_Author_Topic.md` convention and indexing both
`GUDocs_*` documents (the implementation plan and this results doc).
Existing untagged documents in the folder were left untouched.
