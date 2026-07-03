"""
CDP-based automation for the Gods Unchained Electron launcher.

Why raw CDP instead of Playwright?
───────────────────────────────────
Playwright's connect_over_cdp() calls Browser.setDownloadBehavior right
after connecting.  Electron's embedded Chromium rejects this with:
  "Protocol error (Browser.setDownloadBehavior): Browser context
   management is not supported"
…and drops the connection entirely, breaking forge, screenshot, and
plain-card reading.

We bypass this by connecting directly to the page's WebSocket debug URL
using websocket-client, which only uses commands Electron does support.

Connection strategy
───────────────────
The launcher must be running with --remote-debugging-port=9222.
_ensure_launcher_debug() handles this automatically:
  1. If the debug port is already open → connect directly.
  2. Otherwise → kill any running instance, restart with the flag,
     wait up to 30 s.

Forge page layout (from live screenshot)
─────────────────────────────────────────
  Left panel  – search box + quality filter tabs + card grid ("0/N" per card)
  Right panel – card detail + "START FUSING" button (shown after card selection)
"""

import base64
import json
import subprocess
import time
from pathlib import Path
from typing import Callable, Optional

import psutil
import requests as _req
import websocket          # pip install websocket-client

from config import LAUNCHER_EXE, LAUNCHER_URL, FORGE_PATH, DEBUG_PORT

FORGE_URL      = LAUNCHER_URL + FORGE_PATH
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


# ── Launcher process management ───────────────────────────────────────────────

def _debug_port_open() -> bool:
    try:
        r = _req.get(f"http://localhost:{DEBUG_PORT}/json/version", timeout=2)
        return r.ok
    except Exception:
        return False


def _kill_launcher():
    for proc in psutil.process_iter(["name", "exe"]):
        name = (proc.info.get("name") or "").lower()
        exe  = (proc.info.get("exe")  or "").lower()
        if "gods unchained" in name or "gods unchained" in exe:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                pass


def _start_launcher_with_debug() -> bool:
    subprocess.Popen(
        [LAUNCHER_EXE, f"--remote-debugging-port={DEBUG_PORT}"],
        close_fds=True,
    )
    for _ in range(30):
        if _debug_port_open():
            return True
        time.sleep(1)
    return False


def _ensure_launcher_debug(log: Callable = print, may_restart: bool = False):
    """
    Ensure the launcher is running and accessible on the debug port.

    may_restart=False (default, used during auto-load):
        Raises DebugPortClosedError if the port is not open — never kills
        a running launcher automatically.

    may_restart=True (used when the user explicitly clicks Screenshot/Forge):
        Kills and restarts the launcher with the debug flag if the port is
        not already open.
    """
    if _debug_port_open():
        log("Debug port already open.")
        return
    if not may_restart:
        raise DebugPortClosedError(
            "GU launcher debug port is not open — plain cards will appear "
            "after you click Screenshot or Forge (which opens the port)."
        )
    log("Restarting launcher with debug port…")
    _kill_launcher()
    time.sleep(1)
    if not _start_launcher_with_debug():
        raise RuntimeError(
            "Could not open debug port on the GU launcher after 30 s. "
            "Try closing the launcher manually and retrying."
        )
    log("Launcher started with debug port.")


class DebugPortClosedError(RuntimeError):
    """Raised when the CDP debug port is not open and we must not restart."""


# ── CDP target discovery ──────────────────────────────────────────────────────

def _list_targets() -> list[dict]:
    try:
        r = _req.get(f"http://localhost:{DEBUG_PORT}/json/list", timeout=5)
        return r.json()
    except Exception as e:
        raise RuntimeError(f"Cannot reach debug port {DEBUG_PORT}: {e}")


def _get_gu_page_ws_url() -> str:
    targets = _list_targets()
    # Prefer the GU master-desktop page
    for t in targets:
        if "godsunchained" in (t.get("url") or ""):
            return t["webSocketDebuggerUrl"]
    # Fall back to any page-type target
    for t in targets:
        if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
            return t["webSocketDebuggerUrl"]
    raise RuntimeError(
        "No GU page found on debug port — open the game in the launcher."
    )


def _get_metamask_ws_url() -> Optional[str]:
    try:
        for t in _list_targets():
            url = t.get("url") or ""
            ws  = t.get("webSocketDebuggerUrl")
            if ws and ("metamask" in url or
                       ("chrome-extension" in url and
                        ("notification" in url or "confirm" in url))):
                return ws
    except Exception:
        pass
    return None


