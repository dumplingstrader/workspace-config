"""
Launcher-free forging via GU's own HTTP API + a direct on-chain GODS payment.

Flow (reverse-engineered from launcher traffic):

  1. Read refresh token from the launcher's config.json on disk.
  2. Exchange it for a short-lived Bearer via apollo-auth (market.get_gu_auth_token).
  3. Fetch the user's in-game Plain cards from GU's legacy marketplace API —
     this returns the *GU internal asset IDs* that /forge expects (NOT zkEVM
     token IDs).
  4. For each forge:
        POST /forge/validation  → {flux_amount, token_amount}
        POST /forge             → full receipt with token_payment_address
        Sign + broadcast:  GODS.transfer(token_payment_address, token_amount)
     GU's backend listens to the chain and completes the forge automatically
     once the ERC20 transfer confirms.  No launcher window, no MetaMask popup,
     no clicks.

SAFETY — HOT WALLET
  The private key lives in .env as PRIVATE_KEY=0x…  Use a dedicated
  forging wallet funded with only as much GODS + gas as you intend to spend.
  Never put a key controlling significant value on disk.
"""
from __future__ import annotations

import base64
import json
import time
from typing import Callable, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from eth_account import Account
from web3 import Web3

from config import (
    GU_FUSING_VALIDATION_URL,
    GU_FUSING_FORGE_URL,
    GU_LEGACY_ASSETS_URL,
    GODS_CONTRACT,
    WALLET_ADDRESS,
    PRIVATE_KEY,
    ZKEVM_RPC,
    ZKEVM_CHAIN_ID,
    FORGE_RATIOS,
)
from market import get_gu_auth_token

# GU's order-fulfilment ("factory") service.  Completing a forge requires a
# PUT here that links the on-chain GODS payment tx to the order — this is the
# step that makes GU run the card destroy + mint.  Reverse-engineered from the
# website's "Complete Order" button.
FACTORY_BASE = "https://factory.prod.prod.godsunchained.com"

# GU internal quality codes (opposite order from our QUALITIES list).
# Confirmed from the /forge response: quality=5 Plain, quality=4 Meteorite.
GU_QUALITY_CODE = {
    "Diamond":   1,
    "Gold":      2,
    "Shadow":    3,
    "Meteorite": 4,
    "Plain":     5,
}
QUALITY_FROM_CODE = {v: k for k, v in GU_QUALITY_CODE.items()}

# Standard ERC-20 ABI (just the bits we need)
_ERC20_ABI = [
    {
        "constant": False,
        "inputs":   [{"name": "dst", "type": "address"},
                     {"name": "wad", "type": "uint256"}],
        "name":     "transfer",
        "outputs":  [{"name": "", "type": "bool"}],
        "type":     "function",
    },
    {
        "constant": True,
        "inputs":   [{"name": "owner", "type": "address"}],
        "name":     "balanceOf",
        "outputs":  [{"name": "", "type": "uint256"}],
        "type":     "function",
    },
    {
        "constant": True, "inputs": [], "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}], "type": "function",
    },
]


# ── Auth / user identity ──────────────────────────────────────────────────────

class ForgeApiError(RuntimeError):
    """Any failure in the forge API pipeline."""


def _decode_jwt_payload(token: str) -> dict:
    try:
        payload = token.split(".")[1]
        payload += "=" * (4 - len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))
    except Exception as e:
        raise ForgeApiError(f"Could not decode JWT: {e}")


def get_user_id_and_token() -> tuple[int, str]:
    """
    Returns (gu_user_id, bearer_token).  Both come from the JWT the launcher
    keeps refreshed on disk.  Raises ForgeApiError if the user has never
    logged in via the launcher.
    """
    token = get_gu_auth_token()
    if not token:
        raise ForgeApiError(
            "No GU auth token found.  Open the launcher once to log in — "
            "the refresh token will be cached and reused from then on."
        )
    payload = _decode_jwt_payload(token)
    user_id = payload.get("id")
    if not user_id:
        raise ForgeApiError(f"JWT has no 'id' claim: {payload}")
    return int(user_id), token


# ── Asset inventory (GU internal asset IDs, not zkEVM token IDs) ──────────────

def fetch_user_assets(
    user_id:        int,
    token:          str,
    quality:        Optional[str] = None,
    only_off_chain: bool = True,
    log:            Callable = print,
) -> list[dict]:
    """
    Returns a flat list of {id, proto, quality, minting_status} dicts.
    `id` is the GU asset ID (what /forge expects in its asset_id array).

    The endpoint returns the ENTIRE user inventory in one ~3 MB call, shaped as
        {"protos": {"<proto_id>": {"assets": [{"id", "properties": {"quality"}},
                                              ...]}, ...}}

    `only_off_chain=True` filters to in-game (unminted) cards — the ones
    /forge actually consumes.  Minted NFTs would need to be moved back on-chain
    or handled differently.
    """
    last_err = None
    for attempt in range(10):
        if attempt:
            wait = min(2 ** attempt, 60)  # 2, 4, 8, 16, 32, 60, 60 … s
            log(f"  Assets service error — retry {attempt}/9 in {wait}s…")
            time.sleep(wait)
        r = requests.get(
            GU_LEGACY_ASSETS_URL,
            params={"type": "card", "user_id": user_id},
            headers={"Authorization": f"Bearer {token}"},
            timeout=120,   # large inventory response can be 3 MB+; give it time
        )
        if r.status_code == 401:
            raise ForgeApiError("Bearer token rejected — refresh token may have expired.")
        if r.ok:
            break
        last_err = f"Legacy marketplace returned {r.status_code}: {r.text[:300]}"
        if r.status_code < 500:
            raise ForgeApiError(last_err)   # 4xx — retrying won't help
    else:
        raise ForgeApiError(f"Legacy marketplace still failing after 10 attempts. Last error: {last_err}")

    data   = r.json()
    protos = data.get("protos") or {}

    q_filter = GU_QUALITY_CODE.get(quality) if quality else None
    out: list[dict] = []
    for proto_str, proto_data in protos.items():
        try:
            proto_id = int(proto_str)
        except ValueError:
            continue
        for a in (proto_data.get("assets") or []):
            props  = a.get("properties") or {}
            q_code = props.get("quality")
            if q_filter is not None and q_code != q_filter:
                continue
            m_status = a.get("minting_status")
            if only_off_chain and m_status != "off_chain":
                continue
            out.append({
                "id":             a.get("id"),
                "proto":          proto_id,
                "quality":        q_code,
                "minting_status": m_status,
            })
    return out


