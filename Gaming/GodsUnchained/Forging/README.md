# GU Forge Assistant

A Windows desktop app for **automating card forging in Gods Unchained** (GU),
with a built-in **profitability calculator**. It lists every card you own that
can be forged, shows the market floor prices and expected profit of forging it
up a tier, and forges cards for you — including multi-tier "chains"
(e.g. Meteorite → Shadow → Gold → Diamond) — with a single click.

Forging is done **directly on-chain** (no clicking through the launcher): the app
signs the GODS payment, burns the source cards, and tells the GU backend to
complete the forge. A 125-Meteorite → Diamond chain runs unattended in a few
minutes.

---

## 1. Requirements

- **Windows 10/11**
- **Python 3.11+** (3.13 recommended) — <https://www.python.org/downloads/>
  (tick *"Add Python to PATH"* during install)
- A **Gods Unchained account** that you have logged into at least once via the
  Immutable / GU desktop launcher (this is how the app gets your inventory).
- A **dedicated forging wallet** with some GODS (the forge fee) and a little IMX
  for gas.

---

## 2. Install

1. Unzip this folder anywhere (e.g. `C:\GU-Forge`).
2. Double-click **`install.bat`** — it installs the Python dependencies.
   *(Or open a terminal in the folder and run `pip install -r requirements.txt`.)*

---

## 3. Configure your wallet

The app forges using your own wallet, which you provide via a `.env` file.

1. Copy **`.env.example`** to **`.env`** (same folder).
2. Open `.env` and fill in:
   - `WALLET_ADDRESS` — your forging wallet's public address
   - `PRIVATE_KEY` — that wallet's private key (`0x` + 64 hex chars)

> ⚠ **Hot-wallet warning.** The private key is stored in plain text and used to
> sign payments automatically. **Use a dedicated wallet** that holds only the
> GODS + gas you intend to spend on forging — never your main wallet.

If you leave `PRIVATE_KEY` blank, the app runs in **Launcher mode** instead
(slower, drives the GU launcher window). **API mode** (key provided) is
recommended.

---

## 4. Run

Double-click **`run.bat`** (or run `python main.py` in a terminal).

The header shows your wallet, current mode (**API mode** in green = ready), your
GODS balance, and live ETH/GODS prices. The first load takes a few seconds while
it fetches your inventory and market floor prices.

---

## 5. Using the app

### The card list (left)
One row per card (all the different "shines" of a card are combined into a single
row). Columns:

| Column | Meaning |
|---|---|
| **✓** | Tick to queue the card for forging |
| **Card / Set / Rarity** | Card identity |
| **Owned (by tier)** | How many you own of each shine, e.g. `Met 126  Sha 6` (Pln/Met/Sha/Gld/Dia) |
| **Input / Output ETH** | Market floor price of the source / forged card |
| **Fee** | Marketplace sale fee on the output |
| **GODS** | GODS cost per single forge |
| **Profit / ROI** | Expected profit of forging up one tier, after fees + GODS |

- **Click a column header** to sort (click again to reverse).
- Use the **Quality**, **Search**, and **Min profit** filters at the top to
  narrow the list. *(Searching/filtering only hides rows — it never affects what
  you've already queued.)*
- **Profitability** toggle: turn off to skip the (slow) market price scan when
  you only care about forging, not profit.

### Building a recipe — the panel on the right
Click any card row. The right-hand panel lets you build a **recipe** that forges
*upward* to a target shine, pooling cards from several lower shines at once:

1. **Make** — pick the target shine (e.g. Diamond).
2. **Use your cards toward it** — for each lower shine you own, type how many to
   pour in (or hit **Max**). They **cascade and combine** at each tier. Example:
   *2 Gold + 10 Shadow + 25 Meteorite* →
   25 Meteorite makes 5 Shadow → 15 Shadow total makes 3 Gold → 5 Gold total
   makes **1 Diamond**. The panel shows "→ makes N {target}" live, plus any
   leftover.
3. **➕ Add to recipe** — saves it. Add more ops to make a **mix** from one card
   (e.g. 1 Diamond *and* 3 Golds); the per-tier "/ N" shows how many cards you
   have left after what you've already queued.
4. The card is now **queued** (see below). Build recipes for as many cards as you
   like — switching cards, searching, or sorting never loses a saved recipe.

> The old "make N of a tier from a single source" is just a special case here:
> set **Make** = Shadow and put your Meteorites in — or use **Max** on one tier.

### The Forge queue (top of the right panel)
Every card you add a recipe to appears in the **🗒 Forge queue** at the top of the
panel, and its row turns **green** in the table. The queue persists no matter
which card you're currently viewing.

- **✕** next to a queue entry removes it.
- **Click a queue entry's name** to jump back to that card and edit its recipe.

### Forging
Click **Forge Selected (N)** at the bottom — it forges **every queued card** using
its saved recipe, in one batch (even cards currently hidden by a search/filter).
A card that's ticked but has no custom recipe is forged up one tier at the maximum
amount. You'll get a confirmation showing what each card makes, total cards used,
and GODS cost vs. your balance before anything happens. The queue clears
automatically once the batch is forged.

### Safety switches (bottom bar)
- **Dry Run** — simulate without spending anything (on by default). Turn it
  **off** to forge for real.
- **Auto-confirm** — skip the per-forge confirmation dialog.

### Costs
The **⚙ Costs** button lets you adjust the GODS cost per forge by rarity, in case
GU changes the numbers.

---

## 6. Troubleshooting

- **"GU auth token rejected / expired"** — open the GU launcher and log in once,
  then click **↺ Refresh** in the app. The login token is cached afterwards.
- **Wallet badge shows "launcher mode"** — your `.env` is missing or
  `PRIVATE_KEY` is blank. Fill it in and restart.
- **"Private key mismatch"** — `PRIVATE_KEY` and `WALLET_ADDRESS` in `.env` are
  for different wallets. They must match.
- **Forge seems slow** — large chains do real on-chain work tier by tier; this
  is normal. The public RPC can also rate-limit; retry with **↺ Refresh**.

---

## 7. Files

Everything the app needs is in this folder. Caches and logs
(`gu_token_cache.json`, `floor_cache.json`, `settings.json`, `forge_logs/`) are
created automatically at runtime and are safe to delete.

For a technical overview, see **HANDOFF.md**.