def _get_browser_ws_url() -> str:
    """Browser-level WebSocket (needed for Target.* commands)."""
    r = _req.get(f"http://localhost:{DEBUG_PORT}/json/version", timeout=5)
    return r.json()["webSocketDebuggerUrl"]


# ── Raw CDP browser client (for creating hidden targets) ──────────────────────

class _CDPBrowser:
    """
    Connects to the Electron browser's *browser-level* WebSocket so we can
    call Target.createTarget / Target.closeTarget.  This lets us run the
    forge flow in a brand-new page target without touching the main launcher
    window the user is actually looking at.
    """

    def __init__(self):
        self._ws = websocket.create_connection(_get_browser_ws_url(), timeout=60)
        self._id = 0

    def _call(self, method: str, **params) -> dict:
        self._id += 1
        self._ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            try:
                raw = self._ws.recv()
            except websocket.WebSocketTimeoutException:
                raise RuntimeError(f"Timeout waiting for browser CDP response to {method}")
            data = json.loads(raw)
            if data.get("id") == self._id:
                if "error" in data:
                    raise RuntimeError(
                        f"CDP browser {method}: "
                        f"{data['error'].get('message', data['error'])}"
                    )
                return data.get("result", {})

    def create_target(self, url: str, background: bool = True) -> str:
        """
        Create a new page target loading `url`.  Returns the target id.
        `background=True` asks Chromium to create the target without stealing
        focus / showing the window; Electron may or may not honour it.
        """
        try:
            r = self._call("Target.createTarget", url=url, background=background)
        except RuntimeError:
            # Some Chromium builds don't support the `background` flag — retry without.
            r = self._call("Target.createTarget", url=url)
        return r["targetId"]

    def close_target(self, target_id: str):
        try:
            self._call("Target.closeTarget", targetId=target_id)
        except Exception:
            pass

    def wait_for_target_ws(self, target_id: str, timeout_s: float = 10) -> str:
        """Poll the /json/list endpoint until the new target exposes a WS URL."""
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            for t in _list_targets():
                if t.get("id") == target_id and t.get("webSocketDebuggerUrl"):
                    return t["webSocketDebuggerUrl"]
            time.sleep(0.25)
        raise RuntimeError(f"New target {target_id[:8]}… never exposed a WS URL.")

    def close(self):
        try:
            self._ws.close()
        except Exception:
            pass


# ── Raw CDP page client ───────────────────────────────────────────────────────