def group_assets_by_proto(assets: list[dict]) -> dict[tuple[int, str], list[int]]:
    """
    Groups asset ids by (proto, quality-name).  Returns a map of asset-id
    lists ready to pass to POST /forge.
    """
    out: dict[tuple[int, str], list[int]] = {}
    for a in assets:
        proto = a.get("proto")
        q_code = a.get("quality")
        aid   = a.get("id")
        if proto is None or q_code is None or aid is None:
            continue
        q_name = QUALITY_FROM_CODE.get(int(q_code))
        if not q_name:
            continue
        out.setdefault((int(proto), q_name), []).append(int(aid))
    return out


# ── Forge API calls ───────────────────────────────────────────────────────────

def _fusing_post(url: str, token: str, body: dict) -> dict:
    r = requests.post(
        url,
        json=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
            "Accept":        "application/json, text/plain, */*",
            # Origin header mirrors the launcher — some GU endpoints check it
            "Origin":        "https://master.desktop.godsunchained.com",
            "Referer":       "https://master.desktop.godsunchained.com/",
        },
        timeout=30,
    )
    if not r.ok:
        raise ForgeApiError(f"{url} returned {r.status_code}: {r.text[:400]}")
    return r.json()


def validate_forge(user_id: int, address: str, asset_ids: list[int], token: str) -> dict:
    """
    Dry-run: returns {flux_amount, token_amount} for the planned forge
    without creating an order.  Useful for sanity-checking costs.
    """
    return _fusing_post(
        GU_FUSING_VALIDATION_URL, token,
        {"user_id": user_id, "address": address.lower(), "asset_id": asset_ids},
    )


def create_forge_order(user_id: int, address: str, asset_ids: list[int], token: str) -> dict:
    """
    Creates an 'initiated' forge order.  Response includes token_payment_address
    and token_amount (in wei) — we send that exact amount to that exact address
    to settle the forge on-chain.
    """
    return _fusing_post(
        GU_FUSING_FORGE_URL, token,
        {"user_id": user_id, "address": address.lower(), "asset_id": asset_ids},
    )


# ── On-chain GODS payment ────────────────────────────────────────────────────

def _make_retry_session() -> requests.Session:
    """
    requests.Session with exponential-backoff retries for 429/5xx — the public
    Immutable RPC at rpc.immutable.com throttles aggressively and web3 7.x
    amplifies every user call into several RPC hits via its middleware chain.
    Without this, a single forge reliably trips a 429.
    """
    retry = Retry(
        total=8,
        backoff_factor=0.6,              # 0.6, 1.2, 2.4, 4.8, 9.6, 19.2 s …
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET", "POST"]),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    s = requests.Session()
    adapter = HTTPAdapter(max_retries=retry, pool_connections=4, pool_maxsize=8)
    s.mount("https://", adapter)
    s.mount("http://",  adapter)
    return s


def _get_web3() -> Web3:
    session = _make_retry_session()
    w3 = Web3(Web3.HTTPProvider(ZKEVM_RPC, session=session, request_kwargs={"timeout": 30}))
    # w3.is_connected() itself fires an RPC call; treat 429s there as transient.
    try:
        if not w3.is_connected():
            raise ForgeApiError(f"Could not reach zkEVM RPC at {ZKEVM_RPC}")
    except Exception as e:
        raise ForgeApiError(f"zkEVM RPC check failed ({ZKEVM_RPC}): {e}")
    return w3


def send_gods_payment(
    payment_address:  str,
    amount_wei:       int,
    private_key:      str,
    w3:               Optional[Web3] = None,
    log:              Callable = print,
    contract_address: Optional[str] = None,
) -> str:
    """
    Signs and broadcasts GODS.transfer(payment_address, amount_wei) from the
    account that owns `private_key`.  Waits for confirmation.  Returns the
    transaction hash (hex string).

    contract_address: override the GODS ERC-20 contract (defaults to GODS_CONTRACT
    from config).  Pass the value from the forge order's token_contract field so
    we always use what GU tells us rather than a hardcoded constant.
    """
    w3   = w3 or _get_web3()
    acct = Account.from_key(private_key)
    gods = w3.eth.contract(
        address=Web3.to_checksum_address(contract_address or GODS_CONTRACT),
        abi=_ERC20_ABI,
    )

    # Sanity: do we have enough GODS?
    try:
        balance = gods.functions.balanceOf(acct.address).call()
        if balance < amount_wei:
            raise ForgeApiError(
                f"Insufficient GODS: have {balance/1e18:.4f}, need {amount_wei/1e18:.4f}"
            )
    except ForgeApiError:
        raise
    except Exception as e:
        log(f"  (balance check skipped: {e})")

    nonce = w3.eth.get_transaction_count(acct.address, "pending")

    # ── EIP-1559 (type 2) transaction ────────────────────────────────────────
    # CRITICAL: GU's settlement service only processes type-2 EIP-1559
    # Transfer events.  Type-0 legacy transactions are confirmed on-chain but
    # GU's chain-watcher ignores them — the forge order stays "initiated" and
    # no card is minted.  Confirmed by comparing:
    #   • MetaMask forge (type 2, 0.1 GODS) → card appeared ✔
    #   • automation (type 0, 0.3/0.7 GODS) → confirmed on-chain, no card ✘
    # All three on-chain from the same wallet to the same payment address.
    try:
        latest   = w3.eth.get_block("latest")
        base_fee = int(latest.get("baseFeePerGas") or 0)
    except Exception:
        base_fee = 0

    # 10.67 gwei priority fee — matches MetaMask's default on Immutable zkEVM.
    # The base fee on zkEVM is negligible (< 100 wei); the priority fee is the
    # entire cost.  maxFeePerGas = 2 × baseFee + priority gives headroom for
    # one block of base-fee growth.
    PRIORITY_FEE = 10_670_000_000           # 10.67 gwei in wei
    max_fee      = base_fee * 2 + PRIORITY_FEE

    tx = gods.functions.transfer(
        Web3.to_checksum_address(payment_address),
        int(amount_wei),
    ).build_transaction({
        "from":                  acct.address,
        "nonce":                 nonce,
        "maxFeePerGas":          max_fee,
        "maxPriorityFeePerGas":  PRIORITY_FEE,
        "chainId":               ZKEVM_CHAIN_ID,
    })
    log(f"  building type-2 EIP-1559 tx  (base={base_fee} wei, priority={PRIORITY_FEE} wei)")

    # Estimate gas, then pad 20 % for safety
    try:
        tx["gas"] = int(w3.eth.estimate_gas(tx) * 1.2)
    except Exception:
        tx["gas"] = 80_000   # ERC20 transfer is typically ~37k

    signed = acct.sign_transaction(tx)
    raw = getattr(signed, "raw_transaction", None) or signed.rawTransaction
    tx_hash = w3.eth.send_raw_transaction(raw)
    tx_hex  = tx_hash.hex()
    if not tx_hex.startswith("0x"):
        tx_hex = "0x" + tx_hex
    log(f"  tx sent: {tx_hex}")

    # Wait for inclusion (zkEVM settles in a few seconds)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.status != 1:
        raise ForgeApiError(f"GODS transfer reverted: {tx_hex}")
    log(f"  tx confirmed in block {receipt.blockNumber}")
    return tx_hex


# ── Top-level orchestration ──────────────────────────────────────────────────

def notify_payment(
    order: dict,
    tx_hex: str,
    token: str,
    log: Callable = print,
) -> bool:
    """
    Try to tell GU's fusing service that the on-chain payment has been sent.
    GU may require this callback rather than (or in addition to) chain-watching.
    Returns True if any endpoint accepted it.
    """
    factory_id  = order.get("factory_order_id")
    request_id  = order.get("request_id")
    pay_addr    = order.get("token_payment_address") or order.get("payment_address")
    amount      = order.get("token_amount") or order.get("amount")
    wallet      = order.get("address") or WALLET_ADDRESS

    base = "https://fusing.prod.prod.godsunchained.com"

    attempts = []
    if factory_id:
        attempts += [
            (f"{base}/forge/{factory_id}/confirm",  "POST"),
            (f"{base}/forge/{factory_id}/complete", "POST"),
            (f"{base}/forge/{factory_id}/payment",  "POST"),
            (f"{base}/forge/{factory_id}",          "PATCH"),
        ]
    if request_id:
        attempts += [
            (f"{base}/forge/{request_id}/confirm",  "POST"),
            (f"{base}/forge/{request_id}/payment",  "POST"),
        ]

    body = {
        "tx_hash":    tx_hex,
        "address":    wallet.lower(),
        "token_amount": str(amount),
        "token_payment_address": pay_addr,
    }
    hdrs = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
        "Origin":        "https://master.desktop.godsunchained.com",
    }

    for url, method in attempts:
        try:
            fn = requests.post if method == "POST" else requests.patch
            r  = fn(url, json=body, headers=hdrs, timeout=10)
            log(f"  notify {method} {url.split('/')[-2:]} → {r.status_code}: {r.text[:120]}")
            if r.ok:
                return True
        except Exception as e:
            log(f"  notify {url} failed: {e}")
    return False


