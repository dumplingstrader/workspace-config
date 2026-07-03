# GUVrs — Technical Handoff

> AI context restoration document. See README.md for user-facing info.
> **Last updated:** 2026-07-03

## What was accomplished

Full security/code review of a third-party Gods Unchained companion tool at
the user's request, following similar reviews of two other GU tools from
different developers (`Forging/`, `SellingBot/`) earlier this session. Read
every `.cs` file (~1,000 lines total) end to end; this app is source-available
(MIT, GitHub: TimothyMeadows/GUvrs) so no extraction/decompilation was needed.

## Architecture

- **.NET MAUI** app (C#), targets Windows, Mac Catalyst, Android.
- UI is an embedded `WebView` rendering server-generated HTML (Handlebars.Net
  templates in `Views/*.mustache`, embedded resources — not fetched remotely).
- C# ↔ JS communication is two-way:
  - **C# → JS**: `WebView.EvaluateJavaScriptAsync(...)` calls JS functions like
    `guvrs_set_value(...)` defined in the mustache templates.
  - **JS → C#**: JS navigates to a custom `guvrs://<event>?key=value` URL,
    intercepted in `MainPage.WebView_Navigating` and dispatched through a small
    pub/sub bus (`ConcurrentEventListener`).

### File map

| File | Responsibility |
|---|---|
| `MainPage.xaml.cs` | Bulk of the logic — wires up the log watcher, API calls, friends list, settings, and all `guvrs://` event handlers. |
| `Components/GuDebugLog.cs` | `FileSystemWatcher` + 1s poll timer on the game's `debug.log`; string-matches known log line markers (`gameID:`, `Game mode is`, `p:PlayerInfo(...)o:PlayerInfo(...)`, `GameNetworkManager.StopClient`, `Ending the game`) to fire `OnStart/OnGameMode/OnBegin/OnStop/OnEnd` events. |
| `Components/GuApi.cs` | Two GET calls: `/v0/mode` (game mode list) and `/user/{guid}/rank` (rank/win-loss). Plain `HttpClient`, no auth headers, no request body on GET. |
| `Components/StringExtractor.cs` | `"...".Extract(start, end)` — substring-between-two-markers helper used to parse log lines. |
| `Components/CrossPlatform.cs` | Per-OS file helpers; `GuLogPath` is set once at startup (see `Startup.cs`) and never changes at runtime. |
| `Startup.cs` | Sets `GuLogPath` per platform: Windows `%APPDATA%\LocalLow\Immutable\gods`, Mac `~/Library/Logs/Immutable/gods`, Android `.../com.immutable.godsunchained/files`. These are the game's own standard Unity log locations, not something GUVrs invented. |
| `Views/ViewEngine.cs` | Compiles/caches Handlebars templates from embedded resources (`Shared/header` + page body + `Shared/footer`). |
| `Components/ConcurrentEventListener.cs` | Thread-safe named-event pub/sub, used for the `guvrs://` IPC dispatch. |
| `Components/ControlRenderer.cs` | Marshals a WebView action onto the UI thread if called from a background thread (the log watcher fires on its own timer thread). |
| `Models/*` | Plain DTOs: `PlayerModel`, `PlayerRankModel`, `FriendModel`/`FriendsModel`, `GameStart/Begin/StopModel`, `ResponseOrErrorModel<T>`. |

### Data flow for one game

1. `GuDebugLog` ticks every second; on a `debug.log` change it re-reads the
   whole file (not just the delta — see Known limitations) and scans for the
   next unfired marker line.
2. `OnStart` → sets `_gameId`, pushes it to the UI.
3. `OnGameMode` → caches the numeric game mode (used later to pick the right
   gudecks.com URL variant: ranked/casual/sealed/chaos).
4. `OnBegin` → parses both `PlayerInfo(...)` blocks off one log line into
   `apolloId`/`nickName`, calls `GuApi.GetRank` for both (opponent only if
   `ID != "-1"`), looks up a saved nickname override from the local friends
   list, pushes everything to the WebView, and — if the `auto-open` setting is
   on — opens the opponent's stats page in the system browser.
5. `OnStop`/`OnEnd` → resets state and re-fetches the player's own rank so the
   display doesn't go stale between games.

## Security review — verified findings

Walked every file; here's what's actually happening, not just what the README
claims:

- **Network surface, complete list**: `api.godsunchained.com` (mode list, GET),
  `game-legacy.prod.prod.godsunchained.com` (rank lookup, GET),
  `gudecks.com`/`gumeta.web.app` (opened in the **system browser**, not
  fetched by the app — only on explicit click or the opt-in `auto-open`
  setting), and a GitHub issues link. Grepped the whole `.cs` tree for
  `https?://|HttpClient|WebClient|Process.Start` — nothing else exists.
- **No credentials of any kind** are read, stored, or transmitted. No wallet
  address, private key, or GU login token appears anywhere in this codebase —
  structurally different from `Forging/` and `SellingBot/`, which both need a
  wallet key to sign on-chain actions. GUVrs has no such need since it only
  reads a local log file and calls public read endpoints.
- **File access** is limited to: the game's own log directory (read-only,
  fixed OS-standard path set once at startup, never derived from user/network
  input) and the app's own MAUI `AppDataDirectory` (`settings.json`,
  `friends.json` — both plain local JSON, no secrets).
- **Local JS injection surface**: `_SetValue`/`_SetHtml` build
  `EvaluateJavaScriptAsync` strings via interpolation rather than a proper JS
  API bridge; values are `HttpUtility.HtmlEncode`d in `_SetValue` but *not* in
  `_SetHtml` (used only for a static "Guid must be a number" error and for
  friend-list HTML). Since the WebView content is 100% local (embedded
  templates, no remote page ever loads in it) this isn't an externally
  reachable XSS — worth knowing if this code is ever extended to render
  untrusted data, but not a live vulnerability today.

## Known limitations (upstream, not introduced by this review)

- `GuDebugLog` re-reads the *entire* `debug.log` file on every change tick
  rather than seeking from the last read position — fine for GU's log file
  sizes, but would not scale to a much larger log.
- Log parsing is entirely string-marker based (`line.Contains("...")` +
  `Extract(...)`) — if GU changes its log format, parsing silently stops
  working rather than erroring loudly.
- `MainPage.xaml.cs` mixes `Task.Run(...).Result` (blocking) for the API calls
  instead of `await` — works but blocks the calling thread; not a correctness
  bug in this single-threaded event-driven flow, just not idiomatic async C#.

## Possible next steps

- Nothing outstanding from this review — the app is safe to build/run as-is.
- If the user wants to run this from source rather than the bundled
  `GUvrs-3.0.2-net7.0-windows/` build, they'll need Visual Studio + the MAUI
  workload; see README.md's Building section.
- No action needed on the pre-built binary — it's the official v3.0.2 GitHub
  release matching this exact source tree's tagged version.
