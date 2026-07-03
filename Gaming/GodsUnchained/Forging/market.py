"""Market data: inventory, floor prices, token prices."""
import base64
import json
import time
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import requests

from config import (
    IMMUTABLE_API, GU_API, GU_CONTRACT, ETH_CONTRACT,
    WALLET_ADDRESS, TOKEN_CACHE, GU_APOLLO_AUTH_URL, GU_LEGACY_ASSETS_URL,
)

# ── GU launcher config.json (Electron userData) ───────────────────────────────
_LAUNCHER_CONFIG = Path.home() / "AppData/Roaming/immutable-launcher/config.json"

# Our own cache, so we survive the launcher clearing its credentials on close.
# Once we've seen a refresh token (while the launcher was running at least
# once), we keep a copy here and never need the launcher again.
_TOKEN_CACHE = Path(__file__).parent / "gu_token_cache.json"

# Real refresh endpoint confirmed from launcher traffic + the old FasterForge
# decompile.  The generic api.godsunchained.com URLs kept here as fallback.
_REFRESH_URLS = [
    GU_APOLLO_AUTH_URL,
    "https://api.godsunchained.com/v1/auth/token/refresh",
    "https://api.godsunchained.com/v0/auth/refresh",
    "https://api.godsunchained.com/v1/auth/refresh",
]