def check_forge_status(order_id: str, token: str, log: Callable = print) -> Optional[str]:
    """
    Poll the fusing API for the status of a forge order.
    Returns the status string (e.g. 'completed', 'initiated', 'failed') or None.
    """
    # Try both the factory_order_id integer endpoint and the request_id UUID
    urls = [
        f"https://fusing.prod.prod.godsunchained.com/forge/{order_id}",
        f"https://fusing.prod.prod.godsunchained.com/forge/order/{order_id}",
    ]
    for url in urls:
        try:
            r = requests.get(
                url,
                headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
                timeout=15,
            )
            if r.ok:
                data = r.json()
                status = data.get("status") or data.get("state")
                log(f"  Forge order {order_id} status: {status}")
                return status
            if r.status_code != 404:
                log(f"  Status check {url} → {r.status_code}: {r.text[:120]}")
        except Exception as e:
            log(f"  Status check failed: {e}")
    return None


def wait_for_forge_completion(
    order_id:      str,
    token:         str,
    uid:           Optional[int] = None,
    log:           Callable = print,
    max_wait:      int = 45,
    poll_interval: int = 2,
) -> bool:
    """
    Poll the factory until the order is fully settled (source cards destroyed +
    output card minted), returning as soon as status == "complete" — typically
    a few seconds.  Falls back to returning after `max_wait` (the payment is
    already registered via the factory PUT, so GU finishes on its own even if
    we stop watching).

    Returns True if confirmed settled, False if still settling at timeout.
    """
    if uid is None:
        try:
            uid = _gu_user_id(token)
        except Exception:
            uid = None

    log(f"  Waiting for GU to settle the forge (polling, up to {max_wait}s)…")
    deadline = time.time() + max_wait
    while time.time() < deadline:
        time.sleep(poll_interval)
        if uid is None:
            continue
        try:
            o = _factory_get_order_once(token, uid, int(order_id))
            if o and o.get("status") == "complete":
                log("  ✔ Forge settled — output card minted.")
                return True
        except Exception:
            pass   # transient; keep polling
    log(f"  Still settling after {max_wait}s — payment is registered, "
        "GU will finish shortly.")
    return False


# ── Factory service (the missing piece) ───────────────────────────────────────

def _gu_user_id(token: str) -> int:
    """The numeric GU user id, taken from the auth JWT's `id` claim."""
    payload = token.split(".")[1]
    payload += "=" * (4 - len(payload) % 4)
    return int(json.loads(base64.urlsafe_b64decode(payload))["id"])


def _factory_get_order_once(token: str, uid: int, order_id: int) -> Optional[dict]:
    """GET a single order from the factory (≈3 KB / 0.6 s) instead of the full
    1000-order list (≈1.4 MB / 2.3 s).  Returns the order dict or None."""
    try:
        r = requests.get(
            f"{FACTORY_BASE}/orders/{uid}/{order_id}",
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/json, text/plain, */*"},
            timeout=30,
        )
        if r.status_code == 200:
            o = r.json()
            if isinstance(o, dict) and o.get("id"):
                return o
    except Exception:
        pass
    return None


def _factory_fetch_order(token: str, uid: int, order_id: int,
                         log: Callable = print, retries: int = 12) -> Optional[dict]:
    """
    GET the order from the factory service and return its full record, retrying
    until it appears (the order is registered there a moment after POST /forge).
    """
    for attempt in range(retries):
        try:
            o = _factory_get_order_once(token, uid, order_id)
            if o:
                return o
        except Exception as e:
            log(f"  factory fetch error (attempt {attempt+1}): {e}")
        time.sleep(2)
    return None


def _find_gods_payment_action(order: dict) -> Optional[dict]:
    """
    Return the order's GODS token-transfer action as
    {iid, contract, recipient, amount_wei}.  The amount is read EXACTLY from
    the action params (it is NOT amount*1e18 — GU uses values like
    699999999900000000 that must be matched precisely).
    """
    for a in order.get("order_actions", []):
        if a.get("type_of") == "token-transfer" and a.get("status") != "complete":
            cr     = (a.get("action_config") or {}).get("contract_request") or {}
            params = cr.get("params") or []
            if len(params) >= 2:
                return {
                    "iid":        a["iid"],
                    "contract":   cr.get("contract_address") or GODS_CONTRACT,
                    "recipient":  params[0],
                    "amount_wei": int(params[1]),
                }
    return None


def _factory_put_updates(token: str, uid: int, order_id: int,
                         updates: list[dict]) -> requests.Response:
    """
    PUT one or more action updates onto an order.  Each update attaches an
    on-chain tx hash to an action_iid; GU verifies the tx and advances the
    order.  `updates` = [{"action_iid": int, "data": {...,"txn": tx}}, …].
    """
    return requests.put(
        f"{FACTORY_BASE}/orders/{uid}/{order_id}",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json",
                 "Accept": "application/json, text/plain, */*"},
        json={"action_updates": updates},
        timeout=30,
    )


