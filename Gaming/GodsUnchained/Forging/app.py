"""GU Forge Assistant — main UI (CustomTkinter)."""
import threading
import time
from tkinter import ttk     # native, aligned, fast table (Treeview)
from typing import Optional

import customtkinter as ctk

# Background of the scrollable table area.
SCROLL_BG = "#0f0f1a"

from config import QUALITIES, FORGE_RATIOS, WALLET_ADDRESS, load_settings, save_settings, DEFAULT_GODS_COSTS
from forge_calc import next_quality, gods_cost_for, calc_profit, forge_ratio, marketplace_fee
from market import (
    fetch_owned_nfts, scan_all_floor_prices, fetch_ingame_plain_cards,
    get_eth_usd, get_gods_eth, get_card_meta, prefetch_card_meta, invalidate_floor,
    load_cached_floors, floor_cache_age_sec, FLOOR_DISK_TTL,
)
from automation import forge_card
import forge_api

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

from pathlib import Path
LOG_DIR = Path(__file__).parent / "forge_logs"
LOG_DIR.mkdir(exist_ok=True)


def _safe_toplevel(parent) -> ctk.CTkToplevel:
    win = ctk.CTkToplevel(parent)
    win.after(210, lambda: _suppress_icon(win))
    return win


def _suppress_icon(win):
    try:
        win.iconbitmap("")
    except Exception:
        pass

class ForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GU Forge Assistant")
        self.geometry("1280x740")
        self.minsize(900, 550)

        self.settings = load_settings()
        self._cards:    list[dict] = []
        self._loading   = False
        self._eth_usd:  Optional[float] = None
        self._gods_eth: Optional[float] = None
        self._gods_balance: Optional[float] = None

        self._build_ui()
        self.after(100, self._refresh_async)

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_filters()
        self._build_table()
        self._build_bottom()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, height=48, corner_radius=0, fg_color="#1a1a2e")
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(hdr, text="⚒  GU Forge Assistant",
                     font=("Arial", 15, "bold")).grid(row=0, column=0, padx=16, pady=10)

        self.lbl_prices = ctk.CTkLabel(hdr, text="fetching prices…", text_color="#888")
        self.lbl_prices.grid(row=0, column=1, padx=20)

        self.lbl_gods_bal = ctk.CTkLabel(hdr, text="GODS: …", text_color="#e0c050",
                                         font=("Arial", 12, "bold"))
        self.lbl_gods_bal.grid(row=0, column=2, padx=8)

        wallet_short = f"{WALLET_ADDRESS[:6]}…{WALLET_ADDRESS[-4:]}" if WALLET_ADDRESS else "no wallet"
        mode_badge = "  •  API mode" if forge_api.api_mode_available() else "  •  launcher mode"
        mode_color = "#50d050" if forge_api.api_mode_available() else "#888"
        ctk.CTkLabel(hdr, text=f"Wallet: {wallet_short}{mode_badge}",
                     text_color=mode_color).grid(row=0, column=3, padx=16)

        ctk.CTkButton(hdr, text="↺ Refresh", width=90,
                      command=lambda: self._refresh_async(force_floor_scan=True)
                      ).grid(row=0, column=4, padx=6, pady=8)
        ctk.CTkButton(hdr, text="⚙ Costs", width=90,
                      command=self._open_costs_dialog).grid(row=0, column=6, padx=6, pady=8)

    def _build_filters(self):
        flt = ctk.CTkFrame(self, height=38, corner_radius=0, fg_color="#161625")
        flt.grid(row=1, column=0, sticky="ew")

        ctk.CTkLabel(flt, text="Quality:").grid(row=0, column=0, padx=(12, 4), pady=6)
        self.var_quality = ctk.StringVar(value="All")
        self._quality_menu = ctk.CTkOptionMenu(
            flt, variable=self.var_quality,
            values=["All"] + QUALITIES[:-1],
            command=lambda _: self._apply_filter(), width=120,
        )
        self._quality_menu.grid(row=0, column=1, padx=4)
        self._quality_menu.set("All")

        # Profitability toggle — when OFF we skip the (slow) floor-price scan
        # and hide the profit columns.  Persisted across runs.
        self.var_show_profit = ctk.BooleanVar(
            value=self.settings.get("show_profit", True))
        ctk.CTkCheckBox(flt, text="Profitability", variable=self.var_show_profit,
                        command=self._on_toggle_profit, width=110).grid(
            row=0, column=2, padx=(16, 8))

        self.lbl_minprofit = ctk.CTkLabel(flt, text="Min profit ETH:")
        self.lbl_minprofit.grid(row=0, column=3, padx=(8, 4))
        self.var_min_profit = ctk.StringVar(
            value=str(self.settings.get("min_profit_eth", 0.0)))
        self.ent_minprofit = ctk.CTkEntry(flt, textvariable=self.var_min_profit, width=90)
        self.ent_minprofit.grid(row=0, column=4, padx=4)
        self.ent_minprofit.bind("<Return>", lambda _: self._apply_filter())

        ctk.CTkLabel(flt, text="Search:").grid(row=0, column=5, padx=(16, 4))
        self.var_search = ctk.StringVar()
        self.var_search.trace_add("write", lambda *_: self._apply_filter_debounced())
        ctk.CTkEntry(flt, textvariable=self.var_search, width=160).grid(row=0, column=6, padx=4)

        ctk.CTkLabel(flt, text="(click a header to sort)",
                     text_color="#666").grid(row=0, column=7, padx=(16, 4))

        # Select all checkbox
        self.var_select_all = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(flt, text="Select all", variable=self.var_select_all,
                        command=self._toggle_select_all, width=100).grid(
            row=0, column=8, padx=16)

    # Treeview data columns: id -> (heading, width, anchor).  (A checkbox lives
    # in the tree's #0 column on the far left.)  Quantity / target / source are
    # all chosen in the per-card Forge dialog now.
    TCOLS = {
        "card":    ("Card",        200, "w"),
        "set":     ("Set",         110, "w"),
        "rarity":  ("Rarity",       80, "w"),
        "owned":   ("Owned (by tier)", 185, "w"),
        "input":   ("Input ETH",    95, "e"),
        "output":  ("Output ETH",   95, "e"),
        "fee":     ("Fee",          50, "center"),
        "gods":    ("GODS",         55, "center"),
        "profit":  ("Profit ETH",  100, "e"),
        "roi":     ("ROI %",        80, "e"),
    }

    def _build_table(self):
        mid = ctk.CTkFrame(self, corner_radius=0, fg_color=SCROLL_BG)
        mid.grid(row=2, column=0, sticky="nsew")
        mid.grid_columnconfigure(0, weight=1)                # table grows
        mid.grid_columnconfigure(1, weight=0, minsize=380)   # recipe panel (fixed)
        mid.grid_rowconfigure(0, weight=1)

        outer = ctk.CTkFrame(mid, corner_radius=0, fg_color=SCROLL_BG)
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        try:
            style.theme_use("clam")        # 'clam' respects custom colours best
        except Exception:
            pass
        style.configure("Forge.Treeview",
                        background="#161922", fieldbackground="#161922",
                        foreground="#e8eaf0", rowheight=29, borderwidth=0,
                        font=("Segoe UI", 11))
        style.configure("Forge.Treeview.Heading",
                        background="#232842", foreground="#eef0f8",
                        font=("Segoe UI", 11, "bold"), relief="flat", padding=5)
        style.map("Forge.Treeview.Heading",
                  background=[("active", "#30365a")])
        style.map("Forge.Treeview",
                  background=[("selected", "#3a6ea5")],
                  foreground=[("selected", "#ffffff")])

        cols = tuple(self.TCOLS.keys())
        # show="tree headings" keeps the #0 column, which we use as a checkbox.
        self.tree = ttk.Treeview(outer, columns=cols, show="tree headings",
                                 style="Forge.Treeview", selectmode="browse")
        self.tree.heading("#0", text="✓")
        self.tree.column("#0", width=40, minwidth=40, anchor="center", stretch=False)
        for cid, (txt, w, anc) in self.TCOLS.items():
            self.tree.heading(cid, text=txt,
                              command=lambda c=cid: self._sort_by_column(c))
            self.tree.column(cid, width=w, anchor=anc, stretch=False)

        self._checked: set[int] = set()   # PROTOS the user has ticked (stable across rebuilds)
        self._recipes: dict[int, list] = {}   # proto -> plan_ops (persists across selects)

        vsb = ttk.Scrollbar(outer, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Rows are tinted by QUALITY TIER (two shades each for zebra striping),
        # so cards are easy to tell apart and you can see each tier at a glance.
        # Text stays light for readability; the tint is the cue, not the text.
        qual_tint = {
            "Plain":     ("#1f2e25", "#19271f"),
            "Meteorite": ("#332024", "#2b1a1e"),
            "Shadow":    ("#2b2037", "#241b2e"),
            "Gold":      ("#322c19", "#2a2514"),
            "Diamond":   ("#192d35", "#15272d"),
        }
        for q, (odd, even) in qual_tint.items():
            self.tree.tag_configure(f"q_{q}_odd",  background=odd)
            self.tree.tag_configure(f"q_{q}_even", background=even)
        self.tree.tag_configure("q__odd",  background="#1d2030")   # fallback
        self.tree.tag_configure("q__even", background="#181a28")
        # Checked (queued-to-forge) rows get a distinct green tint that PERSISTS
        # regardless of which row is currently highlighted in the panel — so you
        # can see every card you've queued, not just the one you're editing.
        self.tree.tag_configure("checked", background="#1f5c3a", foreground="#eafff0")

        self.tree.bind("<Button-1>", self._on_tree_click)
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

        # ── Recipe panel (right side) — replaces the old popup dialog ──
        self.panel = ctk.CTkScrollableFrame(mid, width=360, fg_color="#14161f")
        self.panel.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        self._panel_proto = None
        # PERSISTENT forge queue at the top — lists every saved recipe so you can
        # see what's queued no matter which card is currently open below.
        self._queue_frame = ctk.CTkFrame(self.panel, fg_color="#101a12", corner_radius=6)
        self._queue_frame.pack(fill="x", padx=6, pady=(6, 4))
        # The per-card recipe builder lives in a single replaceable body frame,
        # rebuilt on each selection (kept BELOW the queue).
        self._panel_body = ctk.CTkLabel(
            self.panel, text="Select a card on the left\nto build a forge recipe.",
            text_color="#777", justify="center")
        self._panel_body.pack(pady=40)
        self._refresh_queue()
        self._dbg("==================== session start ====================")

        self._tree_items: dict[str, dict] = {}   # item id -> card
        # Default sort: best profit first when profitability is on, else by owned count.
        if self.var_show_profit.get():
            self._sort_state = {"col": "profit", "reverse": True}
        else:
            self._sort_state = {"col": "owned", "reverse": True}
        self._apply_profit_visibility()

    # Columns that only make sense when profitability is on.
    _PROFIT_COLS = ("input", "output", "fee", "profit", "roi")

    def _apply_profit_visibility(self):
        """Show/hide the profit columns + the Min-profit filter based on the toggle."""
        on = self.var_show_profit.get()
        if on:
            self.tree.configure(displaycolumns="#all")
        else:
            self.tree.configure(displaycolumns=[c for c in self.TCOLS
                                                if c not in self._PROFIT_COLS])
        # Min-profit filter only matters with profit data.
        for w in (getattr(self, "lbl_minprofit", None), getattr(self, "ent_minprofit", None)):
            if w is not None:
                (w.grid if on else w.grid_remove)()

    def _on_toggle_profit(self):
        on = self.var_show_profit.get()
        self.settings["show_profit"] = on
        save_settings(self.settings)
        # Don't sort by a now-hidden column.
        if not on and self._sort_state["col"] in self._PROFIT_COLS:
            self._sort_state = {"col": "owned", "reverse": True}
        self._apply_profit_visibility()
        if on:
            # Turning it on needs floor prices → rescan and rebuild.
            self._refresh_async(force_floor_scan=True)
        else:
            self._apply_filter()

    def _build_bottom(self):
        bot = ctk.CTkFrame(self, height=52, corner_radius=0, fg_color="#1a1a2e")
        bot.grid(row=3, column=0, sticky="ew")
        bot.grid_columnconfigure(3, weight=1)

        self.var_auto_confirm = ctk.BooleanVar(value=self.settings.get("auto_confirm", False))
        ctk.CTkCheckBox(bot, text="Auto-Confirm Metamask",
                        variable=self.var_auto_confirm,
                        command=self._save_settings).grid(row=0, column=0, padx=16, pady=12)

        self.var_dry_run = ctk.BooleanVar(value=self.settings.get("dry_run", True))
        ctk.CTkCheckBox(bot, text="Dry Run  (no real transactions)",
                        variable=self.var_dry_run,
                        command=self._save_settings,
                        text_color="#e0a000").grid(row=0, column=1, padx=12)

        self.btn_forge = ctk.CTkButton(
            bot, text="Forge Selected  (0)",
            fg_color="#8b1a00", hover_color="#c02200",
            font=("Arial", 13, "bold"), width=200,
            command=self._on_forge_click,
        )
        self.btn_forge.grid(row=0, column=2, padx=20)

        self.lbl_status = ctk.CTkLabel(bot, text="Ready", text_color="#888")
        self.lbl_status.grid(row=0, column=4, padx=16, sticky="e")

    # ── Table population (ttk.Treeview) ─────────────────────────────────────────

    _QUAL_SHORT = {"Plain": "Pln", "Meteorite": "Met", "Shadow": "Sha",
                   "Gold": "Gld", "Diamond": "Dia"}

    def _row_values(self, card: dict) -> tuple:
        ingame    = card.get("ingame", False)
        in_floor  = card.get("input_floor")
        out_floor = card.get("output_floor")
        profit    = card.get("profit")
        roi       = card.get("roi")
        # Owned, broken down per tier, e.g. "Met 126  Sha 6".
        h = card.get("holdings", {})
        owned = "  ".join(f"{self._QUAL_SHORT.get(q, q)} {h[q]}"
                          for q in QUALITIES if h.get(q)) or "0"
        return (
            card.get("name", f"proto:{card['proto']}"),
            (card.get("set", "") or "—").title(),
            (card.get("rarity", "") or "").capitalize(),
            owned,
            "in-game" if ingame else (f"{in_floor:.5f}" if in_floor else "—"),
            f"{out_floor:.5f}" if out_floor else "—",
            f"{card.get('fee_pct', 0):.0f}%",
            f"{card.get('gods_cost', 0):.1f}",
            f"{profit:+.5f}" if profit is not None else "—",
            ("+∞" if roi is not None and roi > 99999
             else f"{roi:+.1f}%") if roi is not None else "—",
        )

    def _populate_table(self, cards: list[dict]):
        # _checked and _recipes are keyed by PROTO, so they survive a rebuild
        # (refresh / re-sort / filter) — only entries for cards that vanished
        # from inventory are pruned. Recipes are cleared explicitly after a forge.
        self.tree.delete(*self.tree.get_children())
        self._tree_items.clear()
        # Prune against ALL owned cards, NOT the filtered/visible subset — a
        # recipe must survive even while its card is hidden by a search/filter.
        owned = {c["proto"] for c in self._cards}
        present = {c["proto"] for c in cards}
        for p in [p for p in self._recipes if p not in owned or not self._recipes[p]]:
            self._recipes.pop(p, None)
        self._checked &= owned
        self._checked |= set(self._recipes)          # a recipe implies "queued"
        self._dbg(f"POPULATE visible={len(cards)} owned={len(owned)} "
                  f"queued={[p for p,o in self._recipes.items() if o]}")
        for i, card in enumerate(cards):
            parity = "odd" if i % 2 else "even"
            q = card.get("quality", "")
            tag = f"q_{q}_{parity}" if q in QUALITIES else f"q__{parity}"
            iid = self.tree.insert("", "end", text="☐",
                                   values=self._row_values(card), tags=(tag,))
            self._tree_items[iid] = card
            if card["proto"] in self._checked:        # restore the ✓ + green tint
                self._render_check(iid, True)
        self._update_forge_btn()
        if hasattr(self, "_queue_frame"):
            self._refresh_queue()

    # ── Row interactions ────────────────────────────────────────────────────────

    def _on_tree_click(self, event):
        # Clicking the ✓ column toggles the checkbox.  Every other click just
        # selects the row (browse mode), which fills the recipe panel.
        if self.tree.identify_region(event.x, event.y) == "heading":
            return                       # let header-click sorting work
        if self.tree.identify_column(event.x) == "#0":
            iid = self.tree.identify_row(event.y)
            if iid:
                self._toggle_check(iid)

    def _on_row_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        card = self._tree_items.get(sel[0])
        if card:
            self._show_recipe_panel(card)

    def _iid_for_proto(self, proto):
        for iid, c in self._tree_items.items():
            if c["proto"] == proto:
                return iid
        return None

    def _render_check(self, iid, on: bool):
        """Update one row's checkbox glyph + green tint (no state change)."""
        tags = [t for t in self.tree.item(iid, "tags") if t != "checked"]
        self.tree.item(iid, text="☑" if on else "☐",
                       tags=tags + (["checked"] if on else []))

    def _set_check(self, proto, on: bool):
        """Check/uncheck a card BY PROTO (stable across table rebuilds)."""
        if on:
            self._checked.add(proto)
        else:
            self._checked.discard(proto)
        iid = self._iid_for_proto(proto)
        if iid:
            self._render_check(iid, on)
        self._update_forge_btn()

    def _toggle_check(self, iid):
        proto = self._tree_items[iid]["proto"]
        self._set_check(proto, proto not in self._checked)

    # ── Selection / sorting ──────────────────────────────────────────────────────

    def _toggle_select_all(self):
        check = self.var_select_all.get()
        for c in self._tree_items.values():
            self._set_check(c["proto"], check)

    def _update_forge_btn(self):
        n = len(self._checked) if hasattr(self, "_checked") else 0
        self.btn_forge.configure(text=f"Forge Selected  ({n})")

    # ── Forge queue (persistent list of saved recipes) ───────────────────────────

    def _dbg(self, msg: str):
        """Append a line to forge_logs/recipe_debug.log (diagnostics only)."""
        try:
            import datetime as _dt
            with open(LOG_DIR / "recipe_debug.log", "a", encoding="utf-8") as f:
                f.write(f"{_dt.datetime.now():%H:%M:%S} {msg}\n")
        except Exception:
            pass

    def _refresh_queue(self):
        """Redraw the persistent queue from self._recipes (called on every change)."""
        for w in self._queue_frame.winfo_children():
            w.destroy()
        queued = [(p, ops) for p, ops in self._recipes.items() if ops]
        if not queued:
            ctk.CTkLabel(self._queue_frame, text="Forge queue: empty",
                         text_color="#5e6b5e", font=("Arial", 11)).pack(
                anchor="w", padx=8, pady=6)
            return
        ctk.CTkLabel(self._queue_frame, text=f"🗒  Forge queue ({len(queued)})",
                     font=("Arial", 12, "bold"), text_color="#bfe8c2").pack(
            anchor="w", padx=8, pady=(5, 2))
        # Names from ALL owned cards so a queued card still shows its name even
        # when it's hidden by the current search/filter.
        names = {c["proto"]: c.get("name", f"proto:{c['proto']}")
                 for c in self._cards}
        for proto, ops in queued:
            row = ctk.CTkFrame(self._queue_frame, fg_color="transparent")
            row.pack(fill="x", padx=6, pady=1)
            ctk.CTkButton(row, text="✕", width=24, height=24,
                          fg_color="#5a1a1a", hover_color="#8a2a2a",
                          command=lambda p=proto: self._remove_from_queue(p)
                          ).pack(side="left", padx=(0, 6))
            steps = ", ".join(
                f"{forge_api.combine_yield(op['target'], op['contribute'])[0]}x {op['target']}"
                for op in ops)
            lbl = ctk.CTkLabel(row, text=f"{names.get(proto, proto)}: {steps}",
                               anchor="w", justify="left", font=("Arial", 11),
                               text_color="#dfe8df", wraplength=265)
            lbl.pack(side="left", fill="x", expand=True)
            lbl.bind("<Button-1>", lambda _e, p=proto: self._select_proto(p))

    def _remove_from_queue(self, proto):
        self._dbg(f"REMOVE proto={proto}")
        self._recipes.pop(proto, None)
        self._set_check(proto, False)
        self._refresh_queue()
        if self._panel_proto == proto:        # rebuild the open builder so it resets
            iid = self._iid_for_proto(proto)
            if iid:
                self._show_recipe_panel(self._tree_items[iid])

    def _select_proto(self, proto):
        iid = self._iid_for_proto(proto)
        if iid:
            self.tree.selection_set(iid)
            self.tree.see(iid)
            self._on_row_select()

    def _combine_forges(self, target: str, contribute: dict) -> int:
        """Total number of individual forges a combine op performs (for GODS cost)."""
        order = QUALITIES
        ti = order.index(target)
        starts = [order.index(q) for q, n in contribute.items()
                  if n and order.index(q) < ti]
        if not starts:
            return 0
        carry = total = 0
        for level in range(min(starts), ti):
            q = order[level]
            ratio = FORGE_RATIOS[q]
            f = (contribute.get(q, 0) + carry) // ratio
            total += f
            carry = f
        return total

    def _needed_extra(self, target, contribute, tier, want):
        """Smallest number of EXTRA `tier` cards (other contributions unchanged)
        that brings the combine yield up to `want` of `target`.  None if even a
        huge amount wouldn't (e.g. tier is above the target)."""
        base = dict(contribute)
        cur = base.get(tier, 0)
        yld = lambda extra: forge_api.combine_yield(target, {**base, tier: cur + extra})[0]
        if yld(0) >= want:
            return 0
        k = 1
        while yld(k) < want:
            k *= 2
            if k > 10_000_000:
                return None
        lo, hi = k // 2, k
        while lo < hi:
            mid = (lo + hi) // 2
            if yld(mid) >= want:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def _show_recipe_panel(self, card: dict):
        """Inline 'combine upward' recipe builder: pick a TARGET tier, then choose
        how many of each lower shine to pour in.  Contributions cascade and MERGE
        at each tier (e.g. 2 Gold + 10 Shadow + 25 Meteorite → 1 Diamond).  Add
        several ops to make a mix of targets from one card."""
        self._panel_body.destroy()
        body = self._panel_body = ctk.CTkFrame(self.panel, fg_color="transparent")
        body.pack(fill="both", expand=True)
        proto = self._panel_proto = card["proto"]
        self._dbg(f"PANEL proto={proto} queued={[p for p,o in self._recipes.items() if o]}")

        name     = card.get("name", f"proto:{proto}")
        order    = QUALITIES
        g_cost   = card.get("gods_cost", 0)
        holdings = dict(card.get("holdings", {}))
        SH       = self._QUAL_SHORT

        ctk.CTkLabel(body, text=name, font=("Arial", 15, "bold"),
                     wraplength=330, justify="left").pack(pady=(8, 2), padx=12, anchor="w")
        own = "   ".join(f"{SH.get(q,q)} {holdings.get(q,0)}" for q in order if holdings.get(q, 0))
        ctk.CTkLabel(body, text=f"You own — {own}", text_color="#aaa",
                     wraplength=330, justify="left").pack(pady=(0, 6), padx=12, anchor="w")

        owned_tiers = [q for q in order[:-1] if holdings.get(q, 0) > 0]
        if not owned_tiers:
            ctk.CTkLabel(body, text="Nothing forgeable here.",
                         text_color="#d05050").pack(pady=16)
            return

        recipe = self._recipes.setdefault(proto, [])   # list of {target, contribute}

        def _remaining(tier):
            used = sum(op["contribute"].get(tier, 0) for op in recipe)
            return holdings.get(tier, 0) - used

        # Target = any tier above the lowest one you own.
        lowest = order.index(owned_tiers[0])
        target_opts = order[lowest + 1:]
        var_target = ctk.StringVar(value=target_opts[-1])   # default to the highest

        trow = ctk.CTkFrame(body, fg_color="transparent")
        trow.pack(fill="x", padx=12, pady=(2, 2))
        ctk.CTkLabel(trow, text="Make", width=44, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkOptionMenu(trow, variable=var_target, values=target_opts, width=150,
                          command=lambda _: _rebuild()).grid(row=0, column=1, padx=6)

        ctk.CTkLabel(body, text="Use your cards toward it:", text_color="#9aa3b0",
                     font=("Arial", 11)).pack(anchor="w", padx=12, pady=(6, 0))
        contrib_frame = ctk.CTkFrame(body, fg_color="transparent")
        contrib_frame.pack(fill="x", padx=12)
        entries: dict[str, ctk.StringVar] = {}

        result_lbl = ctk.CTkLabel(body, text="", font=("Arial", 12, "bold"),
                                  wraplength=330, justify="left")
        result_lbl.pack(anchor="w", padx=12, pady=(4, 2))

        # "To make 1 more {target}, add: [+N Gld] [+N Sha] [+N Met]" — one click tops up.
        next_frame = ctk.CTkFrame(body, fg_color="transparent")
        next_frame.pack(fill="x", padx=12, pady=(0, 2))

        plan_box = ctk.CTkTextbox(body, height=100, font=("Consolas", 11), state="disabled")
        plan_box.pack(fill="x", padx=12, pady=(6, 4))
        summary = ctk.CTkLabel(body, text="", font=("Consolas", 11),
                               justify="left", wraplength=330)
        summary.pack(anchor="w", padx=12)

        def _current():
            out = {}
            for t, v in entries.items():
                try:
                    out[t] = max(0, int(v.get() or 0))
                except ValueError:
                    out[t] = 0
            return {t: n for t, n in out.items() if n > 0}

        def _topup(tier, extra):
            try:
                cur = int(entries[tier].get() or 0)
            except ValueError:
                cur = 0
            entries[tier].set(str(min(cur + extra, _remaining(tier))))

        def _refresh_next():
            for w in next_frame.winfo_children():
                w.destroy()
            tgt = var_target.get()
            ti = order.index(tgt)
            tiers = [q for q in order if order.index(q) < ti and holdings.get(q, 0) > 0]
            if not tiers:
                return
            cur = _current()
            want = forge_api.combine_yield(tgt, cur)[0] + 1
            ctk.CTkLabel(next_frame, text=f"To make 1 more {tgt}, add:",
                         text_color="#9aa3b0", font=("Arial", 10)).grid(
                row=0, column=0, columnspan=max(1, len(tiers)), sticky="w", pady=(2, 1))
            col = 0
            for q in reversed(tiers):
                n = self._needed_extra(tgt, cur, q, want)
                if not n:
                    continue
                try:
                    cur_q = int(entries[q].get() or 0)
                except ValueError:
                    cur_q = 0
                afford = (cur_q + n) <= _remaining(q)
                ctk.CTkButton(
                    next_frame, text=f"+{n} {SH.get(q, q)}", width=84, height=24,
                    fg_color="#2a6b3a" if afford else "#4a3a1a",
                    hover_color="#3a8b4a" if afford else "#6a5a2a",
                    command=lambda qq=q, nn=n: _topup(qq, nn)
                ).grid(row=1, column=col, padx=3, pady=1, sticky="w")
                col += 1
            if col == 0:
                ctk.CTkLabel(next_frame, text="(enough for one already — Add it!)",
                             text_color="#bfe8c2", font=("Arial", 10)).grid(
                    row=1, column=0, sticky="w")

        def _update_result(*_):
            yld, lo = forge_api.combine_yield(var_target.get(), _current())
            txt = f"→ makes {yld} {var_target.get()}"
            if lo:
                txt += "    (leftover: " + ", ".join(f"{SH.get(q,q)} {n}" for q, n in lo.items()) + ")"
            result_lbl.configure(text=txt, text_color="#bfe8c2" if yld > 0 else "#d0a000")
            _refresh_next()

        def _rebuild():
            for w in contrib_frame.winfo_children():
                w.destroy()
            entries.clear()
            ti = order.index(var_target.get())
            tiers = [q for q in order if order.index(q) < ti and holdings.get(q, 0) > 0]
            for r, q in enumerate(reversed(tiers)):          # highest contributing tier first
                ctk.CTkLabel(contrib_frame, text=q, width=78, anchor="w").grid(
                    row=r, column=0, sticky="w", pady=1)
                var = ctk.StringVar(value="0")
                entries[q] = var
                var.trace_add("write", _update_result)
                ctk.CTkEntry(contrib_frame, textvariable=var, width=64).grid(row=r, column=1, padx=3)
                ctk.CTkLabel(contrib_frame, text=f"/ {_remaining(q)}", width=52,
                             anchor="w", text_color="#888").grid(row=r, column=2, sticky="w")
                ctk.CTkButton(contrib_frame, text="Max", width=42, fg_color="#333",
                              hover_color="#555",
                              command=lambda qq=q: entries[qq].set(str(_remaining(qq)))
                              ).grid(row=r, column=3, padx=3)
            _update_result()

        def _redraw_plan():
            plan_box.configure(state="normal")
            plan_box.delete("1.0", "end")
            tot_forges = 0
            for i, op in enumerate(recipe, 1):
                yld, _lo = forge_api.combine_yield(op["target"], op["contribute"])
                tot_forges += self._combine_forges(op["target"], op["contribute"])
                src = " + ".join(f"{n} {SH.get(t,t)}" for t, n in op["contribute"].items())
                plan_box.insert("end", f"{i}.  {yld}x {op['target']}  ({src})\n")
            plan_box.configure(state="disabled")
            summary.configure(
                text=f"~ {tot_forges} forges,  {tot_forges*g_cost:.1f} GODS total",
                text_color="#cfd2dc")

        def _add():
            contribute = _current()
            if not contribute:
                result_lbl.configure(text="Enter how many cards to use.", text_color="#d0a000")
                return
            for t, n in contribute.items():
                if n > _remaining(t):
                    result_lbl.configure(text=f"Only {_remaining(t)} {t} left.",
                                         text_color="#d05050")
                    return
            yld, _lo = forge_api.combine_yield(var_target.get(), contribute)
            if yld < 1:
                result_lbl.configure(text="That isn't enough to make one card.",
                                     text_color="#d05050")
                return
            recipe.append({"target": var_target.get(), "contribute": contribute})
            self._set_check(proto, True)
            self._refresh_queue()
            self._dbg(f"ADD proto={proto} {var_target.get()}<-{contribute} "
                      f"-> queued={[p for p,o in self._recipes.items() if o]}")
            _rebuild(); _redraw_plan()

        def _clear():
            recipe.clear()
            self._set_check(proto, False)
            self._refresh_queue()
            _rebuild(); _redraw_plan()

        btns = ctk.CTkFrame(body, fg_color="transparent")
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="Clear", width=80, fg_color="#333", hover_color="#555",
                      command=_clear).grid(row=0, column=0, padx=6)
        ctk.CTkButton(btns, text="➕ Add to recipe", width=160, fg_color="#2a6b3a",
                      hover_color="#3a8b4a", font=("Arial", 12, "bold"),
                      command=_add).grid(row=0, column=1, padx=6)
        ctk.CTkLabel(body, text="Then click “Forge Selected” at the bottom.",
                     text_color="#777", font=("Arial", 10)).pack(pady=(0, 8))

        _rebuild(); _redraw_plan()

    def _visible_cards(self) -> list[dict]:
        q  = self.var_quality.get()
        s  = self.var_search.get().lower()
        try:
            mp = float(self.var_min_profit.get())
        except ValueError:
            mp = 0.0
        return [
            c for c in self._cards
            if (q == "All" or c.get("holdings", {}).get(q, 0) > 0)
            and (not s or s in c.get("name", "").lower())
            and (c.get("profit") is None or (c.get("profit") or 0.0) >= mp)
        ]

    _TEXT_COLS = {"card", "set", "rarity"}

    def _sort_keyfn(self, col):
        def qrank(c):
            return QUALITIES.index(c["quality"]) if c.get("quality") in QUALITIES else 99
        return {
            "card":   lambda c: (c.get("name") or "").lower(),
            "set":    lambda c: ((c.get("set") or "~").lower(),
                                 (c.get("name") or "").lower(), qrank(c)),
            "rarity": lambda c: (c.get("rarity") or ""),
            "owned":  lambda c: c.get("count") or 0,
            "input":  lambda c: c.get("input_floor") or 0.0,
            "output": lambda c: c.get("output_floor") or 0.0,
            "fee":    lambda c: c.get("fee_pct") or 0.0,
            "gods":   lambda c: c.get("gods_cost") or 0.0,
            "profit": lambda c: c.get("profit") if c.get("profit") is not None else -1e9,
            "roi":    lambda c: c.get("roi") if c.get("roi") is not None else -1e9,
        }.get(col, lambda c: 0)

    def _sort_by_column(self, col):
        st = self._sort_state
        if st["col"] == col:
            st["reverse"] = not st["reverse"]
        else:
            st["col"] = col
            st["reverse"] = col not in self._TEXT_COLS   # numbers desc, text asc
        self._apply_filter()

    def _update_sort_indicators(self):
        for cid, (txt, _w, _a) in self.TCOLS.items():
            arrow = ""
            if cid == self._sort_state["col"]:
                arrow = "  ▼" if self._sort_state["reverse"] else "  ▲"
            self.tree.heading(cid, text=txt + arrow)

    def _apply_filter_debounced(self, *_):
        """Coalesce rapid filter triggers (every search keystroke) into one
        rebuild ~250 ms after typing stops — keeps the UI snappy."""
        if getattr(self, "_filter_after_id", None):
            try:
                self.after_cancel(self._filter_after_id)
            except Exception:
                pass
        self._filter_after_id = self.after(250, self._apply_filter)

    def _apply_filter(self, *_):
        self._filter_after_id = None
        visible = self._visible_cards()
        col = self._sort_state["col"] or "profit"
        keyf = self._sort_keyfn(col)
        try:
            visible.sort(key=keyf, reverse=self._sort_state["reverse"])
        except TypeError:
            visible.sort(key=lambda c: str(keyf(c)), reverse=self._sort_state["reverse"])
        self._populate_table(visible)
        self._update_sort_indicators()
        self._status(f"{len(visible)} card group(s)" if visible
                     else "No cards match the current filters.")

    # ── Data loading ──────────────────────────────────────────────────────────

    def _refresh_async(self, force_floor_scan: bool = False):
        if self._loading:
            return
        self._loading = True
        self._status("Loading inventory & prices…")
        threading.Thread(
            target=self._load_data, args=(force_floor_scan,), daemon=True
        ).start()

    def _load_data(self, force_floor_scan: bool = False):
        try:
            eth_usd  = get_eth_usd()
            gods_eth = get_gods_eth()
            self._eth_usd  = eth_usd  or 0.0
            self._gods_eth = gods_eth or 0.0

            gods_usd = self._gods_eth * self._eth_usd
            self.after(0, lambda: self.lbl_prices.configure(
                text=(f"ETH: ${self._eth_usd:,.0f}  |  "
                      f"GODS: ${gods_usd:.4f}  |  "
                      f"GODS/ETH: {self._gods_eth:.6f}")))

            # GODS wallet balance (on-chain) — shown in the header, used by the
            # forge confirmation as a budget guard.
            self._gods_balance = forge_api.gods_balance()
            self.after(0, lambda b=self._gods_balance: self.lbl_gods_bal.configure(
                text=(f"GODS: {b:,.1f}" if b is not None else "GODS: ?")))

            # ── Step 1: inventory (NFTs + in-game plain cards) ────────────────
            self.after(0, lambda: self._status("Fetching NFT inventory…"))
            nfts = fetch_owned_nfts()

            groups: dict[tuple, list] = {}
            for n in nfts:
                groups.setdefault((n["proto"], n["quality"]), []).append(n)

            # In-game plain cards: use the GU API directly (no launcher window needed).
            # The auth token is cached on disk by the launcher; as long as you've
            # logged in at least once, this works with the launcher closed.
            self.after(0, lambda: self._status("Fetching in-game plain cards via GU API…"))
            # plain_asset_ids: (proto, "Plain") → [asset_id, …]
            # Populated here and reused by the forge to skip a second
            # marketplace-legacy call (which is slow and flaky under load).
            plain_asset_ids: dict[tuple, list[int]] = {}
            try:
                ingame = fetch_ingame_plain_cards()
                for g in ingame:
                    if not g.get("proto") or not g.get("count"):
                        continue
                    key = (g["proto"], "Plain")
                    plain_asset_ids[key] = g.get("asset_ids") or []
                    existing = groups.get(key, [])
                    needed   = g["count"] - len(existing)
                    if needed > 0:
                        # Share a single sentinel dict — we only read from it
                        # (ingame flag + token_id=None).  Avoids creating tens
                        # of thousands of individual objects for large inventories.
                        sentinel = {"proto": g["proto"], "quality": "Plain",
                                    "token_id": None, "ingame": True}
                        existing = existing + [sentinel] * needed
                    groups[key] = existing
            except Exception as e:
                err_msg = str(e)
                self.after(0, lambda msg=err_msg:
                    self._status(f"⚠ Plain cards unavailable: {msg}"))
                import traceback; traceback.print_exc()

            # Build set of (proto, quality) keys we own that are forgeable
            owned_keys: set[tuple] = set()
            for (proto, quality), group in groups.items():
                nxt = next_quality(quality)
                if nxt and len(group) >= 2:
                    owned_keys.add((proto, quality))
                    owned_keys.add((proto, nxt))   # also need output floor

            # ── Step 2: bulk floor scan (one pass over all listings) ──────────
            # Skipped entirely when "Profitability" is off — that scan pages
            # through every active ETH listing and is the slowest part of a load.
            if not self.var_show_profit.get():
                floors = {}
                self.after(0, lambda: self._status("Profitability off — skipping floor scan."))
            else:
                # Prefer the on-disk cache when it's less than an hour old.  The
                # Refresh button and post-forge reloads skip the cache via
                # force_floor_scan=True.
                floors = None if force_floor_scan else load_cached_floors(FLOOR_DISK_TTL)
                if floors is not None:
                    age_min = (floor_cache_age_sec() or 0) / 60
                    self.after(0, lambda n=len(floors), a=age_min:
                        self._status(f"Using cached floors ({n} prices, {a:.0f} min old)"))
                else:
                    self.after(0, lambda n=len(owned_keys)//2:
                        self._status(f"Scanning market for {n} forgeable groups…"))

                    def _progress(page_n, found):
                        self.after(0, lambda p=page_n, f=found:
                            self._status(f"Scanning listings… page {p}  ({f} floors found)"))

                    floors = scan_all_floor_prices(owned_keys, progress_cb=_progress)

            # ── Step 3: parallel metadata fetch, then build rows ─────────────
            self.after(0, lambda: self._status("Fetching card names…"))
            unique_protos = list({p for (p, _) in groups})
            prefetch_card_meta(unique_protos)   # parallel, fills cache

            self.after(0, lambda: self._status("Building card list…"))
            custom_costs = self.settings.get("gods_costs", {})

            # ── Aggregate per PROTO (one card = one row; shines handled by the
            # recipe panel).  Keep per-quality holdings / asset ids for the panel.
            per_proto: dict[int, dict] = {}
            for (proto, quality), group in groups.items():
                count = len(group)
                if count < 1:
                    continue
                meta = get_card_meta(proto) or {}
                rarity = meta.get("rarity", "common")
                d = per_proto.setdefault(proto, {
                    "proto":     proto,
                    "name":      meta.get("name", f"proto:{proto}"),
                    "rarity":    rarity,
                    "set":       meta.get("set", "") or "—",
                    "gods_cost": gods_cost_for(rarity, custom_costs),
                    "holdings":  {},
                    "asset_ids": {},
                    "ingame_q":  set(),
                })
                d["holdings"][quality] = d["holdings"].get(quality, 0) + count
                ids = plain_asset_ids.get((proto, quality))
                if ids:
                    d["asset_ids"][quality] = ids
                if quality == "Plain" and all(c.get("ingame") for c in group):
                    d["ingame_q"].add(quality)

            cards = []
            for proto, d in per_proto.items():
                holdings = d["holdings"]
                # "Primary" recipe (for the profit/sort columns) = the lowest
                # shine you own that can be forged up one tier.
                primary_q = next((q for q in QUALITIES
                                  if holdings.get(q, 0) >= 2 and next_quality(q)), None)
                if primary_q is None:
                    continue
                nxt = next_quality(primary_q)
                is_ingame    = primary_q in d["ingame_q"]
                input_floor  = 0.0 if is_ingame else floors.get((proto, primary_q))
                output_floor = floors.get((proto, nxt))
                g_cost       = d["gods_cost"]

                profit_data = None
                if (input_floor is not None) and output_floor and self._gods_eth:
                    profit_data = calc_profit(input_floor, output_floor,
                                              primary_q, nxt, g_cost, self._gods_eth)

                cards.append({
                    "proto":        proto,
                    "name":         d["name"],
                    "rarity":       d["rarity"],
                    "set":          d["set"],
                    "gods_cost":    g_cost,
                    "holdings":     holdings,
                    "asset_ids":    d["asset_ids"],
                    "ingame_q":     d["ingame_q"],
                    "quality":      primary_q,      # primary source (for tint/sort)
                    "next_quality": nxt,
                    "count":        sum(holdings.values()),
                    "forgeable":    holdings.get(primary_q, 0) // forge_ratio(primary_q),
                    "input_floor":  input_floor,
                    "output_floor": output_floor,
                    "ingame":       is_ingame,
                    "fee_pct":      profit_data["fee_pct"] if profit_data else marketplace_fee(nxt) * 100,
                    "profit":       profit_data["profit"] if profit_data else None,
                    "roi":          profit_data["roi"]    if profit_data else None,
                })

            self._cards = cards
            self.after(0, self._apply_filter)
            self.after(0, lambda n=len(cards):
                self._status(f"Done — {n} forgeable card groups loaded."))

        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.after(0, lambda e=str(exc): self._status(f"Error: {e}"))
        finally:
            self._loading = False

    # ── Forge ─────────────────────────────────────────────────────────────────

    def _on_forge_click(self):
        # Each CHECKED card is forged using its saved recipe (built in the panel).
        # A checked card with NO recipe defaults to forging its lowest shine up
        # one tier, max amount.
        # Look up from ALL owned cards, not just the visible rows — a queued card
        # may be hidden by the current search/filter but must still be forged.
        by_proto = {c["proto"]: c for c in self._cards}
        to_forge = []
        for proto in list(self._checked):
            c = by_proto.get(proto)
            if not c:
                continue
            ops = self._recipes.get(proto)
            if ops:
                to_forge.append({**c, "combine_ops": [dict(o) for o in ops]})
                continue
            # No custom recipe: default to forging the lowest shine up one tier, max.
            q   = c.get("quality")
            nxt = c.get("next_quality")
            if not nxt:
                continue
            if c.get("holdings", {}).get(q, 0) // forge_ratio(q) < 1:
                continue
            to_forge.append({**c, "combine_ops": [
                {"target": nxt, "contribute": {q: c["holdings"][q]}}]})
        if not to_forge:
            self._status("No cards checked — tick the ✓ box on the left of each card.")
            return

        auto_c = self.var_auto_confirm.get()
        dry    = self.var_dry_run.get()

        if dry:
            self._open_dry_run_window(to_forge)
        else:
            self._open_forge_confirm(to_forge, auto_c)

    def _open_forge_confirm(self, to_forge: list[dict], auto_confirm: bool):
        """Budget-guard / profit preview shown before any real forge."""
        win = _safe_toplevel(self)
        win.title("Confirm Forge")
        win.geometry("760x540")
        win.grab_set()

        ctk.CTkLabel(win, text="Confirm Forge", font=("Arial", 16, "bold")).pack(pady=(14, 2))
        bal = self._gods_balance
        ctk.CTkLabel(win, text=(f"Your GODS balance: {bal:,.1f}" if bal is not None
                                else "GODS balance: unknown"),
                     text_color="#e0c050", font=("Arial", 12, "bold")).pack(pady=(0, 6))
        status = ctk.CTkLabel(win, text="Calculating costs & profit…", text_color="#e0a000")
        status.pack(pady=6)

        body = ctk.CTkScrollableFrame(win, height=300)
        body.pack(fill="both", expand=True, padx=14, pady=6)
        totals_lbl = ctk.CTkLabel(win, text="", font=("Arial", 12, "bold"))
        totals_lbl.pack(pady=6)

        btnf = ctk.CTkFrame(win, fg_color="transparent")
        btnf.pack(pady=10)
        btn_go = ctk.CTkButton(btnf, text="Confirm & Forge", fg_color="#8b1a00",
                               hover_color="#c02200", font=("Arial", 13, "bold"),
                               state="disabled",
                               command=lambda: (win.destroy(),
                                                self._open_forge_window(to_forge, auto_confirm)))
        btn_go.grid(row=0, column=0, padx=8)
        ctk.CTkButton(btnf, text="Cancel", fg_color="#333", hover_color="#555",
                      command=win.destroy).grid(row=0, column=1, padx=8)

        def _render(summaries):
            if not status.winfo_exists():
                return
            status.destroy()
            heads = ["Card", "Forge", "Cards", "GODS", "Profit ETH"]
            widths = [165, 240, 60, 70, 110]
            for ci, (h, w) in enumerate(zip(heads, widths)):
                ctk.CTkLabel(body, text=h, width=w, anchor="w", font=("Arial", 10, "bold"),
                             text_color="#aaa").grid(row=0, column=ci, padx=4, pady=3, sticky="w")
            tot_gods = tot_profit = 0.0
            have_profit = False
            for ri, s in enumerate(summaries, 1):
                tot_gods += s["gods"]
                if s["profit"] is not None:
                    tot_profit += s["profit"]; have_profit = True
                pc = ("#50d050" if (s["profit"] or 0) > 0 else
                      "#d05050" if (s["profit"] or 0) < 0 else "#888")
                vals = [(s["name"] or "?", "white"),
                        (s["desc"], "#f0c000" if s["is_chain"] else "#cfd2dc"),
                        (str(s["cards_used"]), "white"),
                        (f"{s['gods']:.1f}", "#e0c050"),
                        (f"{s['profit']:+.5f}" if s["profit"] is not None else "—", pc)]
                for ci, (t, c) in enumerate(vals):
                    ctk.CTkLabel(body, text=t, width=widths[ci], anchor="w",
                                 text_color=c, font=("Arial", 11)).grid(
                        row=ri, column=ci, padx=4, pady=1, sticky="w")
            over = bal is not None and tot_gods > bal
            ptxt = f"     Est. profit: {tot_profit:+.5f} ETH" if have_profit else ""
            totals_lbl.configure(
                text=f"Total GODS: {tot_gods:.1f}" +
                     ("   ⚠ EXCEEDS BALANCE" if over else "") + ptxt,
                text_color="#d05050" if over else "#50d050")
            btn_go.configure(state="normal",
                             text="Forge anyway" if over else "Confirm & Forge")

        def _calc():
            summaries = [self._forge_summary(c) for c in to_forge]
            self.after(0, lambda: _render(summaries))

        threading.Thread(target=_calc, daemon=True).start()

    def _open_forge_window(self, to_forge: list[dict], auto_confirm: bool):
        """Live forge progress window with log and Stop button."""
        import datetime

        win = _safe_toplevel(self)
        win.title("Forging…")
        win.geometry("780x480")

        total_forges = sum(c["forgeable"] for c in to_forge)
        ctk.CTkLabel(win,
                     text=f"Running {total_forges} real forge(s) — DO NOT close this window",
                     font=("Arial", 13, "bold"), text_color="#e05050",
                     ).pack(pady=(14, 2))

        log_box = ctk.CTkTextbox(win, font=("Consolas", 14), state="disabled")
        log_box.pack(fill="both", expand=True, padx=14, pady=(4, 4))

        # Log file so output is never lost
        log_path = LOG_DIR / f"forge_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
        log_file  = open(log_path, "w", encoding="utf-8")

        stop_event = threading.Event()

        def _log(msg: str):
            ts = time.strftime("%H:%M:%S")
            line = f"[{ts}] {msg}"
            try:
                if not log_file.closed:
                    log_file.write(line + "\n"); log_file.flush()
            except Exception:
                pass
            try:                              # window may have been closed
                log_box.configure(state="normal")
                log_box.insert("end", line + "\n")
                log_box.see("end")
                log_box.configure(state="disabled")
            except Exception:
                pass
            self.after(0, lambda m=msg: self._status(m))

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=(0, 12))

        def _stop():
            stop_event.set()
            btn_stop.configure(state="disabled", text="Stopping…")
            _log("Stop requested — will halt after the current forge completes.")

        def _on_done():
            # Re-enable the main Forge button FIRST so it can NEVER get stuck
            # disabled — even if the forging window was already closed (its
            # widgets would then be dead and configuring them would throw).
            try:
                self.btn_forge.configure(state="normal")
            except Exception:
                pass
            try:
                _log(f"Log saved to: {log_path}")
            except Exception:
                pass
            try:
                log_file.close()
            except Exception:
                pass
            for w, kw in ((btn_stop, {"state": "disabled"}),
                          (btn_close, {"state": "normal"})):
                try:
                    w.configure(**kw)
                except Exception:
                    pass
            self._dbg("FORGE_DONE -> clear recipes")
            self._recipes.clear()        # forged cards are consumed; start fresh
            try:
                self._refresh_queue()
            except Exception:
                pass
            self.after(500, lambda: self._refresh_async(force_floor_scan=True))

        btn_stop = ctk.CTkButton(btn_frame, text="⏹  Stop", width=120,
                                 fg_color="#8b0000", hover_color="#c00000",
                                 command=_stop)
        btn_stop.grid(row=0, column=0, padx=8)

        btn_close = ctk.CTkButton(btn_frame, text="Close", width=100,
                                  fg_color="#333", hover_color="#555",
                                  command=win.destroy, state="disabled")
        btn_close.grid(row=0, column=1, padx=8)

        self.btn_forge.configure(state="disabled")
        _log(f"Forge log: {log_path}")

        threading.Thread(
            target=self._run_forges,
            args=(to_forge, auto_confirm, False, _log, _on_done, stop_event),
            daemon=True,
        ).start()

    def _forge_summary(self, card: dict) -> dict:
        """Per-card cost summary (sums every combine op in the card's recipe)."""
        g_cost = card.get("gods_cost", 0)
        ops    = card.get("combine_ops") or []
        total_forges = cards_used = 0
        descs = []
        for op in ops:
            tgt, contribute = op["target"], op["contribute"]
            yld, _lo = forge_api.combine_yield(tgt, contribute)
            total_forges += self._combine_forges(tgt, contribute)
            cards_used   += sum(contribute.values())
            src = " + ".join(f"{n} {self._QUAL_SHORT.get(t, t)}"
                             for t, n in contribute.items())
            descs.append(f"{yld}× {tgt} ({src})")
        return {"name": card.get("name"), "desc": "  +  ".join(descs) or "—",
                "is_chain": total_forges > len(ops), "cards_used": cards_used,
                "gods": total_forges * g_cost,
                "profit": None}   # profit across mixed sources is ambiguous; omitted

    def _open_dry_run_window(self, to_forge: list[dict]):
        win = _safe_toplevel(self)
        win.title("Dry Run — Forge Plan")
        win.geometry("780x600")
        win.grab_set()

        # ── Header ────────────────────────────────────────────────────────────
        ctk.CTkLabel(win, text="Dry Run — no real transactions will happen",
                     font=("Arial", 13, "bold"), text_color="#e0a000").pack(pady=(14, 2))

        # ── Summary table ─────────────────────────────────────────────────────
        tframe = ctk.CTkScrollableFrame(win, height=220)
        tframe.pack(fill="x", padx=14, pady=(6, 0))

        eth_usd = self._eth_usd or 0.0
        gods_eth = self._gods_eth or 0.0

        headers = ["Card", "Makes", "Cards used", "GODS"]
        widths  = [200, 280, 90, 70]
        for ci, (h, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(tframe, text=h, width=w, anchor="w",
                         font=("Arial", 10, "bold"), text_color="#aaa").grid(
                row=0, column=ci, padx=3, pady=3, sticky="w")

        total_gods = 0.0
        for ri, card in enumerate(to_forge, start=1):
            s = self._forge_summary(card)
            total_gods += s["gods"]
            row_vals = [
                (s["name"],                  "white"),
                (s["desc"],                  "#f0c000" if s["is_chain"] else "#cfd2dc"),
                (str(s["cards_used"]),       "white"),
                (f"{s['gods']:.1f}",         "#e0c050"),
            ]
            for ci, (txt, col) in enumerate(row_vals):
                ctk.CTkLabel(tframe, text=txt, width=widths[ci], anchor="w",
                             text_color=col, font=("Arial", 11), wraplength=widths[ci]).grid(
                    row=ri, column=ci, padx=3, pady=1, sticky="w")

        # ── Totals ────────────────────────────────────────────────────────────
        tot_frame = ctk.CTkFrame(win, fg_color="#1a1a2e", corner_radius=6)
        tot_frame.pack(fill="x", padx=14, pady=6)
        gods_usd = total_gods * gods_eth * eth_usd
        ctk.CTkLabel(tot_frame,
                     text=f"GODS to spend: {total_gods:.1f}  (≈ ${gods_usd:.2f})",
                     font=("Arial", 11, "bold"), text_color="#e0c050",
                     ).pack(padx=12, pady=8)

        # ── Live log ──────────────────────────────────────────────────────────
        ctk.CTkLabel(win, text="Simulation log:", font=("Arial", 10, "bold"),
                     text_color="#aaa").pack(anchor="w", padx=14)
        log_box = ctk.CTkTextbox(win, height=160, font=("Consolas", 14), state="disabled")
        log_box.pack(fill="both", expand=True, padx=14, pady=(2, 6))

        def _log(msg: str):
            try:
                log_box.configure(state="normal")
                log_box.insert("end", msg + "\n")
                log_box.see("end")
                log_box.configure(state="disabled")
            except Exception:
                pass

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=(0, 12))

        def _dry_done():
            try:
                self.btn_forge.configure(state="normal")   # main button FIRST
            except Exception:
                pass
            for w in (btn_run, btn_close):
                try:
                    w.configure(state="normal")
                except Exception:
                    pass

        def _run_dry():
            btn_run.configure(state="disabled")
            btn_close.configure(state="disabled")
            self.btn_forge.configure(state="disabled")
            threading.Thread(
                target=self._run_forges,
                args=(to_forge, False, True, _log, _dry_done),
                daemon=True,
            ).start()

        btn_run = ctk.CTkButton(btn_frame, text="▶  Run Simulation",
                                command=_run_dry, width=160)
        btn_run.grid(row=0, column=0, padx=8)

        btn_close = ctk.CTkButton(btn_frame, text="Close", width=100,
                                  fg_color="#333", hover_color="#555",
                                  command=win.destroy)
        btn_close.grid(row=0, column=1, padx=8)

    def _run_forges(self, to_forge: list[dict], auto_confirm: bool, dry_run: bool,
                    log_cb=None, done_cb=None, stop_event: threading.Event = None):
        def _log(msg: str):
            if log_cb:
                log_cb(msg)   # already marshalled to main thread by _open_forge_window
            else:
                self.after(0, lambda m=msg: self._status(m))

        use_api = forge_api.api_mode_available() and not dry_run

        if use_api:
            _log("=== API mode: direct on-chain GODS payments ===")

        # Everything runs in a try/finally so the Forge button is ALWAYS
        # re-enabled (done_cb), even if a forge throws an unexpected error.
        try:
            for card in to_forge:
                if stop_event and stop_event.is_set():
                    _log("Stopped by user.")
                    break

                name = card["name"]
                q    = card["quality"]
                ops  = card.get("combine_ops") or []
                plan_desc = ", ".join(
                    f"{forge_api.combine_yield(o['target'], o['contribute'])[0]}×{o['target']}"
                    for o in ops) or "—"
                _log(f"{'[DRY RUN] ' if dry_run else ''}Forging {name}: {plan_desc}")

                # Catch BROADLY (not just ForgeApiError) so a web3/RPC/network
                # error in one card is logged and we move on — never killing the
                # worker thread (which would leave the button stuck disabled).
                try:
                    if use_api and ops:
                        receipts = forge_api.forge_combine_plan(
                            card["proto"], ops, log=_log, stop_event=stop_event)
                        results = [True] * len(receipts)
                    elif use_api:
                        receipts = forge_api.forge_by_proto_quality(
                            proto=card["proto"], quality=q,
                            count=card.get("forgeable", 1),
                            ratio=forge_ratio(q), log=_log,
                            stop_event=stop_event, asset_ids=card.get("asset_ids"))
                        results = [True] * len(receipts)
                    else:
                        results = forge_card(
                            proto=card["proto"], card_name=name, quality=q,
                            forge_count=card.get("forgeable", 1),
                            auto_confirm=auto_confirm, dry_run=dry_run, status_cb=_log)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    _log(f"❌ Forge error for {name}: {e}")
                    results = [False]

                _log(f"  Done: {len(results)} forge(s).\n")

                if not dry_run:
                    invalidate_floor(card["proto"], card["quality"])
                    if card.get("next_quality"):
                        invalidate_floor(card["proto"], card.get("next_quality"))
        finally:
            if done_cb:
                self.after(0, done_cb)

    # ── Settings / Costs dialog ───────────────────────────────────────────────

    def _open_costs_dialog(self):
        win = _safe_toplevel(self)
        win.title("GODS Forge Costs")
        win.geometry("620x560")
        win.grab_set()

        ctk.CTkLabel(win, text="GODS tokens per forge (by rarity × from-quality)",
                     font=("Arial", 13, "bold")).pack(pady=(14, 2))
        ctk.CTkLabel(
            win,
            text="⚠  Verify these values in-game — they may have changed!",
            text_color="#e0a000",
        ).pack(pady=(0, 8))

        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=16, pady=8)

        entries: dict[str, ctk.CTkEntry] = {}
        custom = self.settings.get("gods_costs", DEFAULT_GODS_COSTS)
        rarities = ["common", "rare", "epic", "legendary", "mythic"]

        ctk.CTkLabel(frame, text="Rarity", width=120, font=("Arial", 10, "bold"),
                     text_color="#aaa").grid(row=0, column=0, padx=8, pady=4)
        ctk.CTkLabel(frame, text="GODS per forge", width=130, font=("Arial", 10, "bold"),
                     text_color="#aaa").grid(row=0, column=1, padx=8, pady=4)

        for ri, rarity in enumerate(rarities, start=1):
            ctk.CTkLabel(frame, text=rarity.capitalize(), width=120,
                         anchor="e", font=("Arial", 11, "bold")).grid(
                row=ri, column=0, padx=8, pady=6, sticky="e")
            val = custom.get(rarity, DEFAULT_GODS_COSTS.get(rarity, 0))
            e = ctk.CTkEntry(frame, width=120)
            e.insert(0, str(val))
            e.grid(row=ri, column=1, padx=8, pady=6)
            entries[rarity] = e

        def _save():
            new_costs = {}
            for rarity, e in entries.items():
                try:
                    new_costs[rarity] = float(e.get())
                except ValueError:
                    pass
            self.settings["gods_costs"] = new_costs
            save_settings(self.settings)
            win.destroy()
            self.after(100, self._refresh_async)

        ctk.CTkButton(win, text="Save & Refresh", command=_save).pack(pady=12)

    def _save_settings(self):
        self.settings["auto_confirm"]   = self.var_auto_confirm.get()
        self.settings["dry_run"]        = self.var_dry_run.get()
        try:
            self.settings["min_profit_eth"] = float(self.var_min_profit.get())
        except ValueError:
            pass
        save_settings(self.settings)

    def _status(self, msg: str):
        self.lbl_status.configure(text=msg)


if __name__ == "__main__":
    app = ForgeApp()
    app.mainloop()