class _CDPPage:
    """
    Minimal synchronous CDP client that connects to a single page target
    via its WebSocket debug URL.  Only uses page-level CDP commands that
    Electron's Chromium actually supports.
    """

    def __init__(self, ws_url: str):
        self._ws = websocket.create_connection(ws_url, timeout=60)
        self._id = 0
        # Filled in by connect_page() when this page owns a background target:
        self._owned_target_id: Optional[str]  = None
        self._browser:         Optional[_CDPBrowser] = None
        self._call("Page.enable")
        self._call("Runtime.enable")

    # ── Core ──────────────────────────────────────────────────────────────────

    def _call(self, method: str, **params) -> dict:
        self._id += 1
        self._ws.send(json.dumps({"id": self._id,
                                  "method": method,
                                  "params": params}))
        while True:          # drain CDP events until we get the matching response
            try:
                raw = self._ws.recv()
            except websocket.WebSocketTimeoutException:
                raise RuntimeError(f"Timeout waiting for CDP response to {method}")
            data = json.loads(raw)
            if data.get("id") == self._id:
                if "error" in data:
                    raise RuntimeError(
                        f"CDP {method} error: "
                        f"{data['error'].get('message', data['error'])}"
                    )
                return data.get("result", {})
            # else: it is an event or a response to a different id — discard

    def evaluate(self, expression: str):
        """Run JS in the page context and return the JSON-serialised result."""
        r   = self._call("Runtime.evaluate", expression=expression,
                         returnByValue=True, awaitPromise=False)
        exc = r.get("exceptionDetails")
        if exc:
            raise RuntimeError(f"JS exception: {exc.get('text', exc)}")
        return r.get("result", {}).get("value")

    def navigate(self, url: str, settle_s: float = 3.0):
        """Navigate to a URL and wait for the page to become ready."""
        self._call("Page.navigate", url=url)
        time.sleep(settle_s)
        # Poll until document is ready (transient JS context resets are expected)
        deadline = time.time() + 20
        while time.time() < deadline:
            try:
                if self.evaluate("document.readyState") == "complete":
                    break
            except Exception:
                pass
            time.sleep(0.4)

    def wait_ms(self, ms: int):
        time.sleep(ms / 1000)

    def screenshot_png(self) -> bytes:
        try:
            r = self._call("Page.captureScreenshot", format="png",
                           captureBeyondViewport=True)
        except RuntimeError:
            r = self._call("Page.captureScreenshot", format="png")
        return base64.b64decode(r["data"])

    def close(self):
        try:
            self._ws.close()
        except Exception:
            pass
        # If we created our own background target, tear it down so the user
        # doesn't accumulate phantom windows.
        if self._browser and self._owned_target_id:
            self._browser.close_target(self._owned_target_id)
            self._browser.close()
            self._browser = None
            self._owned_target_id = None

    # ── JS helpers ────────────────────────────────────────────────────────────

    def js_fill(self, selector: str, value: str) -> bool:
        """Fill a React-controlled input field (triggers synthetic events)."""
        code = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (!el) return false;
            el.focus();
            // Bypass React's controlled-input optimisation
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, {json.dumps(value)});
            el.dispatchEvent(new Event('input',  {{bubbles: true}}));
            el.dispatchEvent(new Event('change', {{bubbles: true}}));
            return true;
        }})()
        """
        try:
            return bool(self.evaluate(code))
        except Exception:
            return False

    def js_click_sel(self, selector: str) -> bool:
        """Click the first element matching a CSS selector."""
        code = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (!el) return false;
            el.click();
            return true;
        }})()
        """
        try:
            return bool(self.evaluate(code))
        except Exception:
            return False

    def js_click_text(self, text: str,
                      tags: str = "button,[role='button'],[role='tab']",
                      exact: bool = False) -> bool:
        """
        Click the first button/tab matching the given text.
        exact=True matches only if the element's trimmed text equals the needle —
        use this for tab labels ("Plain", "Meteorite") so we don't accidentally
        click a card description that happens to contain the word.
        """
        match = "t === needle" if exact else "t.includes(needle)"
        code = f"""
        (() => {{
            const needle = {json.dumps(text.lower())};
            for (const el of document.querySelectorAll({json.dumps(tags)})) {{
                const t = (el.textContent || '').trim().toLowerCase();
                if ({match}) {{
                    el.click();
                    return true;
                }}
            }}
            return false;
        }})()
        """
        try:
            return bool(self.evaluate(code))
        except Exception:
            return False

    def count_matches_text(self, text: str,
                           tags: str = "button,[role='button'],[role='tab']") -> int:
        """Diagnostic — how many visible tags contain this text (lowercased)?"""
        code = f"""
        (() => {{
            const needle = {json.dumps(text.lower())};
            let n = 0;
            for (const el of document.querySelectorAll({json.dumps(tags)})) {{
                if ((el.textContent || '').trim().toLowerCase().includes(needle)) n++;
            }}
            return n;
        }})()
        """
        try:
            return int(self.evaluate(code) or 0)
        except Exception:
            return 0

    def current_url(self) -> str:
        try:
            return self.evaluate("window.location.href") or ""
        except Exception:
            return ""

    def save_screenshot(self, path: Path):
        """Save a PNG screenshot to disk; returns the path on success."""
        try:
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(self.screenshot_png())
            return path
        except Exception:
            return None

    def js_click_card(self, card_name: str) -> bool:
        """Click the card tile in the forge grid matching the given card name."""
        code = f"""
        (() => {{
            const needle = {json.dumps(card_name.lower())};
            const sel = '[data-proto],[class*="card"],[class*="Card"],' +
                        '[class*="tile"],[class*="Tile"],' +
                        '[class*="item"],[class*="Item"]';
            for (const el of document.querySelectorAll(sel)) {{
                if ((el.textContent || '').toLowerCase().includes(needle)) {{
                    el.click();
                    return true;
                }}
            }}
            return false;
        }})()
        """
        try:
            return bool(self.evaluate(code))
        except Exception:
            return False

    def wait_for_text(self, text: str,
                      tags: str = "button",
                      timeout_ms: int = 8000) -> bool:
        """Wait until an element with the given text appears on the page."""
        needle   = text.lower()
        deadline = time.time() + timeout_ms / 1000
        while time.time() < deadline:
            try:
                found = self.evaluate(f"""
                (() => {{
                    const needle = {json.dumps(needle)};
                    return Array.from(document.querySelectorAll({json.dumps(tags)}))
                        .some(el => (el.textContent || '').toLowerCase().includes(needle));
                }})()
                """)
                if found:
                    return True
            except Exception:
                pass
            time.sleep(0.3)
        return False