# Minimal ABIs for the on-chain actions a forge order can ask the client to run.
#   token-transfer → GODS.transfer(address,uint256)
#   asset-burn     → ImmutableERC721.burnBatch(uint256[])   (burns the source cards)
_ACTION_FN_ABI = {
    "transfer": {
        "type": "function", "name": "transfer", "stateMutability": "nonpayable",
        "inputs":  [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}],
        "outputs": [{"name": "", "type": "bool"}],
    },
    "burnBatch": {
        "type": "function", "name": "burnBatch", "stateMutability": "nonpayable",
        "inputs":  [{"name": "tokenIDs", "type": "uint256[]"}],
        "outputs": [],
    },
}

# Forge actions whose contract_request the CLIENT must execute on-chain.
# (asset-mint / asset-destroy / consumable-destroy are done by GU server-side.)
_EXECUTABLE_ACTION_TYPES = {"token-transfer", "asset-burn"}


def _coerce_params(function_name: str, params: list):
    """Coerce the order's raw contract params into typed args for web3."""
    if function_name == "transfer":
        return [Web3.to_checksum_address(params[0]), int(params[1])]
    if function_name == "burnBatch":
        return [[int(x) for x in params[0]]]
    return params


def _find_onchain_actions(order: dict) -> list[dict]:
    """
    Return the still-open on-chain actions the client must execute, as
    [{iid, type, contract, function_name, params}, …], sorted by iid so the
    burn (lower iid) runs before the GODS payment.
    """
    out = []
    for a in order.get("order_actions", []):
        if a.get("status") == "complete":
            continue
        if a.get("type_of") not in _EXECUTABLE_ACTION_TYPES:
            continue
        cr = (a.get("action_config") or {}).get("contract_request") or {}
        if cr.get("function_name") and cr.get("contract_address") and cr.get("params") is not None:
            out.append({
                "iid":           a["iid"],
                "type":          a.get("type_of"),
                "contract":      cr["contract_address"],
                "function_name": cr["function_name"],
                "params":        cr["params"],
            })
    out.sort(key=lambda x: x["iid"])
    return out


def _execute_onchain_action(w3: Web3, acct, action: dict, log: Callable = print) -> str:
    """
    Build, sign and broadcast one forge action's contract call (type-2 EIP-1559)
    from the EOA, wait for the receipt, and return the tx hash.  Raises if the
    tx reverts — so a failed burn aborts BEFORE any payment is sent.
    """
    fn = action["function_name"]
    abi = _ACTION_FN_ABI.get(fn)
    if not abi:
        raise ForgeApiError(f"Don't know how to execute on-chain action '{fn}'.")

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(action["contract"]), abi=[abi])
    args  = _coerce_params(fn, action["params"])
    nonce = w3.eth.get_transaction_count(acct.address, "pending")

    # zkEVM base fee is negligible (<100 wei) and the 10.67 gwei priority fee is
    # the whole cost, so we skip the get_block() round-trip and just over-provide
    # maxFee.  We also skip estimate_gas (another round-trip) and use a generous
    # fixed gas limit — gas is ~free here, so over-provisioning the LIMIT costs
    # nothing (you only pay for gas actually used) and saves an RPC call per tx.
    PRIORITY_FEE = 10_670_000_000               # 10.67 gwei
    max_fee      = PRIORITY_FEE * 2
    if fn == "burnBatch":
        ntok = len(args[0]) if (args and isinstance(args[0], (list, tuple))) else 5
        gas_limit = 90_000 + 55_000 * ntok      # ~365k for 5 cards; plenty of headroom
    else:
        gas_limit = 70_000                       # ERC-20 transfer ≈ 37k

    tx = contract.functions[fn](*args).build_transaction({
        "from":                 acct.address,
        "nonce":                nonce,
        "maxFeePerGas":         max_fee,
        "maxPriorityFeePerGas": PRIORITY_FEE,
        "chainId":              ZKEVM_CHAIN_ID,
        "gas":                  gas_limit,        # provided → build_transaction won't estimate
    })

    signed  = acct.sign_transaction(tx)
    raw     = getattr(signed, "raw_transaction", None) or signed.rawTransaction
    tx_hash = w3.eth.send_raw_transaction(raw)
    tx_hex  = tx_hash.hex()
    if not tx_hex.startswith("0x"):
        tx_hex = "0x" + tx_hex

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    if receipt.status != 1:
        raise ForgeApiError(f"{fn} reverted on-chain: {tx_hex}")
    return tx_hex


def _build_action_tx(w3: Web3, acct, action: dict, nonce: int) -> str:
    """Build+sign+broadcast one action tx with an EXPLICIT nonce and DON'T wait
    for the receipt — returns the tx hash immediately.  Used to pipeline many
    forges in a tier (send all, then wait for receipts together)."""
    fn  = action["function_name"]
    abi = _ACTION_FN_ABI.get(fn)
    if not abi:
        raise ForgeApiError(f"Don't know how to execute on-chain action '{fn}'.")
    contract = w3.eth.contract(address=Web3.to_checksum_address(action["contract"]), abi=[abi])
    args = _coerce_params(fn, action["params"])
    PRIORITY_FEE = 10_670_000_000
    gas_limit = (90_000 + 55_000 * len(args[0])) if fn == "burnBatch" else 70_000
    tx = contract.functions[fn](*args).build_transaction({
        "from":                 acct.address,
        "nonce":                nonce,
        "maxFeePerGas":         PRIORITY_FEE * 2,
        "maxPriorityFeePerGas": PRIORITY_FEE,
        "chainId":              ZKEVM_CHAIN_ID,
        "gas":                  gas_limit,
    })
    signed = acct.sign_transaction(tx)
    raw    = getattr(signed, "raw_transaction", None) or signed.rawTransaction
    tx_hex = w3.eth.send_raw_transaction(raw).hex()
    return tx_hex if tx_hex.startswith("0x") else "0x" + tx_hex


