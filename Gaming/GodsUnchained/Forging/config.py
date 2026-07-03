import json
import os
from pathlib import Path

# Wallet credentials are read from a local .env file placed NEXT TO this app
# (see .env.example).  Copy .env.example to .env and fill in your own values.
# Environment variables already set in the shell take precedence over the file.
_ENV = Path(__file__).parent / ".env"
if _ENV.exists():
    with open(_ENV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "").lower()

# Private key for no-launcher (API mode) forging.  Put "PRIVATE_KEY=0x…" in the
# .env file next to WALLET_ADDRESS.  If absent, the app falls back to the
# launcher-automation flow.
#
# WARNING: this is a hot-wallet pattern.  Use a DEDICATED forging wallet funded
# only with enough GODS for your planned forges.  Never put the private key for
# a wallet holding significant value on disk.
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

# ── Immutable / GU API ────────────────────────────────────────────────────────
IMMUTABLE_API = "https://api.immutable.com/v1/chains/imtbl-zkevm-mainnet"
GU_API        = "https://api.godsunchained.com/v0"
GU_CONTRACT   = "0x06d92b637dfcdf95a2faba04ef22b2a096029b69"
ETH_CONTRACT  = "0x52a6c53869ce09a731cd772f245b97a4401d3348"
GODS_CONTRACT = "0xe0e0981d19ef2e0a57cc48ca60d9454ed2d53feb"

# Marketplace fee by OUTPUT quality (deducted from sale revenue)
MARKETPLACE_FEES = {
    "Meteorite": 0.09,
    "Shadow":    0.08,
    "Gold":      0.07,
    "Diamond":   0.06,
}
MARKETPLACE_FEE = 0.09   # fallback

# ── Forging ───────────────────────────────────────────────────────────────────
QUALITIES = ["Plain", "Meteorite", "Shadow", "Gold", "Diamond"]

# Cards needed per forge, by FROM quality
FORGE_RATIOS = {
    "Plain":     2,   # 2 Plain     → 1 Meteorite
    "Meteorite": 5,   # 5 Meteorite → 1 Shadow
    "Shadow":    5,   # 5 Shadow    → 1 Gold
    "Gold":      5,   # 5 Gold      → 1 Diamond
}

# GODS cost per single forge, by rarity (same regardless of quality level)
DEFAULT_GODS_COSTS = {
    "common":    0.1,
    "rare":      0.3,
    "epic":      0.7,
    "legendary": 1.5,
    "mythic":    1.5,   # not shown in image — using legendary value until confirmed
}

# ── Launcher / automation ─────────────────────────────────────────────────────
# Path to the Immutable / Gods Unchained desktop launcher.  Auto-detected for the
# current Windows user; override with the GU_LAUNCHER_EXE environment variable if
# yours is installed elsewhere.  (Only used by the legacy launcher flow — API
# mode, with a PRIVATE_KEY in .env, does not need the launcher at all.)
LAUNCHER_EXE  = os.getenv(
    "GU_LAUNCHER_EXE",
    str(Path.home() / "AppData/Local/Programs/immutable-launcher/Gods Unchained.exe"))
LAUNCHER_URL  = "https://master.desktop.godsunchained.com"
FORGE_PATH    = "/#/game/gu/forge"   # SPA hash route — launcher uses nested /game/gu/…
DEBUG_PORT    = 9222

# ── GU backend (captured from live launcher traffic) ──────────────────────────
# apollo-auth: exchanges the launcher's refresh token for a short-lived Bearer.
# fusing: the forge API — POST /forge/validation and POST /forge.
# marketplace-legacy: user's asset list with GU internal asset IDs (what /forge
# wants in its asset_id array — NOT the same as zkEVM token IDs).
GU_APOLLO_AUTH_URL       = "https://apollo-auth.prod.prod.godsunchained.com/auth2?type=refresh"
GU_FUSING_VALIDATION_URL = "https://fusing.prod.prod.godsunchained.com/forge/validation"
GU_FUSING_FORGE_URL      = "https://fusing.prod.prod.godsunchained.com/forge"
GU_LEGACY_ASSETS_URL     = "https://marketplace-legacy.prod.prod.godsunchained.com/v2/asset"

# ── zkEVM chain ───────────────────────────────────────────────────────────────
ZKEVM_RPC     = "https://rpc.immutable.com"
ZKEVM_CHAIN_ID = 13371

# ── Persistence (all kept inside the app folder) ──────────────────────────────
SETTINGS_FILE = Path(__file__).parent / "settings.json"
TOKEN_CACHE   = Path(__file__).parent / "token_proto_cache.json"


def load_settings() -> dict:
    defaults = {
        "auto_confirm":   False,
        "dry_run":        True,
        "min_profit_eth": 0.0,
        "gods_costs":     DEFAULT_GODS_COSTS,
    }
    if SETTINGS_FILE.exists():
        try:
            saved = json.loads(SETTINGS_FILE.read_text())
            defaults.update(saved)
        except Exception:
            pass
    return defaults


def save_settings(s: dict):
    SETTINGS_FILE.write_text(json.dumps(s, indent=2))