def connect_page(log: Callable = print,
                 may_restart: bool = False,
                 url: str = FORGE_URL,
                 prefer_background: bool = True) -> _CDPPage:
    """
    Returns a CDP page for automation.

    prefer_background=True (default):
        Opens a brand-new page target loading `url` directly — the user's
        main launcher window is never navigated away from.  If Electron
        doesn't honour the `background` flag this target may briefly pop
        up as a visible window, but it's separate from the main view.

    prefer_background=False:
        Reuses the existing GU page target (legacy behaviour that hijacks
        the main window).  Kept as a fallback.
    """
    _ensure_launcher_debug(log, may_restart=may_restart)

    if prefer_background:
        try:
            browser = _CDPBrowser()
            log(f"Opening background target for {url}…")
            tid    = browser.create_target(url, background=True)
            ws_url = browser.wait_for_target_ws(tid, timeout_s=15)
            page   = _CDPPage(ws_url)
            page._owned_target_id = tid
            page._browser         = browser
            # Give the SPA a moment to boot in the new target.
            page.wait_ms(3500)
            log(f"Background target {tid[:8]}… ready.")
            return page
        except Exception as e:
            log(f"Background target unavailable ({e}) — falling back to main window.")

    ws_url = _get_gu_page_ws_url()
    log("Connecting to main GU page (will navigate it — user will see this)…")
    return _CDPPage(ws_url)


def _on_forge_page(url: str) -> bool:
    """
    True if `url` looks like the forge page.  The launcher uses hash
    routing (e.g.  …com/#/game/gu/game-modes) so we look at what comes
    after the `#`, not just a substring of the whole URL.
    """
    if not url:
        return False
    hash_part = url.split("#", 1)[1] if "#" in url else url
    for kw in ("forge", "forging", "fuse", "fusion"):
        if kw in hash_part.lower():
            return True
    return False


def _navigate_to_forge(page: _CDPPage, log: Callable) -> bool:
    """
    Reach the forge page on the launcher's hash-routed SPA.

    Order of attempts:
      1. If we're already there, do nothing.
      2. Click an in-app nav link labelled "Forge" / "Fuse".
      3. Directly set window.location.hash (no page reload — React Router
         picks up the hashchange event).
      4. Try alternative route names: /#/forge, /#/forging, /#/fuse, /#/fusion.
      5. Page.navigate to the full URL with the hash included.

    Logs the final URL on failure so the next debug round has something to go on.
    """
    current = page.current_url()
    log(f"Current URL: {current}")
    if _on_forge_page(current):
        return True

    # ── 1) Click nav link if one exists on the current page ─────────────────
    for txt in ("Forge", "Fuse", "Forging", "Fusion"):
        if page.js_click_text(txt, tags="a,button,[role='link'],[role='tab']",
                              exact=True):
            page.wait_ms(2500)
            if _on_forge_page(page.current_url()):
                log(f"Reached forge via nav link '{txt}'.")
                return True

    # ── 2) Try several hash routes (SPA picks up hashchange events) ─────────
    # Launcher nests app routes under /game/gu/… (the default landing is
    # /#/game/gu/game-modes), so try those first before bare /forge.
    routes = (
        "/game/gu/forge",
        "/game/gu/forging",
        "/game/gu/fuse",
        "/game/gu/fusion",
        "/forge",
        "/forging",
        "/fuse",
        "/fusion",
    )
    for route in routes:
        try:
            # Set hash and fire hashchange manually in case the app listens to it
            page.evaluate(f"""
                (() => {{
                    window.location.hash = {json.dumps(route)};
                    window.dispatchEvent(new HashChangeEvent('hashchange'));
                }})()
            """)
            page.wait_ms(1800)
            if _on_forge_page(page.current_url()):
                log(f"Reached forge via hash route '{route}'.")
                return True
        except Exception:
            pass

    # ── 3) Page.navigate with hash included ────────────────────────────────
    for route in ("/game/gu/forge", "/game/gu/forging", "/forge", "/forging", "/fuse"):
        hash_url = f"{LAUNCHER_URL}/#{route}"
        try:
            log(f"Trying Page.navigate → {hash_url}")
            page.navigate(hash_url, settle_s=3.0)
            page.wait_ms(1500)
            if _on_forge_page(page.current_url()):
                log(f"Reached forge via full-URL navigate ({hash_url}).")
                return True
        except Exception:
            pass

    # ── 4) Last resort: dump all nav link hrefs for diagnostics ─────────────
    try:
        hrefs = page.evaluate("""
            (() => {
                const out = [];
                document.querySelectorAll('a,[role="link"]').forEach(el => {
                    const t = (el.textContent || '').trim();
                    const h = el.getAttribute('href') || '';
                    if (t.length && t.length < 30) out.push(t + ' → ' + h);
                });
                return out.slice(0, 40);
            })()
        """)
        if hrefs:
            log("Available nav links on this page:")
            for line in hrefs:
                log(f"   · {line}")
    except Exception:
        pass

    log(f"⚠ could not reach forge page — still on {page.current_url()}")
    return False