def _forge_tier_pipelined(
    source_groups: list[list[int]],
    user_id:       int,
    token:         str,
    wallet:        str,
    w3:            Web3,
    acct,
    uid:           int,
    log:           Callable = print,
    stop_event=None,
) -> list[int]:
    """
    Forge every group in ONE tier with pipelining: create all orders, fire all
    on-chain txs back-to-back (managed nonces, no per-tx wait), wait for the
    receipts together, PUT them, then wait for all to settle.  Returns the list
    of minted asset ids (the next tier's inputs).

    Tiers are still run one-at-a-time by the caller (forge_chain) — you can't
    forge Gold before all the Shadows exist — but the forges *inside* a tier are
    independent, so this collapses 31 sequential waits into a few batched ones.
    """
    # 1) Create all orders + read their on-chain actions.
    orders = []
    for src in source_groups:
        if stop_event and stop_event.is_set():
            break
        o   = create_forge_order(user_id, wallet, src, token)
        oid = int(o.get("factory_order_id") or o.get("id") or 0)
        if not oid:
            log(f"    order create failed for {src}"); continue
        fo = _factory_fetch_order(token, uid, oid, log=log)
        acts = _find_onchain_actions(fo) if fo else []
        if not acts:
            log(f"    order {oid}: no on-chain actions, skipping"); continue
        orders.append({"id": oid, "actions": acts})

    if not orders:
        return []

    # 2) Send every tx back-to-back with locally-incremented nonces.
    n_tx  = sum(len(o["actions"]) for o in orders)
    log(f"    sending {n_tx} txs for {len(orders)} forge(s)…")
    nonce = w3.eth.get_transaction_count(acct.address, "pending")
    for od in orders:
        od["sent"] = []
        for a in od["actions"]:
            try:
                txh = _build_action_tx(w3, acct, a, nonce)
                od["sent"].append((a["iid"], txh))
                nonce += 1
            except Exception as e:
                log(f"    send failed (order {od['id']}, {a['function_name']}): {e}")
                od["sent"] = None
                break
            time.sleep(0.05)   # gentle pacing so the public RPC doesn't 429

    # 3) Wait for all receipts; mark which orders fully succeeded.
    for od in orders:
        od["ok"] = bool(od.get("sent"))
        for _iid, txh in (od.get("sent") or []):
            try:
                rc = w3.eth.wait_for_transaction_receipt(txh, timeout=180)
                if rc.status != 1:
                    od["ok"] = False
                    log(f"    tx reverted (order {od['id']}): {txh}")
            except Exception as e:
                od["ok"] = False
                log(f"    receipt wait failed (order {od['id']}): {e}")

    # 4) PUT the tx hashes for orders whose txs all succeeded.
    token = get_gu_auth_token() or token
    pending = set()
    for od in orders:
        if not od["ok"]:
            continue
        updates = [{"action_iid": iid,
                    "data": {"signature": "", "imx_signatures": [], "txn": txh}}
                   for iid, txh in od["sent"]]
        resp = _factory_put_updates(token, uid, od["id"], updates)
        if resp.ok:
            pending.add(od["id"])
        else:
            log(f"    PUT failed (order {od['id']}): HTTP {resp.status_code} {resp.text[:120]}")

    log(f"    {len(pending)} forge(s) paid; waiting for GU to mint…")

    # 5) Poll until ALL settle; collect minted ids.  The timeout scales with the
    #    number of forges — GU mints them at its own pace and a big tier (e.g. 25
    #    forges at once) can take several minutes; cutting it short would drop
    #    outputs and break the next tier.
    minted: list[int] = []
    timeout  = max(240, 15 * len(pending))     # ~6 min for a 25-forge tier
    deadline = time.time() + timeout
    while pending and time.time() < deadline:
        time.sleep(3)
        token = get_gu_auth_token() or token
        for oid in list(pending):
            fo = _factory_get_order_once(token, uid, oid)
            if fo and fo.get("status") == "complete":
                for a in fo.get("order_actions", []):
                    if a.get("type_of") == "asset-mint":
                        minted += (a.get("action_config") or {}).get("asset_ids") or []
                pending.discard(oid)
    if pending:
        log(f"    ⚠ {len(pending)} forge(s) still settling after {timeout}s "
            f"(forge_chain will try to recover their outputs from inventory).")
    return minted


def forge_one(
    source_asset_ids: list[int],
    private_key:      str,          # EOA key used to send the GODS payment
    user_id:          int,
    token:            str,
    wallet_address:   str,          # the EOA wallet (must own private_key)
    w3:               Optional[Web3] = None,
    log:              Callable = print,
) -> dict:
    """
    Runs the full pipeline for a single forge (N source cards → 1 output) and
    completes it end-to-end with no clicks.

    The flow (reverse-engineered from the website's "Complete Order" button):
      1. POST /forge                     → creates the order.
      2. GET  factory /orders/{uid}      → read the order's on-chain actions.
      3. Execute each on-chain action from the EOA (web3.py):
           • asset-burn   → burnBatch(tokenIDs)   (only for on-chain source cards)
           • token-transfer → GODS.transfer(recipient, exact_amount)
      4. PUT factory /orders/{uid}/{id}  → attach each tx hash to its action.
         GU then mints the output card server-side.

    Off-chain source cards skip the burn (GU destroys them server-side), so a
    fresh in-game forge has only the transfer action.  On-chain (imx_minted)
    source cards add the burnBatch action — needed for multi-tier chaining,
    where every forge output is an on-chain NFT.

    Step 4 is the part every earlier attempt missed; the on-chain txs alone are
    confirmed but never settled.
    """
    log(f"  Creating forge order for asset ids {source_asset_ids}…")
    order = create_forge_order(user_id, wallet_address, source_asset_ids, token)

    order_id = order.get("factory_order_id") or order.get("id") or order.get("request_id")
    if not order_id:
        raise ForgeApiError(f"Forge order response missing id.\nFull response: {order}")

    # ── Read the order's on-chain actions from the factory ──────────────────
    uid = _gu_user_id(token)
    log(f"  Order id={order_id} created. Reading actions from factory…")
    fo = _factory_fetch_order(token, uid, int(order_id), log=log)
    if not fo:
        raise ForgeApiError(
            f"Order {order_id} never appeared in the factory service.")
    actions = _find_onchain_actions(fo)
    if not actions:
        raise ForgeApiError(f"No executable on-chain actions on order {order_id}.")

    w3   = w3 or _get_web3()
    acct = Account.from_key(private_key)

    # Pre-flight: make sure we hold enough GODS for the payment BEFORE we burn
    # anything irreversibly.
    transfer = next((a for a in actions if a["type"] == "token-transfer"), None)
    if transfer:
        need_wei = int(transfer["params"][1])
        try:
            gods = w3.eth.contract(
                address=Web3.to_checksum_address(transfer["contract"]), abi=_ERC20_ABI)
            bal = gods.functions.balanceOf(acct.address).call()
            if bal < need_wei:
                raise ForgeApiError(
                    f"Insufficient GODS: have {bal/1e18:.4f}, need {need_wei/1e18:.4f}")
        except ForgeApiError:
            raise
        except Exception as e:
            log(f"  (GODS balance check skipped: {e})")

    # ── Execute each on-chain action (burn first, then pay) ─────────────────
    summary = ", ".join(f"{a['function_name']}#{a['iid']}" for a in actions)
    log(f"  Executing on-chain actions: {summary}")
    updates = []
    for a in actions:
        if a["type"] == "token-transfer":
            log(f"    GODS transfer {int(a['params'][1])/1e18:.6f} → {a['params'][0]} (iid {a['iid']})…")
        else:
            log(f"    burnBatch {len(a['params'][0])} card(s) (iid {a['iid']})…")
        tx_hex = _execute_onchain_action(w3, acct, a, log=log)
        log(f"      tx {tx_hex}")
        updates.append({
            "action_iid": a["iid"],
            "data": {"signature": "", "imx_signatures": [], "txn": tx_hex},
        })

    order["tx_hashes"] = [u["data"]["txn"] for u in updates]

    # ── Tell the factory (token is short-lived; refresh after the chain wait) ─
    token = get_gu_auth_token() or token
    resp  = _factory_put_updates(token, uid, int(order_id), updates)
    if not resp.ok:
        raise ForgeApiError(
            f"factory PUT failed: HTTP {resp.status_code}: {resp.text[:300]}\n"
            f"(on-chain txs already sent: {order['tx_hashes']} — order may need manual completion.)"
        )
    log(f"  ✔ Factory accepted {len(updates)} action(s) (HTTP {resp.status_code}). "
        "GU will mint the output card.")

    order["confirmed"] = True
    settled = wait_for_forge_completion(str(order_id), token, uid=uid, log=log)

    # Capture the newly-minted card's asset id(s) from the completed order so a
    # chain can feed them straight into the next tier (no inventory re-poll).
    minted: list[int] = []
    try:
        token = get_gu_auth_token() or token
        final = _factory_get_order_once(token, uid, int(order_id))
        if final:
            for a in final.get("order_actions", []):
                if a.get("type_of") == "asset-mint":
                    minted += (a.get("action_config") or {}).get("asset_ids") or []
    except Exception as e:
        log(f"  (could not read minted asset id: {e})")
    order["minted_asset_ids"] = minted
    order["settled"] = settled
    return order