def _read_token_cache() -> dict:
    try:
        return json.loads(_TOKEN_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_token_cache(data: dict):
    try:
        _TOKEN_CACHE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def _decode_jwt_exp(token: str) -> Optional[int]:
    """Extract expiry timestamp from JWT payload without verifying signature."""
    try:
        payload_b64 = token.split(".")[1]
        # Add padding
        payload_b64 += "=" * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return payload.get("exp")
    except Exception:
        return None


def _read_launcher_config() -> dict:
    try:
        return json.loads(_LAUNCHER_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_launcher_config(data: dict):
    try:
        _LAUNCHER_CONFIG.write_text(json.dumps(data, indent="\t"), encoding="utf-8")
    except Exception:
        pass


def _try_refresh(refresh_token: str) -> Optional[tuple[str, str]]:
    """
    Try each known refresh endpoint. Returns (new_access, new_refresh) on success,
    or None if every endpoint failed.
    """
    for url in _REFRESH_URLS:
        try:
            r = requests.post(
                url,
                json={"refresh": refresh_token, "refresh_token": refresh_token},
                timeout=10,
            )
            if r.ok:
                data = r.json()
                new_access  = (data.get("access") or data.get("access_token")
                               or data.get("token") or data.get("jwt"))
                new_refresh = (data.get("refresh") or data.get("refresh_token")
                               or refresh_token)
                if new_access:
                    return new_access, new_refresh
        except Exception:
            continue
    return None


def _read_credentials() -> tuple[Optional[str], Optional[str]]:
    """
    Returns (access, refresh) preferring the live launcher config when it's
    populated, falling back to our own on-disk cache if the launcher has been
    closed (which clears the launcher's credentials).
    """
    cfg   = _read_launcher_config()
    creds = cfg.get("credentials") or {}
    access  = creds.get("access")  or None
    refresh = creds.get("refresh") or None

    if not (access or refresh):
        cache = _read_token_cache()
        access  = access  or cache.get("access")
        refresh = refresh or cache.get("refresh")
    return access, refresh


def _persist_credentials(access: str, refresh: str):
    """
    Write tokens both to our own cache (always) and — if the launcher file is
    still populated — back to the launcher config too, so both stay in sync.
    """
    _write_token_cache({"access": access, "refresh": refresh})

    cfg = _read_launcher_config()
    creds = cfg.get("credentials")
    # Only rewrite launcher config if it has a populated credentials block
    # already.  If the launcher wiped it, leave it wiped — that's the launcher's
    # business, not ours.
    if isinstance(creds, dict) and (creds.get("refresh") or creds.get("access")):
        creds["access"]  = access
        creds["refresh"] = refresh
        cfg["credentials"] = creds
        _write_launcher_config(cfg)


def get_gu_auth_token() -> Optional[str]:
    """
    Returns a valid GU access token, auto-refreshing if expired.

    Source priority:
      1. Live launcher config.json (if the launcher is running / just ran).
      2. Our own on-disk cache (seeded from the launcher the first time we
         saw a real token — survives launcher shutdowns).

    To bootstrap from scratch, open the launcher once.  After that you can
    close it forever and the cached refresh token will keep working.
    """
    access, refresh = _read_credentials()
    if not (access or refresh):
        return None

    exp = _decode_jwt_exp(access) if access else None
    # If the access token is still fresh (more than 60 s left), just use it.
    if access and exp and time.time() < exp - 60:
        # Opportunistically seed cache so later launcher shutdowns don't lock us out
        if refresh:
            _write_token_cache({"access": access, "refresh": refresh})
        return access

    # Otherwise refresh.
    if refresh:
        pair = _try_refresh(refresh)
        if pair:
            new_access, new_refresh = pair
            _persist_credentials(new_access, new_refresh)
            return new_access

    # Refresh failed — return whatever we had, caller will see a 401 if stale.
    return access

_session = requests.Session()
_session.headers.update({"Accept": "application/json"})

_meta_cache:   dict[int, Optional[dict]] = {}
_floor_cache:  dict[tuple, tuple]        = {}   # (proto, quality) → (price_eth, ts)
_eth_usd:      tuple = (None, 0)
_gods_eth:     tuple = (None, 0)

FLOOR_TTL  = 5 * 60
PRICE_TTL  = 5 * 60
MIN_DUST   = 1e-7   # ignore listings below this ETH value


def _get(url: str, retries: int = 4) -> Optional[dict]:
    for i in range(retries):
        try:
            r = _session.get(url, timeout=15)
            if r.status_code == 429:
                time.sleep(2 ** i)
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if i == retries - 1:
                return None
            time.sleep(1 + i)
    return None


# ── Token prices ──────────────────────────────────────────────────────────────

def get_eth_usd() -> Optional[float]:
    global _eth_usd
    price, ts = _eth_usd
    if price and time.time() - ts < PRICE_TTL:
        return price
    r = _get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    if r and r.get("price"):
        _eth_usd = (float(r["price"]), time.time())
    return _eth_usd[0]


def get_gods_eth() -> Optional[float]:
    """Returns GODS price denominated in ETH."""
    global _gods_eth
    price, ts = _gods_eth
    if price and time.time() - ts < PRICE_TTL:
        return price
    try:
        gr = _get("https://api.coinbase.com/v2/prices/GODS-USD/spot")
        er = _get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
        if gr and er:
            gods_usd = float(gr["data"]["amount"])
            eth_usd  = float(er["data"]["amount"])
            _gods_eth = (gods_usd / eth_usd, time.time())
    except Exception:
        pass
    return _gods_eth[0]


# ── Card metadata ─────────────────────────────────────────────────────────────

def get_card_meta(proto: int) -> Optional[dict]:
    if proto in _meta_cache:
        return _meta_cache[proto]
    r = _get(f"{GU_API}/proto/{proto}")
    if not r or not r.get("name"):
        _meta_cache[proto] = None
        return None
    meta = {
        "name":   r.get("name", f"proto:{proto}"),
        "rarity": (r.get("rarity") or "common").lower(),
        "set":    (r.get("set") or "").lower(),
    }
    _meta_cache[proto] = meta
    return meta


def _decode_user_id_from_jwt(token: str) -> Optional[int]:
    try:
        payload = token.split(".")[1]
        payload += "=" * (4 - len(payload) % 4)
        return int(json.loads(base64.urlsafe_b64decode(payload)).get("id"))
    except Exception:
        return None


def fetch_ingame_plain_cards(wallet: str = WALLET_ADDRESS) -> list[dict]:
    """
    Fetch in-game Plain cards via GU's legacy marketplace API.

    Returns [{proto, quality:"Plain", count, asset_ids:[…]}, …].  asset_ids
    are the GU legacy asset IDs — forge_api needs them to POST /forge, so
    we surface them here and avoid re-fetching the same 3 MB response twice.

    Requires a working refresh token either in the launcher config or the
    on-disk cache.  Raises RuntimeError if neither is available.
    """
    token = get_gu_auth_token()
    if not token:
        raise RuntimeError(
            "No GU auth token — open the launcher once so we can cache your "
            "refresh token.  After that you can close it forever."
        )

    user_id = _decode_user_id_from_jwt(token)
    if not user_id:
        raise RuntimeError("Could not decode GU user_id from access token.")

    last_err = None
    for attempt in range(10):
        if attempt:
            wait = min(2 ** attempt, 60)
            time.sleep(wait)
        r = requests.get(
            GU_LEGACY_ASSETS_URL,
            params={"type": "card", "user_id": user_id},
            headers={"Authorization": f"Bearer {token}"},
            timeout=120,
        )
        if r.status_code == 401:
            raise RuntimeError("GU auth token rejected (401) — refresh token may have expired.")
        if r.ok:
            break
        last_err = f"{r.status_code}: {r.text[:200]}"
        if r.status_code < 500:
            raise RuntimeError(f"Legacy marketplace error: {last_err}")
    else:
        raise RuntimeError(f"Legacy marketplace still failing after 10 attempts: {last_err}")
    data = r.json()

    # Shape: {"protos": {"<proto>": {"assets": [{id, minting_status, properties:{quality}}]}}}
    protos = data.get("protos") or {}
    grouped: dict[int, list[int]] = {}
    for proto_str, pd in protos.items():
        try:
            proto_id = int(proto_str)
        except ValueError:
            continue
        for a in (pd.get("assets") or []):
            props  = a.get("properties") or {}
            # quality 5 = Plain; only off_chain = still in-game (unminted)
            if props.get("quality") != 5:
                continue
            if a.get("minting_status") != "off_chain":
                continue
            aid = a.get("id")
            if aid is not None:
                grouped.setdefault(proto_id, []).append(int(aid))

    return [
        {"proto": proto, "quality": "Plain", "count": len(ids), "asset_ids": ids}
        for proto, ids in grouped.items()
    ]


def prefetch_card_meta(protos: list[int], workers: int = 12) -> None:
    """Parallel metadata fetch — populates cache for all protos at once."""
    from concurrent.futures import ThreadPoolExecutor
    missing = [p for p in protos if p not in _meta_cache]
    if not missing:
        return
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(get_card_meta, missing))


# ── Owned inventory ───────────────────────────────────────────────────────────

def fetch_owned_nfts(wallet: str = WALLET_ADDRESS) -> list[dict]:
    """Returns [{token_id, proto, quality, set}, ...]."""
    nfts, cursor = [], None
    while True:
        url = (f"{IMMUTABLE_API}/accounts/{wallet}/nfts"
               f"?contract_address={GU_CONTRACT}&page_size=200"
               + (f"&page_cursor={cursor}" if cursor else ""))
        r = _get(url)
        if not r or not r.get("result"):
            break
        for nft in r["result"]:
            attrs = {a["trait_type"]: a["value"] for a in (nft.get("attributes") or [])}
            proto = attrs.get("Proto")
            if not proto:
                continue
            nfts.append({
                "token_id": nft["token_id"],
                "proto":    int(proto),
                "quality":  attrs.get("Quality", ""),
                "set":      (attrs.get("Set") or "").lower(),
            })
        cursor = (r.get("page") or {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.15)
    return nfts


# ── Floor prices ──────────────────────────────────────────────────────────────

# Disk cache for the full floor scan — the scan itself is expensive (iterates
# every active ETH listing on the marketplace), so we persist results and
# reuse them for up to an hour between app opens.
_FLOOR_DISK_CACHE = Path(__file__).parent / "floor_cache.json"
FLOOR_DISK_TTL    = 60 * 60   # 1 hour


def load_cached_floors(max_age_sec: int = FLOOR_DISK_TTL) -> Optional[dict[tuple, float]]:
    """
    Returns the most recent floor scan result if it's younger than
    `max_age_sec`, otherwise None.  Keys are (proto, quality) tuples and match
    the shape returned by scan_all_floor_prices.
    """
    if not _FLOOR_DISK_CACHE.exists():
        return None
    try:
        payload = json.loads(_FLOOR_DISK_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return None
    ts = payload.get("timestamp", 0)
    if time.time() - ts > max_age_sec:
        return None
    floors_json = payload.get("floors") or {}
    # JSON keys are strings, convert back to (proto:int, quality:str) tuples
    floors: dict[tuple, float] = {}
    for k, v in floors_json.items():
        try:
            proto_str, quality = k.split("|", 1)
            floors[(int(proto_str), quality)] = float(v)
        except Exception:
            continue
    # Seed the in-memory TTL cache so single-card fetch_floor_price calls also
    # benefit (until its own 5-min TTL forces a refresh).
    now = time.time()
    for key, price in floors.items():
        _floor_cache[key] = (price, now)
    return floors


def save_floor_cache(floors: dict[tuple, float]) -> None:
    """Persists a full scan result to disk for next app open."""
    try:
        floors_json = {f"{p}|{q}": v for (p, q), v in floors.items()}
        _FLOOR_DISK_CACHE.write_text(
            json.dumps({"timestamp": time.time(), "floors": floors_json}),
            encoding="utf-8",
        )
    except Exception:
        pass


def floor_cache_age_sec() -> Optional[float]:
    """Age of the on-disk floor cache in seconds, or None if no cache exists."""
    if not _FLOOR_DISK_CACHE.exists():
        return None
    try:
        payload = json.loads(_FLOOR_DISK_CACHE.read_text(encoding="utf-8"))
        ts = payload.get("timestamp", 0)
        return max(0.0, time.time() - ts)
    except Exception:
        return None


def scan_all_floor_prices(
    owned_keys: set[tuple],
    progress_cb=None,
) -> dict[tuple, float]:
    """
    Single-pass global scan of all active ETH listings.
    Returns {(proto, quality): floor_price_eth} for every proto+quality in owned_keys.
    Uses token_proto_cache.json to map token_id → proto+quality.
    Much faster than per-card API calls for large inventories.
    """
    # Load token→proto+quality mapping from disk cache
    token_map: dict[str, dict] = {}
    if TOKEN_CACHE.exists():
        try:
            data = json.loads(TOKEN_CACHE.read_text())
            token_map = data.get("tokens") or {}
        except Exception:
            pass

    floors: dict[tuple, float] = {}
    cursor = None
    page_n = 0
    found  = 0

    while True:
        url = (f"{IMMUTABLE_API}/orders/listings"
               f"?sell_item_contract_address={GU_CONTRACT}"
               f"&buy_item_contract_address={ETH_CONTRACT}"
               f"&status=ACTIVE"
               f"&order_by=buy_item_amount&direction=asc"
               f"&page_size=200"
               + (f"&page_cursor={quote(cursor)}" if cursor else ""))
        r = _get(url)
        if not r or not r.get("result"):
            break

        page_n += 1
        if progress_cb:
            progress_cb(page_n, found)

        for listing in r["result"]:
            sell = listing.get("sell") or []
            tid  = (sell[0].get("token_id") if isinstance(sell, list) and sell
                    else (sell or {}).get("token_id"))
            buy  = listing.get("buy") or []
            amt  = (buy[0].get("amount") if isinstance(buy, list) and buy
                    else (buy or {}).get("amount"))
            if not tid or not amt:
                continue

            entry = token_map.get(str(tid))
            if not entry:
                continue
            proto   = entry.get("proto")
            quality = entry.get("quality")
            if not proto or not quality:
                continue

            key = (proto, quality)
            # Only store the cheapest price per key (listings are already sorted asc)
            if key not in floors:
                price_eth = int(amt) / 1e18
                if price_eth >= MIN_DUST:
                    floors[key] = price_eth
                    _floor_cache[key] = (price_eth, time.time())
                    if key in owned_keys:
                        found += 1

        cursor = (r.get("page") or {}).get("next_cursor")
        if not cursor:
            break

        # Stop early once we have a floor for every key we care about
        if owned_keys and owned_keys.issubset(floors.keys()):
            break

        time.sleep(0.12)

    # Persist so the next app open can skip this scan entirely for up to an hour
    save_floor_cache(floors)
    return floors


def fetch_floor_price(proto: int, quality: str) -> Optional[float]:
    """Cheapest active ETH listing for proto+quality (single-card fallback)."""
    key = (proto, quality)
    cached = _floor_cache.get(key)
    if cached:
        price, ts = cached
        if time.time() - ts < FLOOR_TTL:
            return price

    meta_filter = {"proto": [str(proto)], "quality": [quality]}
    url = (f"{IMMUTABLE_API}/orders/listings"
           f"?sell_item_contract_address={GU_CONTRACT}"
           f"&sell_item_metadata_filter={quote(json.dumps(meta_filter))}"
           f"&buy_item_contract_address={ETH_CONTRACT}"
           f"&status=ACTIVE"
           f"&sort_by=buy_item_amount&sort_direction=asc"
           f"&page_size=10")
    r = _get(url)
    if r and r.get("result"):
        for listing in r["result"]:
            buy = listing.get("buy") or []
            amt = (buy[0].get("amount") if isinstance(buy, list) and buy
                   else (buy or {}).get("amount"))
            if not amt:
                continue
            price_eth = int(amt) / 1e18
            if price_eth >= MIN_DUST:
                _floor_cache[key] = (price_eth, time.time())
                return price_eth

    _floor_cache[key] = (None, time.time())
    return None


def _quality_from_cache(token_id: Optional[str]) -> Optional[str]:
    if not token_id or not TOKEN_CACHE.exists():
        return None
    try:
        data = json.loads(TOKEN_CACHE.read_text())
        entry = (data.get("tokens") or {}).get(token_id)
        return entry.get("quality") if isinstance(entry, dict) else None
    except Exception:
        return None


def invalidate_floor(proto: int, quality: str):
    _floor_cache.pop((proto, quality), None)