# ── MetaMask payment via CDP ──────────────────────────────────────────────────

def get_passport_address(log: Callable = print) -> Optional[str]:
    """
    Return the user's Passport smart-contract wallet address via
    window.ethereum.selectedAddress.

    This is the Sequence contract wallet (0x0D3be80…) that GU's chain-watcher
    watches.  It is different from the raw EOA / Magic.link signing key.  The
    forge order's `address` field AND the GODS payment sender must both be this
    wallet for GU's settlement service to recognise the transaction.

    Returns None if the launcher isn't running or Passport isn't connected.
    """
    try:
        _ensure_launcher_debug(log=log, may_restart=False)
    except Exception:
        return None
    try:
        ws_url = _get_gu_page_ws_url()
        page   = _CDPPage(ws_url)
        try:
            # selectedAddress is synchronous — available immediately when
            # Passport is already connected to the GU page.
            addr = page.evaluate(
                "window.ethereum ? window.ethereum.selectedAddress : null"
            )
            if addr and str(addr).startswith("0x"):
                log(f"  Passport wallet (selectedAddress): {addr}")
                return str(addr)

            # Fallback: ask via eth_accounts (async — requires awaitPromise).
            r = page._call(
                "Runtime.evaluate",
                expression=(
                    "(async () => {"
                    "  try {"
                    "    const a = await window.ethereum"
                    "        .request({method: 'eth_accounts'});"
                    "    return (a && a[0]) ? a[0] : null;"
                    "  } catch (e) { return null; }"
                    "})()"
                ),
                returnByValue=True,
                awaitPromise=True,
                timeout=10_000,
            )
            acct = (r.get("result") or {}).get("value")
            if acct and str(acct).startswith("0x"):
                log(f"  Passport wallet (eth_accounts): {acct}")
                return str(acct)
        finally:
            page.close()
    except Exception as e:
        log(f"  Could not get Passport wallet address: {e}")
    return None