# Quality tiers in forge order (each forges up into the next).
FORGE_QUALITY_ORDER = ["Plain", "Meteorite", "Shadow", "Gold", "Diamond"]


def _proto_quality_ids(user_id: int, token: str, proto: int, quality: str) -> list[int]:
    """Current GU asset ids the wallet holds for (proto, quality), newest first."""
    assets = fetch_user_assets(user_id, token, quality=quality, only_off_chain=False)
    return sorted(
        [a["id"] for a in assets if a.get("proto") == proto and a.get("id")],
        reverse=True,
    )


def _lift_one_tier(proto, q, nq, pool, user_id, token, w3, acct,
                   log=print, stop_event=None) -> list[int]:
    """Forge ONE tier: turn `pool` (asset ids of quality q) into nq cards.
    Returns the freshly-minted nq asset ids, with late-mint reconciliation
    against inventory.  Shared by forge_chain and forge_combine_plan."""
    ratio = FORGE_RATIOS[q]
    n = len(pool) // ratio
    if n == 0:
        return []
    groups = [pool[i * ratio:(i + 1) * ratio] for i in range(n)]
    token  = get_gu_auth_token() or token
    before = set(_proto_quality_ids(user_id, token, proto, nq))
    minted = _forge_tier_pipelined(groups, user_id, token, WALLET_ADDRESS,
                                   w3, acct, user_id, log=log, stop_event=stop_event)
    if len(minted) < n and not (stop_event and stop_event.is_set()):
        log(f"  Captured {len(minted)}/{n} {nq}; waiting for late mints to "
            "appear in inventory…")
        wait_deadline = time.time() + max(120, 20 * (n - len(minted)))
        while time.time() < wait_deadline:
            time.sleep(10)
            token = get_gu_auth_token() or token
            fresh = [i for i in _proto_quality_ids(user_id, token, proto, nq)
                     if i not in before]
            log(f"    {len(fresh)}/{n} {nq} now owned…")
            if len(fresh) >= n:
                break
        fresh = [i for i in _proto_quality_ids(user_id, token, proto, nq)
                 if i not in before]
        if len(fresh) > len(minted):
            minted = fresh
    return minted


def forge_chain(
    proto:            int,
    from_quality:     str,
    target_quality:   str,
    start_count:      Optional[int] = None,   # use at most this many starting cards
    source_ids:       Optional[list[int]] = None,  # forge EXACTLY these asset ids
    log:              Callable = print,
    progress_cb:      Optional[Callable[[int, str, str, dict], None]] = None,
    stop_event=None,
) -> list[dict]:
    """
    Forge a single proto all the way up the quality ladder in one go:
    e.g. from_quality="Meteorite", target_quality="Diamond" turns a stack of
    Meteorites into 25 Shadows → 5 Golds → 1 Diamond automatically.

    Each tier's freshly-minted outputs (captured from the completed orders)
    become the next tier's inputs, so there's no dependence on the slow
    marketplace inventory re-indexing between tiers.

    Returns the flat list of per-forge order receipts.  Stops early (without
    error) if a tier doesn't have enough cards to forge at least once.
    """
    if not PRIVATE_KEY:
        raise ForgeApiError("PRIVATE_KEY is not set — add it to .env.")
    derived = Account.from_key(PRIVATE_KEY).address.lower()
    if derived != WALLET_ADDRESS.lower():
        raise ForgeApiError(
            f"Private key mismatch (key={derived}, wallet={WALLET_ADDRESS}).")

    try:
        fi = FORGE_QUALITY_ORDER.index(from_quality)
        ti = FORGE_QUALITY_ORDER.index(target_quality)
    except ValueError:
        raise ForgeApiError(f"Unknown quality in {from_quality}→{target_quality}.")
    if ti <= fi:
        raise ForgeApiError("Target quality must be higher than the source quality.")

    user_id, token = get_user_id_and_token()
    w3 = _get_web3()

    # Seed the pool.  `source_ids` (used by the custodial service) forges exactly
    # those deposited cards so one user's job never touches another's; otherwise
    # we take the wallet's own cards at the starting quality.
    token = get_gu_auth_token() or token
    if source_ids is not None:
        pool = list(source_ids)
    else:
        pool = _proto_quality_ids(user_id, token, proto, from_quality)
        if start_count is not None:
            pool = pool[:start_count]
    log(f"Chain forge proto {proto}: {from_quality} → {target_quality}. "
        f"Using {len(pool)} {from_quality}.")

    acct = Account.from_key(PRIVATE_KEY)
    receipts: list[dict] = []
    for qi in range(fi, ti):
        q, nq = FORGE_QUALITY_ORDER[qi], FORGE_QUALITY_ORDER[qi + 1]
        ratio = FORGE_RATIOS[q]
        if stop_event and stop_event.is_set():
            log("Stopped by user.")
            break

        n = len(pool) // ratio
        log(f"\n=== Tier {q} → {nq}:  {len(pool)} {q}, ratio {ratio}  →  {n} forge(s) (pipelined) ===")
        if n == 0:
            log(f"Not enough {q} to forge (need {ratio}). Chain stops at {q}.")
            break

        # All `n` forges in THIS tier are independent → pipeline them (handled by
        # _lift_one_tier, incl. late-mint reconciliation).  The next tier can't
        # start until they've all minted (e.g. need all 5 Golds before the
        # Diamond), so we wait for the whole tier here before moving up.
        minted = _lift_one_tier(proto, q, nq, pool[:n * ratio],
                                user_id, token, w3, acct, log, stop_event)

        for mid in minted:
            receipts.append({"minted_asset_ids": [mid], "confirmed": True})
        if progress_cb:
            progress_cb(len(receipts), q, nq, {})

        # Outputs of this tier are the inputs of the next.
        pool = minted
        log(f"  Tier {q}→{nq} complete: {len(pool)} {nq} available for the next tier.")
        if not pool and qi + 1 < ti:
            log("  No minted outputs captured — cannot continue the chain.")
            break

    log(f"\nChain finished: {len(receipts)} forge(s) total.")
    return receipts


