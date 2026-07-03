═══════════════════════════════════════════════════════════
  GU BOT — Gods Unchained marketplace auto-lister
═══════════════════════════════════════════════════════════

Automatically lists the cards in your wallet on the Immutable zkEVM
marketplace at the cheapest competitive price, and re-prices them as
the market moves. Runs in a simple desktop app — no coding needed.


───────────────────────────────────────────────────────────
  1. INSTALL
───────────────────────────────────────────────────────────

  • Double-click  GU-Bot-Setup-1.0.11.exe

  • Windows may show a blue "Windows protected your PC" box
    (because the app isn't code-signed). This is normal for
    indie software. Click:

        More info  →  Run anyway

  • Follow the installer. It creates a Start Menu shortcut and a
    Desktop shortcut called "GU Bot".


───────────────────────────────────────────────────────────
  2. SET UP YOUR WALLET  (do this first)
───────────────────────────────────────────────────────────

  ⚠  USE A DEDICATED "BURNER" WALLET — never your main one.
      Put only the cards you want to sell + a small amount of
      IMX/ETH for gas fees into it.

  In the app:
    • Open the "Wallet" tab
    • Paste your wallet address (0x...)
    • Paste that wallet's private key
    • Click "Save wallet"

  Your credentials are stored ONLY on your own computer, in:
      %APPDATA%\gu-bot-ui\bot\.env
  They are never uploaded anywhere.


───────────────────────────────────────────────────────────
  3. (OPTIONAL) ADJUST SETTINGS
───────────────────────────────────────────────────────────

  The "Settings" tab controls how the bot prices your cards.
  The defaults are sensible — you can leave them as-is.

  Key settings:
    • Qualities / Sets     — which cards the bot lists
    • Dump protection      — refuses to list far below recent sales
    • Relist threshold     — how much the market must move before re-pricing
    • Cycle intervals      — how often it scans (default: daily + 30 min for new set)
    • Aggressive undercut  — always be cheapest, with a safety floor
    • Whitelisted wallets  — wallets the bot won't try to undercut

  Click "Save settings" after any change, then restart the bot.


───────────────────────────────────────────────────────────
  4. RUN
───────────────────────────────────────────────────────────

  • Open the "Run" tab
  • Click "▶ Start bot"
  • Watch the live log. Leave the window open while it runs.

  Buttons:
    ▶ Start   — starts the bot (does a full market scan first, ~5 min)
    ⏸ Pause   — pauses after the current cycle; Resume continues instantly
    ■ Stop    — stops the bot completely

  The bot loops on the schedule you set in Settings. You can just
  leave it running.


───────────────────────────────────────────────────────────
  TROUBLESHOOTING
───────────────────────────────────────────────────────────

  • "Wallet not configured" when starting
        → Fill in the Wallet tab first.

  • Antivirus flags the installer
        → False positive on bundled software. Add an exception.

  • See the full log
        → Run tab → "Open bot.log"

  • Inspect your settings/wallet files
        → Run tab → "Open bot folder"


───────────────────────────────────────────────────────────
  SAFETY
───────────────────────────────────────────────────────────

  • Burner wallet only. If your computer is ever compromised, the
    most anyone can take is what's in that one wallet.
  • The bot only LISTS cards for sale — it never buys, transfers,
    or moves funds out of your wallet.
  • Everything runs locally on your machine.

═══════════════════════════════════════════════════════════