def send_payment_via_metamask(
    payment_address: str,
    amount_wei:      int,
    gods_contract:   str,
    log:             Callable = print,
    auto_confirm:    bool     = False,
    timeout:         int      = 120,
) -> Optional[str]:
    """
    Sends the GODS ERC-20 payment through the launcher's MetaMask provider
    (window.ethereum) instead of a raw web3.py transaction.

    This routes through Immutable Passport's transaction pipeline — the same
    path the GU game uses — which is what GU's settlement service actually
    watches for.

    Returns the tx hash on success, or None if the user rejected / timed out.

    Requires the launcher to be running with --remote-debugging-port=9222.
    """
    _ensure_launcher_debug(log=log, may_restart=False)

    # ERC-20 transfer(address,uint256) calldata
    # Selector: 0xa9059cbb
    # address padded to 32 bytes, uint256 padded to 32 bytes
    to_padded  = payment_address.lower().replace("0x", "").zfill(64)
    amt_padded = hex(amount_wei)[2:].zfill(64)
    data = "0xa9059cbb" + to_padded + amt_padded

    js = f"""
(async () => {{
  try {{
    const txHash = await window.ethereum.request({{
      method: 'eth_sendTransaction',
      params: [{{
        from:  window.ethereum.selectedAddress,
        to:    '{gods_contract.lower()}',
        data:  '{data}',
        value: '0x0',
      }}],
    }});
    return txHash;
  }} catch (e) {{
    return 'ERROR:' + e.message;
  }}
}})()
"""

    ws_url = _get_gu_page_ws_url()
    # Use a WebSocket socket-timeout that is comfortably longer than the CDP
    # awaitPromise timeout so the recv() loop never fires before Chrome replies.
    ws_sock_timeout = timeout + 45
    page = _CDPPage.__new__(_CDPPage)
    page._ws = websocket.create_connection(ws_url, timeout=ws_sock_timeout)
    page._id = 0
    page._owned_target_id = None
    page._browser         = None
    page._call("Page.enable")
    page._call("Runtime.enable")

    log("  Injecting GODS payment via window.ethereum…")
    # Use awaitPromise so we get the result back synchronously.
    # The CDP `timeout` field tells Chrome to wait up to `timeout` seconds
    # for the Promise to resolve — Passport auto-approves GU forge transactions
    # so this usually resolves within a few seconds.
    result = page._call(
        "Runtime.evaluate",
        expression=js,
        returnByValue=True,
        awaitPromise=True,
        timeout=timeout * 1000,
    )
    page.close()

    val = (result.get("result") or {}).get("value")
    exc = result.get("exceptionDetails")
    if exc:
        log(f"  MetaMask injection error: {exc.get('text', exc)}")
        return None
    if val and str(val).startswith("ERROR:"):
        log(f"  MetaMask rejected payment: {val}")
        return None
    if val:
        log(f"  MetaMask tx submitted: {val}")
        return str(val)

    log("  MetaMask returned no tx hash — user may have rejected or timed out.")
    return None


# ── Screenshot utility ────────────────────────────────────────────────────────

def screenshot_forge(log: Callable = print) -> Optional[Path]:
    """
    Opens the forge page in a *new background target* and saves a screenshot.
    The user's main launcher window is not disturbed.
    """
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    out  = SCREENSHOT_DIR / f"forge_{int(time.time())}.png"
    page = connect_page(log, may_restart=True, url=FORGE_URL,
                        prefer_background=True)
    try:
        if not _navigate_to_forge(page, log):
            log("Warning: the new target never reached /forge — "
                "screenshot may show home or login page.")
        page.wait_ms(3000)
        png = page.screenshot_png()
        out.write_bytes(png)
        log(f"Screenshot saved → {out}")
    finally:
        page.close()
    return out


# ── Plain card reading from launcher ─────────────────────────────────────────