def _ratio_product(from_q: str, target_q: str) -> int:
    """Source cards consumed to make ONE target_q from from_q."""
    try:
        fi, ti = FORGE_QUALITY_ORDER.index(from_q), FORGE_QUALITY_ORDER.index(target_q)
    except ValueError:
        return 0
    cpo = 1
    for qi in range(fi, ti):
        cpo *= FORGE_RATIOS.get(FORGE_QUALITY_ORDER[qi], 5)
    return cpo


def forge_plan(
    proto:       int,
    operations:  list[tuple],     # [(from_quality, target_quality, qty), …]
    log:         Callable = print,
    progress_cb: Optional[Callable] = None,
    stop_event=None,
) -> list[dict]:
    """
    Run a mixed forge plan for ONE proto in a single pass, e.g.
        [("Meteorite","Diamond",1), ("Meteorite","Gold",2), ("Meteorite","Shadow",5)]
    Cards are allocated in DISTINCT slices per operation (same source quality
    draws from one fetched pool, sliced so operations never overlap), then each
    operation is chained up with forge_chain(source_ids=…).
    """
    if not PRIVATE_KEY:
        raise ForgeApiError("PRIVATE_KEY is not set — add it to .env.")
    derived = Account.from_key(PRIVATE_KEY).address.lower()
    if derived != WALLET_ADDRESS.lower():
        raise ForgeApiError(f"Private key mismatch (key={derived}, wallet={WALLET_ADDRESS}).")

    user_id, token = get_user_id_and_token()

    from collections import defaultdict
    by_from: dict[str, list[tuple]] = defaultdict(list)
    for fq, tq, qty in operations:
        if qty and qty > 0:
            by_from[fq].append((tq, int(qty)))

    receipts: list[dict] = []
    for fq, ops in by_from.items():
        if stop_event and stop_event.is_set():
            break
        token = get_gu_auth_token() or token
        pool  = _proto_quality_ids(user_id, token, proto, fq)
        idx   = 0
        for tq, qty in ops:
            if stop_event and stop_event.is_set():
                break
            cpo  = _ratio_product(fq, tq)
            need = qty * cpo
            slice_ids = pool[idx:idx + need]
            idx += len(slice_ids)
            if len(slice_ids) < cpo:
                log(f"  Not enough {fq} for {qty}× {tq} "
                    f"(need {need}, have {len(slice_ids)}). Skipping.")
                continue
            log(f"\n##### Forging {qty}× {tq} from {len(slice_ids)} {fq} #####")
            recs = forge_chain(proto, fq, tq, source_ids=slice_ids,
                               log=log, stop_event=stop_event)
            receipts += recs
            if progress_cb:
                progress_cb(len(receipts), fq, tq, {})
    log(f"\nPlan finished: {len(receipts)} forge(s) total.")
    return receipts


def combine_yield(target_quality: str, contributions: dict) -> tuple[int, dict]:
    """Pure calc: how many `target_quality` cards a mix of contributed lower-tier
    cards yields when cascaded & merged at each tier.  Returns (count, leftover)
    where leftover[q] = cards of tier q that couldn't be forged up.

    e.g. target=Diamond, {Gold:2, Shadow:10, Meteorite:25}
         Met 25 →5 Sha; +10 = 15 Sha →3 Gld; +2 = 5 Gld →1 Diamond  →  (1, {})
    """
    order = FORGE_QUALITY_ORDER
    try:
        ti = order.index(target_quality)
    except ValueError:
        return 0, {}
    contrib = {q: int(n) for q, n in contributions.items() if n and int(n) > 0}
    starts = [order.index(q) for q in contrib if order.index(q) < ti]
    if not starts:
        return 0, {}
    carry, leftover = 0, {}
    for level in range(min(starts), ti):
        q = order[level]
        ratio = FORGE_RATIOS[q]
        avail = contrib.get(q, 0) + carry
        carry = avail // ratio
        rem = avail % ratio
        if rem:
            leftover[q] = rem
    return carry, leftover


def forge_combine_plan(
    proto:       int,
    operations:  list,            # [{"target": q, "contribute": {tier: count}}, …]
    log:         Callable = print,
    progress_cb: Optional[Callable] = None,
    stop_event=None,
) -> list[dict]:
    """
    Run COMBINE operations for one proto: each op forges UP to a target tier by
    pooling contributed cards from several lower tiers, merging each tier's
    contribution with whatever was forged from below.  Cards are reserved in
    DISTINCT slices per tier across all ops so nothing is used twice.
    """
    if not PRIVATE_KEY:
        raise ForgeApiError("PRIVATE_KEY is not set — add it to .env.")
    derived = Account.from_key(PRIVATE_KEY).address.lower()
    if derived != WALLET_ADDRESS.lower():
        raise ForgeApiError(f"Private key mismatch (key={derived}, wallet={WALLET_ADDRESS}).")

    user_id, token = get_user_id_and_token()
    w3   = _get_web3()
    acct = Account.from_key(PRIVATE_KEY)
    order = FORGE_QUALITY_ORDER

    # Fetch each needed tier's ids ONCE, then hand out distinct slices per op.
    token = get_gu_auth_token() or token
    tiers_needed = {t for op in operations for t, n in op.get("contribute", {}).items() if n}
    ids_by_tier  = {t: _proto_quality_ids(user_id, token, proto, t) for t in tiers_needed}
    idx_by_tier  = {t: 0 for t in tiers_needed}

    receipts: list[dict] = []
    for op in operations:
        if stop_event and stop_event.is_set():
            break
        target = op["target"]
        contribute = {t: int(n) for t, n in op.get("contribute", {}).items() if n and int(n) > 0}
        if not contribute:
            continue
        ti = order.index(target)

        # Reserve this op's exact asset ids from each tier's shared pool.
        reserved: dict[str, list[int]] = {}
        for t, cnt in contribute.items():
            avail = ids_by_tier.get(t, [])
            sl = avail[idx_by_tier[t]:idx_by_tier[t] + cnt]
            idx_by_tier[t] += len(sl)
            if sl:
                reserved[t] = sl
            if len(sl) < cnt:
                log(f"  Only {len(sl)}/{cnt} {t} left for this op.")

        yld, _lo = combine_yield(target, {t: len(v) for t, v in reserved.items()})
        log(f"\n##### Combine → {yld}× {target} from "
            + " + ".join(f"{len(v)} {t}" for t, v in reserved.items()) + " #####")

        start = min(order.index(t) for t in reserved) if reserved else ti
        carry: list[int] = []
        for level in range(start, ti):
            if stop_event and stop_event.is_set():
                break
            q, nq = order[level], order[level + 1]
            pool = list(carry) + list(reserved.get(q, []))
            ratio = FORGE_RATIOS[q]
            n = len(pool) // ratio
            log(f"  Tier {q}→{nq}: {len(pool)} {q} "
                f"({len(reserved.get(q, []))} yours + {len(carry)} forged) → {n} forge(s)")
            if n == 0:
                log(f"  Not enough {q} to forge up — stopping this op.")
                break
            minted = _lift_one_tier(proto, q, nq, pool[:n * ratio],
                                    user_id, token, w3, acct, log, stop_event)
            receipts += [{"minted_asset_ids": [m], "confirmed": True} for m in minted]
            carry = minted
            token = get_gu_auth_token() or token
            if not carry and level + 1 < ti:
                log("  No minted outputs — cannot continue this op.")
                break
        log(f"  → made {len(carry)} {target}.")
        if progress_cb:
            progress_cb(len(receipts), "combine", target, {})

    log(f"\nCombine plan finished: {len(receipts)} forge(s) total.")
    return receipts


