# GUVrs

A third-party companion app for Gods Unchained (GU) by developer Timothy Meadows
(GitHub: [TimothyMeadows/GUvrs](https://github.com/TimothyMeadows/GUvrs), MIT licensed).
It watches the game's own local debug log while you play and displays your and
your opponent's profile ID, name, rating, and win/loss points in real time. You
can click an opponent to open their stats on a third-party site (gudecks.com or
gumeta.web.app), or save them as a "friend" with a custom nickname.

This folder holds two things:

| Path | What it is |
|------|------------|
| `GUvrs-main/GUvrs-main/` | Full C# source (.NET MAUI), downloaded from GitHub |
| `GUvrs-3.0.2-net7.0-windows/` | Pre-built, self-contained Windows binary for release v3.0.2 (matches the source's official release tag) |

## What it does

- Watches `%APPDATA%\LocalLow\Immutable\gods\debug.log` (the game's own Unity
  log file — same location on every GU install) for lines marking game
  start/mode/players/end.
- Parses out your and your opponent's profile GUID and nickname from those lines.
- Calls two read-only endpoints on official GU domains (`api.godsunchained.com`,
  `game-legacy.prod.prod.godsunchained.com`) to fetch rank/win-loss data for
  both players.
- Displays everything in an embedded WebView UI.
- Lets you save a local "friends" list (nickname per GUID) to a JSON file in
  the app's own data directory.
- Optionally auto-opens (or lets you click to open) an opponent's stats page
  on gudecks.com or gumeta.web.app.

It does **not** touch a wallet, private key, or any GU account credentials —
this is a read-only spectator/informational tool, unlike other GU third-party
tools in this workspace (see `Forging/` and `SellingBot/`).

## Install & run (pre-built binary)

1. Extract `GUvrs-3.0.2-net7.0-windows/` anywhere.
2. Run `GUvrs.exe`.
3. Launch it any time before, during, or after starting a GU game — it just
   watches the log file. There may be a short delay after a game event before
   the info appears (depends on disk speed and when the game writes to its log).

Settings (theme, auto-open, stats site) are available from within the app; use
the "open settings folder" option in-app to find `settings.json` /
`friends.json` on disk if you need to inspect or reset them by hand.

## Building from source

Requires Visual Studio with the .NET MAUI workload, targeting `net7.0-windows10.0.19041.0`
(or `net7.0-maccatalyst15.4` for Mac). From `GUvrs-main/GUvrs-main/GUvrs/`:

```bash
dotnet publish GUvrs.csproj -f net7.0-windows10.0.19041.0
```

The MAUI multi-targeting publish step can be finicky in Visual Studio — see the
upstream README (`GUvrs-main/GUvrs-main/README.md`) for the `WindowsPackageType`
workaround if a publish fails.

## Dependencies

Three NuGet packages, all well-known: `Handlebars.Net` (renders the UI from
local `.mustache` templates embedded in the app), `MemoryCache.NetCore` (local
settings cache), `Microsoft.Extensions.Logging.Debug` (official MS package).

## Security review summary

Reviewed the full source (~1,000 lines of C#) line by line. Findings:

- Every network call goes to an official GU/Immutable domain, or (only on
  explicit click or an opt-in setting) to gudecks.com / gumeta.web.app for
  public stats — no other third-party endpoint anywhere.
- No wallet, private key, or GU login credential is read, stored, or
  transmitted anywhere in the codebase.
- Local file access is limited to the game's own log directory (read-only) and
  the app's own data directory (`settings.json`, `friends.json`).
- MIT licensed with full source available — nothing is obfuscated or compiled
  without a matching source release.

See `HANDOFF.md` for the technical/architecture breakdown.