def fetch_plain_from_launcher(log: Callable = print) -> list[dict]:
    """
    Reads unminted plain cards directly from the launcher's forge page.
    Returns [{proto: int, count: int}, ...]  (only cards with a known proto).
    """
    # may_restart=False: never kill the launcher during background auto-load.
    # If the debug port is closed we return [] and the status bar shows why.
    # prefer_background=True: scrape in a hidden/separate target so the
    # user's main launcher window is never touched.
    page = connect_page(log, may_restart=False, url=FORGE_URL,
                        prefer_background=True)
    try:
        if not _navigate_to_forge(page, log):
            log("Could not reach forge page in background target.")
            return []
        page.wait_ms(2000)

        log("Scrolling to load all cards…")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_ms(1000)

        log("Reading card counts from forge page DOM…")

        # Use a raw string so Python doesn't mangle the JS regex backslashes.
        result = page.evaluate(r"""
            (() => {
                const out = {};

                // Strategy 1: elements that carry a data-proto attribute
                // and contain "selected/owned" text like "0/9".
                document.querySelectorAll('[data-proto]').forEach(el => {
                    const proto = el.getAttribute('data-proto');
                    const txt   = el.innerText || '';
                    const m     = txt.match(/\d+\/(\d+)/);
                    if (proto && m) out[proto] = Math.max(out[proto]||0, parseInt(m[1]));
                });
                if (Object.keys(out).length) return { method: 'data-proto', out };

                // Strategy 2: scan all leaf text nodes for "N/M" pattern,
                // then walk up the DOM to find a proto identifier.
                const seen = new Set();
                document.querySelectorAll('*').forEach(el => {
                    if (el.children.length > 0) return;
                    const txt = (el.textContent || '').trim();
                    if (!/^\d+\/\d+$/.test(txt)) return;
                    const key = txt + el.getBoundingClientRect().top;
                    if (seen.has(key)) return;
                    seen.add(key);

                    const owned = parseInt(txt.split('/')[1]);
                    if (owned === 0) return;

                    let node = el.parentElement;
                    for (let i = 0; i < 8 && node; i++) {
                        const proto = node.getAttribute('data-proto')
                                   || node.getAttribute('data-id')
                                   || node.getAttribute('data-card-id');
                        if (proto) {
                            out[proto] = Math.max(out[proto]||0, owned);
                            return;
                        }
                        node = node.parentElement;
                    }

                    // Last resort: key by card name text
                    node = el.parentElement;
                    for (let i = 0; i < 8 && node; i++) {
                        const nameEl = node.querySelector(
                            'p,h3,h4,[class*="name"],[class*="Name"]');
                        if (nameEl) {
                            const name = (nameEl.textContent || '').trim();
                            if (name && name.length > 1) {
                                out['__name__' + name] =
                                    Math.max(out['__name__'+name]||0, owned);
                                return;
                            }
                        }
                        node = node.parentElement;
                    }
                });

                return { method: 'text-scan', out };
            })()
        """)

        cards: list[dict] = []
        if result:
            raw    = result.get("out", {})
            method = result.get("method")
            log(f"DOM scrape ({method}): {len(raw)} entries")
            for k, count in raw.items():
                if k.startswith("__name__"):
                    pass   # name-only cards can't be looked up — skip them
                else:
                    try:
                        cards.append({"proto": int(k), "count": count})
                    except ValueError:
                        pass
            if cards:
                log(f"Found {len(cards)} plain card types in launcher.")
            else:
                log("DOM scrape returned data but no usable proto ids.")
        else:
            log("Could not read plain cards — take a screenshot to inspect the forge page.")

        # Nothing to restore — the background target is closed in finally.
        return cards
    finally:
        page.close()


# ── Forge automation ──────────────────────────────────────────────────────────

_SEL_SEARCH = ('input[placeholder*="Search"], input[placeholder*="search"], '
               'input[type="search"]')


def _confirm_metamask(log: Callable):
    log("Waiting for Metamask popup…")
    deadline = time.time() + 30
    mm_ws    = None

    while time.time() < deadline:
        mm_ws = _get_metamask_ws_url()
        if mm_ws:
            break
        time.sleep(0.5)

    if not mm_ws:
        raise RuntimeError("Metamask popup not found within 30 s — confirm manually.")

    log("Connecting to Metamask popup…")
    mm = _CDPPage(mm_ws)
    try:
        time.sleep(1.0)
        for label in ("Confirm", "Sign", "Approve"):
            if mm.js_click_text(label):
                log(f"Metamask: clicked '{label}'.")
                return
        raise RuntimeError("Could not find Confirm button in Metamask popup.")
    finally:
        mm.close()


