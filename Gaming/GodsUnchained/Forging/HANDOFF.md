# GU Forge Assistant — Technical Handoff

This document is for a developer taking over the codebase. For end-user
instructions see **README.md**.

---

## Overview

A CustomTkinter desktop app that automates Gods Unchained card forging on
Immutable zkEVM (chain `13371`). It reads your inventory and market prices from
GU/Immutable APIs, and forges cards **directly on-chain** using a wallet private
key — no launcher window or MetaMask clicking required.

- **Language:** Python 3.11+
- **UI:** `customtkinter` + a native `ttk.Treeview` for the card table
- **Chain:** `web3.py` / `eth-account` against the Immutable zkEVM RPC
- **No database** — all state is local JSON caches

---

## File map

| File | Responsibility |
|---|---|
| `main.py` | Entry point — creates and runs `ForgeApp`. |
| `app.py` | The entire UI: the table, filters, recipe panel, confirm/cost dialogs, and the threaded forge runner. |
| `config.py` | Constants (contract addresses, API URLs, forge ratios, GODS costs), `.env` loading, settings persistence. |
| `market.py` | Read-side GU/Immutable API: inventory, in-game cards, floor prices, ETH/GODS prices, card metadata, and **auth** (GU bearer token). |
| `forge_calc.py` | Pure functions: profit math, tier ratios, marketplace fees, `next_quality`. No I/O. |
| `forge_api.py` | The **forge engine** — the on-chain + backend flow that actually completes a forge. |
| `automation.py` | Legacy fallback that drives the GU launcher via Chrome DevTools/Playwright. Only used when no `PRIVATE_KEY` is set. |
| `requirements.txt` / `install.bat` | Dependencies. |
| `gu_forge.ico` | App icon. |

Runtime-generated (git-ignored, safe to delete):
`gu_token_cache.json`, `token_proto_cache.json`, `floor_cache.json`,
`settings.json`, `forge_logs/`.

---

## The forge flow (the important part)

Completing a GU forge takes **three** things, and missing the third is why naive
attempts never settle:

1. **Create the order** — `POST` to the GU *fusing* API returns an order with a
   list of on-chain "actions".
2. **Execute the on-chain actions** with the wallet key via `web3.py`:
   - `burnBatch` of the source card token IDs on the GU ERC-721 contract, and
   - a GODS ERC-20 `transfer` of the forge fee to the payment address.
3. **Tell the factory** — `PUT` the transaction hash(es) to
   `factory.prod.prod.godsunchained.com/orders/{user_id}/{order_id}`. **This is
   the step that finalizes the forge.** Then poll that order until its status is
   complete; the response contains the **minted card's asset id**, which is what
   lets you chain to the next tier.

Key functions in `forge_api.py`:

- `forge_one(...)` — a single forge (one tier, one output): create → execute →
  PUT → wait → return the minted asset id.
- `_lift_one_tier(proto, q, nq, pool, …)` — forge ONE tier: turn a `pool` of
  quality-`q` asset ids into `nq` cards, pipelined (txs back-to-back with managed
  nonces, receipts awaited together) with late-mint reconciliation against
  inventory. Shared building block.
- `forge_chain(proto, from_quality, target_quality, …)` — cascade one starting
  pool straight up the ladder, calling `_lift_one_tier` per tier (each tier's
  mints feed the next).
- `combine_yield(target, contributions) -> (count, leftover)` — pure calc of how
  many `target` cards a mix yields after cascading & **merging** each tier's
  contribution with what was forged from below.
- **`forge_combine_plan(proto, operations, …)`** — the current UI's forge path.
  `operations` is a list of `{"target": q, "contribute": {tier: count}}`. For each
  op it reserves the exact contributed asset ids (distinct slices per tier across
  all ops, taken from one initial inventory fetch so nothing is used twice), then
  cascades: at each tier it pools `carry` (minted from below) + that tier's
  reserved ids and calls `_lift_one_tier`. This is what lets *2 Gold + 10 Shadow +
  25 Meteorite* combine into 1 Diamond.
- `forge_plan(...)` — older `(from, target, qty)` model; superseded by
  `forge_combine_plan` but kept for reference.

Ratios (in `config.FORGE_RATIOS`): `2` Plain→Meteorite, then `5` each up to
Diamond. So Meteorite→Diamond consumes `5×5×5 = 125` Meteorites.

---

## Auth

