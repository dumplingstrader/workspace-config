# Portfolio Audit and Roadmap -- E:\_Development

**Date:** 2026-07-06
**Method:** Cross-portfolio audit via Fable 5, read-only, evidence-based (git history,
HANDOFF/CLAUDE.md/_TODO.md files across ControlsBMW, controls-docs, finances,
healthassistant, Documentation, openclaw-sandbox, resource-tools, and Gaming/GodsUnchained's
~15 sub-projects). This is a one-time strategic snapshot, not a living document -- update or
supersede it rather than editing history into it.

---

## The two money questions, answered

**finances/ is built-and-abandoned, and its `sell` command would give a corrupted answer
right now.** Prices haven't moved since 2026-01-23 (5.5 months) on a metals-heavy portfolio.
Worse: three silver bags carry $0 cost basis (a known blocker in `finances/HANDOFF.md`) --
meaning ~$66K of holdings show as 100% "profit" and float to the top of any profit-ranked
liquidation list for a data-hygiene reason, not a real market signal. Note: `finances/CLAUDE.md`
says current value ~$393K while `finances/HANDOFF.md` (same "last updated" date) says ~$376K --
the two files disagree with each other, itself evidence the tracker has gone stale.

**Gaming is unmeasured tool-building with real money attached, not a measured trading
operation.** There is no P&L or trade ledger anywhere in the repo. SellingBot runs live
against a real wallet and its own HANDOFF documents five pricing-risk gaps in priority
order, including one confirmed-active bug (Binance ETH/USD is geo-blocked on this machine,
HTTP 451, so USDC conversion likely hasn't worked here) and one that could mis-list a 1+ ETH
collectible as an ordinary card. Meanwhile, of the last 90 days' ~360 Gaming commits, roughly
195 went to play-side analytics and third-party tool autopsies (GUOptimizer's deck-meta
dashboard, GUVrs's security review, FasterForge's decompilation whose own HANDOFF says
"nothing here is worth porting forward," DirectMatch's review) versus ~105 across the three
tools that actually touch money -- and even DealsBot's flagged deals require a human to
manually act, since the buy-side was never built.

---

## Ranked moves (highest expected return first)

### 1. Fix SellingBot's five documented pricing gaps

**Why:** live wallet, live listings, one confirmed-active bug, one catastrophic-tail risk,
and the fix list is already written and prioritized -- three of the five fixes are already
proven working in DealsBot.

**Steps:** work `SellingBot/HANDOFF.md`'s "Next steps" in its own order --
1. Fold `ethereum` into the existing CoinGecko call to fix the Binance geo-block
2. Capture and exclude `Frame`-tagged variant tokens from `buildFloorCache`
3. Add a `MIN_FLOOR_SAMPLE_SIZE` gate
4. Add a sample-size gate to `fetch30DayAvg`
5. (Optional, biggest lift) port `tokentrove_sales.js` as a primary sales source

**Done looks like:** all five closed, `ethUsd` resolves on this machine, a live pricing cycle
logged with no Frame-tagged token priced.

**Tell a weaker model exactly:** "Open `E:\_Development\Gaming\GodsUnchained\SellingBot\HANDOFF.md`,
section 'Next steps.' Implement items 1-4 exactly as described, copying the working logic from
DealsBot's `price_reference.js` and `tokentrove_sales.js`. Do not change any other pricing
logic. Verify item 5 separately before merging."

### 2. Make finances decision-ready, then actually run the sell analysis

**Why:** the ~$200K+ unrealized gain here dwarfs anything Gaming will produce, and the tool
exists specifically to time liquidation.

**Steps:** update all 66 prices from current PCGS/NGC guide values; flag (don't rank) the
three $0-basis silver bags instead of letting them read as 100% profit; regenerate the
report; run `sell` and record the actual decision in HANDOFF.md.

**Done looks like:** a report dated July 2026, zero unflagged $0-basis rows, a written
sell/hold decision.

**Tell a weaker model exactly:** "Update `data/portfolio.db` prices for all 66 items from
current price-guide values. For the three $0-cost silver bags, set a `basis_unknown` flag
and have `sell` print a warning line for those instead of ranking them by profit. Regenerate
the report. Do not add features."

### 3. Build the missing P&L number for Gaming before building anything else there

**Why:** SellingBot has been selling real cards and Forging burning real GODS/gas with zero
measurement, so whether Gaming deserves its current #1 share of side-project hours is
currently unanswerable.

**Steps:** one script pulling the wallet's filled sells/buys plus forge costs for the
trailing 90 days, converted to USD, printed as a single net-profit number.

**Done looks like:** a monthly USD figure appended to Gaming's HANDOFF.md. If it's under
roughly $200/month, that should reset the whole time budget for this project.

**Tell a weaker model exactly:** "Write `Gaming/GodsUnchained/pnl_report.py`: fetch FILLED
orders where seller or buyer is the wallet address for the last 90 days, convert to USD at
sale-date rates, subtract gas and GODS forge fees, print totals. Read-only, no wallet key
needed."

### 4. Twenty-minute healthassistant revival before the Jul 8 PCP visit

**Why:** this didn't stabilize, it stalled mid-migration. The alembic migration adding
urticaria-tracking fields was never applied, and the explicit next step -- weekly Dupixent
response tracking to measure a just-started biologic -- has no evidence of happening since
April. Both the Jul 8, 2026 PCP visit and the Jul 27, 2026 allergy follow-up are exactly
when that response data would matter.

**Done looks like:** migration applied, app verified running, 2-3 symptom entries logged
(backfilled if needed) before Jul 27.

**Tell a weaker model exactly:** "cd backend; alembic upgrade head; start backend and
frontend; verify `/symptoms/uas7` responds. Then stop -- no feature work."

### 5. ControlsBMW: scrub, commit, and make an explicit go/park call

**Why:** 140 commits of sunk effort, dormant 4.5 months, revived with uncommitted work
sitting in the tree -- and real incident numbers/dates are still sitting in backlog
filenames, which threatens both anonymity and the employer relationship they're meant to
protect.

**Done looks like:** no identifying strings anywhere in the repo, clean `git status`, and one
recorded line in HANDOFF.md: a real posting cadence, or "parked until [date]."

### 6. Documentation: execute the existing `.tasks/todo.md` punch list and finish the AI case-study standard

**Why:** this is the only compounding career asset in the whole portfolio (employer-visible,
quantified impact), it's the most actively worked repo right now, and the fix list already
exists.

**Done looks like:** mojibake fixed in the canonical instruction files, the dangling
archived-file reference removed, every `Example Case N` conforms to the required structure.

### 7. Fix the workspace map itself

**Why:** root `CLAUDE.md` calls Gaming "reference tools" when it's a live wallet-key trading
operation -- and that index is what loads first into every session. Root `HANDOFF.md` is
5 months stale despite its own "update before closing" rule.

**Done looks like:** the index label corrected; root HANDOFF.md either refreshed or that
rule demoted to per-project only, since a rule ignored for 5 months is worse than no rule.

---

## The three things to stop doing

### 1. Stop the play-side analytics and third-party tool autopsies in Gaming until the money side is safe and measured

This isn't low-quality tinkering -- GUOptimizer in particular is genuinely rigorous work
(cross-validated against a live third-party site, its own scheduled refresh task). The
problem is aim, not craft: roughly 195 of the last 360 Gaming commits went to a deck-meta
dashboard, a decompiled tool its own review called not worth porting, and two security
reviews of read-only stat viewers -- while the one tool that auto-prices real assets carried
five known, written-down, unfixed defects the whole time. The interesting problems got the
hours; the boring risk-reduction on live money didn't. Freeze GUOptimizer where it is and
call the third-party review program complete.

### 2. Stop carrying dormant AI meta-infrastructure as if it were active

openclaw-sandbox and resource-tools weren't built gradually -- openclaw-sandbox was built in
a single day and never touched again. The real cost isn't the maintenance burden, it's
structural: a four-part stack (ControlsBMW -> controls-docs -> openclaw-sandbox ->
resource-tools) exists to serve a persona that has published nothing and gone dormant since
the day its own infrastructure finished. A "94.9% token savings" pipeline with zero
throughput is optimizing nothing. Leave all three support repos alone until ControlsBMW has
an actual posting cadence; if move 5 lands on "park," archive all four together at once.

### 3. Stop declaring projects done at code-complete and skipping the one operational step that produces the actual return

This is the portfolio's real pattern: finances stalled exactly when the remaining work
became "manually update 66 prices"; healthassistant stalled exactly at "run one migration
and log symptoms weekly"; ControlsBMW built the entire backlog-to-post pipeline and stalled
at posting; Gaming built pricing engines and stalled at measuring profit. Every HANDOFF is
well-written and the code is verified working -- the skipped step is always the unglamorous
recurring chore, never the engineering. The fix is behavioral: give each active project one
recurring 15-minute chore (price update, symptom log, a post, a P&L check), scheduled the
same way GUOptimizer's own refresh task already runs -- proof this person already knows how
to automate a cadence when it's the interesting kind of problem.

---

## Bottom line

The two assets that actually compound are the coin portfolio's liquidation decisions and
Documentation's AI case studies. Gaming only earns its current share of hours after moves 1
and 3 prove it's net-positive. Everything else is one decision away from archive, or one
20-minute chore away from being useful again.