def _do_one_forge(page: _CDPPage, card_name: str, quality: str,
                  auto_confirm: bool, log: Callable, forge_index: int = 0):
    """
    Execute a single forge on the GU forge page.

    Flow (based on live forge page UI):
      1. Navigate to forge URL (only if not already there).
      2. Click the quality filter tab (FROM-quality, e.g. "Plain") — EXACT match.
      3. Type card name into the search box.
      4. Click the card tile in the grid → right panel shows card + START FUSING.
      5. Click START FUSING.
      6. Handle any in-app confirmation modal.
      7. Confirm in Metamask (auto or wait for manual).

    On any unexpected failure, a debug screenshot is saved to screenshots/
    with a step-tagged name so you can see exactly what the page looked like.
    """
    def debug_shot(tag: str):
        p = SCREENSHOT_DIR / f"forge_fail_{forge_index}_{tag}_{int(time.time())}.png"
        saved = page.save_screenshot(p)
        if saved:
            log(f"🖼  debug screenshot → {saved}")

    # ── 0: Make sure we're on the forge page ────────────────────────────────
    if not _navigate_to_forge(page, log):
        debug_shot("no_forge_route")
        raise RuntimeError(
            "Could not reach the forge page. The SPA kept redirecting — "
            "check the debug screenshot and the current URL."
        )
    page.wait_ms(1500)

    # ── 1: Quality tab FIRST (filters the grid before we search) ────────────
    # exact=True so we click the TAB labelled "Plain", not a card description
    # or stat row that happens to contain the word.
    n_matches = page.count_matches_text(quality)
    log(f"Clicking quality tab '{quality}' (candidates on page: {n_matches})")
    if not page.js_click_text(quality, exact=True):
        # Fall back to substring match if exact didn't work (some UIs include
        # a count badge like "Plain (329)").
        if not page.js_click_text(quality, exact=False):
            log(f"⚠ quality tab '{quality}' not clickable.")
            debug_shot("no_quality_tab")
    page.wait_ms(1200)

    # ── 2: Search ────────────────────────────────────────────────────────────
    if page.js_fill(_SEL_SEARCH, card_name):
        log(f"Typed '{card_name}' into search.")
    else:
        log("⚠ search box not found.")
        debug_shot("no_search")
    page.wait_ms(1500)   # debounce

    # ── 3: Click card tile ───────────────────────────────────────────────────
    if page.js_click_card(card_name):
        log(f"Card tile '{card_name}' clicked.")
    else:
        log("⚠ card tile not found by name — trying first grid item.")
        debug_shot("no_card_tile")
        if not page.js_click_sel(
            '[data-proto],[class*="CardTile"],[class*="card-tile"],'
            '[class*="CardItem"],[class*="card-item"]'
        ):
            raise RuntimeError(f"Could not click any card tile for '{card_name}'.")
    page.wait_ms(1400)   # right panel fade-in

    # ── 4: START FUSING ──────────────────────────────────────────────────────
    log("Waiting for START FUSING button…")
    if not page.wait_for_text("FUSING", timeout_ms=10_000):
        debug_shot("no_fuse_btn")
        raise RuntimeError("'START FUSING' button never appeared. "
                           "See debug screenshot to check the page state.")
    clicked = (page.js_click_text("START FUSING") or
               page.js_click_text("FUSING"))
    if not clicked:
        debug_shot("fuse_btn_not_clickable")
        raise RuntimeError("Found START FUSING text but could not click it.")
    log("START FUSING clicked.")
    page.wait_ms(1500)

    # ── 5: In-app confirm modal (if any) ────────────────────────────────────
    for label in ("Confirm", "Forge Now", "Yes, Forge", "Yes"):
        if page.js_click_text(label):
            log(f"In-app modal: clicked '{label}'.")
            page.wait_ms(600)
            break

    # ── 6: MetaMask ──────────────────────────────────────────────────────────
    if auto_confirm:
        _confirm_metamask(log)
    else:
        log("Waiting for manual Metamask confirmation (up to 120 s)…")
        time.sleep(120)

    log("Forge submitted.")


def forge_card(
    proto:        int,
    card_name:    str,
    quality:      str,
    forge_count:  int,
    auto_confirm: bool,
    dry_run:      bool,
    status_cb:    Optional[Callable[[str], None]] = None,
) -> list[bool]:
    def log(msg):
        print(f"[forge] {msg}")
        if status_cb:
            status_cb(msg)

    if dry_run:
        for i in range(forge_count):
            log(f"[DRY RUN] Forge #{i+1}/{forge_count}: "
                f"{card_name} [{quality}] proto={proto}")
        return [True] * forge_count

    results: list[bool] = []
    # Open a dedicated background target for the whole forge session, so the
    # user's main launcher window is never hijacked.  The target is closed
    # automatically in `page.close()`.
    page = connect_page(log, may_restart=True, url=FORGE_URL,
                        prefer_background=True)
    try:
        for i in range(forge_count):
            log(f"Forge {i+1}/{forge_count}: {card_name} [{quality}]")
            try:
                _do_one_forge(page, card_name, quality, auto_confirm, log,
                              forge_index=i+1)
                results.append(True)
                time.sleep(2)
            except Exception as e:
                log(f"❌ Forge #{i+1} failed: {e}")
                # Save a final screenshot of whatever state the page ended in.
                try:
                    fail_path = (SCREENSHOT_DIR /
                                 f"forge_fail_{i+1}_final_{int(time.time())}.png")
                    if page.save_screenshot(fail_path):
                        log(f"🖼  Page state at failure → {fail_path}")
                except Exception:
                    pass
                results.append(False)
    finally:
        page.close()

    return results