- The GU **refresh token** is read from the launcher's Electron config at
  `~/AppData/Roaming/immutable-launcher/config.json` (works even when the
  launcher is closed, as long as it has been logged into once).
- `market.get_gu_auth_token()` exchanges it for a short-lived Bearer (via the GU
  apollo-auth endpoint) and caches both in `gu_token_cache.json`, auto-refreshing
  when expired.
- The forge **wallet** comes only from `.env` (`WALLET_ADDRESS` + `PRIVATE_KEY`).
  `config.PRIVATE_KEY` empty ⇒ `forge_api.api_mode_available()` is `False` ⇒ the
  UI falls back to launcher mode.

---

## UI architecture (`app.py`)

- **One row per card (proto).** `_load_data` aggregates all owned (proto,
  quality) groups into a single dict per card with a `holdings` map
  (`{quality: count}`) plus `asset_ids`. The "Owned (by tier)" column renders the
  per-shine breakdown; the profit columns use a "primary" recipe (lowest owned
  tier → next).
- **Table** is a `ttk.Treeview` styled `Forge.Treeview`. The `#0` tree column is
  a **checkbox** (`☐`/`☑`); other clicks select the row (`browse` mode) and fill
  the recipe panel via `_on_row_select`.
- **State is keyed by PROTO, never by tree row id.** `self._checked` (set of
  protos) and `self._recipes` (`{proto: [op, …]}`) survive table rebuilds
  (refresh / sort / filter), which reassign row ids. `_populate_table` prunes
  these only against **all owned** protos (`self._cards`), not the filtered
  visible subset, so a search/filter never drops a queued recipe. Helpers:
  `_set_check(proto, on)` / `_iid_for_proto` / `_render_check`.
- **Recipe = combine ops.** Each op is `{"target": q, "contribute": {tier: count}}`.
  `_show_recipe_panel` (inline, in the replaceable `self._panel_body`) lets the user
  pick a target and type per-tier contributions; it previews the result live via
  `forge_api.combine_yield` and appends ops to `self._recipes[proto]`. Per-tier
  "remaining" accounts for what other queued ops already consume. `_combine_forges`
  computes the forge count (for GODS cost).
- **Forge queue** (`_refresh_queue`, persistent `self._queue_frame` above the
  builder) lists every card with a saved recipe; ✕ removes one
  (`_remove_from_queue`), clicking a name jumps to it (`_select_proto`).
- **Forging.** `_on_forge_click` builds the batch from `self._checked` using a
  `{proto: card}` map over **`self._cards`** (so hidden-but-queued cards are
  included), attaching each card's `combine_ops` (a checked card with no recipe
  defaults to "lowest shine → next tier, max"). `_run_forges` (worker thread) calls
  `forge_api.forge_combine_plan` per card. Recipes are cleared after a successful
  batch. All forge calls take a `stop_event` and stream log lines to the UI and a
  timestamped `forge_logs/` file.
- **Profitability toggle** controls whether the slow floor scan runs and whether
  the profit columns/dialogs are shown.
- **Diagnostics.** `_dbg()` appends recipe/queue lifecycle lines to
  `forge_logs/recipe_debug.log` — harmless, safe to delete or strip.

---

## Known limitations / risks

- **Undocumented endpoints.** The fusing, factory, marketplace-legacy, and
  apollo-auth endpoints are GU-internal and could change without notice. They
  have historically been stable for long stretches, but expect occasional
  maintenance.
- **Public RPC rate limits.** `rpc.immutable.com` throttles under load; large
  chains may need a retry. Swapping in a private RPC URL (`config.ZKEVM_RPC`) is
  the easy fix.
- **GODS cost table.** `config.DEFAULT_GODS_COSTS` must match GU's current
  per-rarity forge cost; it's user-editable via the ⚙ Costs dialog.
- **Hot wallet.** The private key sits in `.env` in plain text. This is inherent
  to unattended signing — documented to users; use a dedicated low-value wallet.
- **Terms of Service.** Automating game/marketplace actions may conflict with GU
  / Immutable terms. Operating the tool is the user's responsibility.

---

## Possible extensions

- A custodial "forge-as-a-service" mode (watch a wallet for deposited cards +
  GODS, forge, and return them) was prototyped during development but is **not
  included** in this release.
- Replace the launcher-config token source with a proper OAuth login flow to drop
  the launcher dependency entirely.