def forge_by_proto_quality(
    proto:        int,
    quality:      str,
    count:        int,
    ratio:        int,
    log:          Callable = print,
    progress_cb:  Optional[Callable[[int, int, dict], None]] = None,
    stop_event=None,         # threading.Event — checked between forges
    asset_ids:    Optional[list[int]] = None,  # pre-loaded from app; skips marketplace-legacy
) -> list[dict]:
    """
    High-level: forge `count` times from (proto, quality), picking asset_ids
    from the user's inventory.  Returns a list of order receipts (one per
    forge).  Partial failures bubble up as ForgeApiError with the index.

    asset_ids: if supplied (loaded by the app at startup via fetch_ingame_plain_cards),
    the marketplace-legacy fetch is skipped entirely — avoids the slow/flaky
    second call to that endpoint.
    """
    # ── Verify the EOA key matches the wallet that owns the cards ───────────
    # The forge order is created under WALLET_ADDRESS, and the GODS payment is
    # sent from the same EOA (private_key).  GU links the payment to the order
    # via the factory PUT (see forge_one), so the on-chain sender just needs to
    # be this wallet.  If the key and address disagree, abort before spending.
    if not PRIVATE_KEY:
        raise ForgeApiError(
            "PRIVATE_KEY is not set — add PRIVATE_KEY=0x… to .env to "
            "enable 1-click forging."
        )
    derived = Account.from_key(PRIVATE_KEY).address.lower()
    if derived != WALLET_ADDRESS.lower():
        raise ForgeApiError(
            f"Private key mismatch!\n"
            f"  WALLET_ADDRESS in .env       = {WALLET_ADDRESS}\n"
            f"  Address derived from key     = {derived}\n"
            "These must be the same wallet.  Fix .env before forging."
        )
    log(f"Wallet verified: {derived}")

    user_id, token = get_user_id_and_token()

    need = count * ratio

    # ── Build the pool of source asset IDs ──────────────────────────────────
    # Prefer the inventory the app already pre-loaded (asset_ids).  This skips a
    # second, slow, frequently-throttled call to the marketplace-legacy assets
    # endpoint on every forge run.
    #
    # The old code always re-fetched live and picked newest-first to dodge GU's
    # FIFO/amount-based payment matching (a stale order with the same amount
    # could absorb the payment).  That collision is impossible now: forge_one
    # links each payment to its exact order via the factory PUT, so any valid
    # off-chain card works and the pre-loaded list is safe to use directly.
    if asset_ids and len(asset_ids) >= need:
        pool = list(asset_ids)
        log(f"Using {len(pool)} pre-loaded {quality} asset IDs for proto {proto}.")
    else:
        log("No pre-loaded IDs — fetching live asset IDs from GU marketplace…")
        live_assets = fetch_user_assets(user_id, token, quality=quality,
                                        only_off_chain=False, log=log)
        # off-chain first, then newest id first
        live_assets.sort(key=lambda a: (
            0 if a.get("minting_status") == "off_chain" else 1,
            -a.get("id", 0),
        ))
        grouped = group_assets_by_proto(live_assets)
        pool    = grouped.get((proto, quality), [])

    if len(pool) < need:
        raise ForgeApiError(
            f"Not enough {quality} cards for proto {proto}: "
            f"have {len(pool)}, need {need} for {count} forge(s)."
        )

    w3      = _get_web3()        # shared web3 instance for all forges this run
    results: list[dict] = []

    for i in range(count):
        if stop_event and stop_event.is_set():
            log(f"Stopped after {i}/{count} forge(s).")
            break
        log(f"Forge {i+1}/{count}: proto={proto} {quality} → ratio {ratio}")
        source = pool[i*ratio : (i+1)*ratio]
        receipt = forge_one(
            source_asset_ids=source,
            private_key=PRIVATE_KEY,        # EOA key sends the GODS payment
            user_id=user_id,
            token=token,
            wallet_address=WALLET_ADDRESS,  # EOA wallet (owns the cards + key)
            w3=w3,
            log=log,
        )
        results.append(receipt)
        if progress_cb:
            progress_cb(i + 1, count, receipt)

    return results


def api_mode_available() -> bool:
    """
    True when the 1-click forge path is available.

    The flow is pure HTTP + web3.py — NO launcher, NO MetaMask, NO Passport:
      1. POST /forge to create the order (auth via the launcher's cached token).
      2. GODS payment on-chain from the EOA (PRIVATE_KEY).
      3. PUT to the factory service to link the tx to the order.

    So all it needs is the EOA key + wallet in .env.
    """
    return bool(PRIVATE_KEY) and bool(WALLET_ADDRESS)


def gods_balance(wallet: Optional[str] = None, w3: Optional[Web3] = None) -> Optional[float]:
    """Current GODS balance (in whole GODS) of `wallet` (defaults to WALLET_ADDRESS).
    Returns None on any RPC error."""
    try:
        w3   = w3 or _get_web3()
        gods = w3.eth.contract(address=Web3.to_checksum_address(GODS_CONTRACT),
                               abi=_ERC20_ABI)
        addr = Web3.to_checksum_address(wallet or WALLET_ADDRESS)
        return gods.functions.balanceOf(addr).call() / 1e18
    except Exception:
        return None
