# extract_chat_logs.py
# Workspace tool: extract readable conversation logs from VS Code Copilot Chat sessions.
#
# VS Code stores every Copilot Chat conversation as a JSONL file in:
#   %APPDATA%\Code\User\workspaceStorage\{workspace-hash}\chatSessions\{session-id}.jsonl
#
# This script finds the chatSessions folder for the current workspace, lists all sessions
# with their titles and sizes, and exports selected sessions to readable Markdown logs.
#
# USAGE -- interactive mode (default):
#   python ..\_scripts\extract_chat_logs.py
#
# USAGE -- export specific sessions by ID:
#   python ..\_scripts\extract_chat_logs.py --sessions SESSION_ID1 SESSION_ID2
#
# USAGE -- export all sessions to a folder:
#   python ..\_scripts\extract_chat_logs.py --all --output Chat_Logs
#
# USAGE -- list sessions only (no export):
#   python ..\_scripts\extract_chat_logs.py --list
#
# OUTPUT:
#   Markdown files in the --output folder (default: _scratch\chat_logs\)
#   One file per session: Chat_Log_{title_slug}_{date}.md
#
# RECOMMENDED PRACTICE:
#   At the end of any significant AI-assisted project, run this script to capture the
#   conversation as a permanent record. Store logs in the project's Chat_Logs/ folder.
#   See .github/AI_WORKSPACE_GUIDE.md, Section 13: Chat Log Capture.

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Locate the chatSessions folder for this workspace
# ---------------------------------------------------------------------------

def find_workspace_hash(workspace_root: Path) -> str | None:
    """
    Find the VS Code workspaceStorage hash for the given workspace root.
    VS Code stores a workspace.json in each storage folder that contains the folder URI.
    """
    appdata = os.environ.get("APPDATA", "")
    storage_root = Path(appdata) / "Code" / "User" / "workspaceStorage"
    if not storage_root.exists():
        return None

    target_uri = workspace_root.as_uri().lower()

    for entry in storage_root.iterdir():
        if not entry.is_dir():
            continue
        workspace_json = entry / "workspace.json"
        if workspace_json.exists():
            try:
                data = json.loads(workspace_json.read_text(encoding="utf-8"))
                folder = data.get("folder", "").lower()
                if folder == target_uri:
                    return entry.name
            except Exception:
                continue
    return None


def find_chat_sessions_dir(workspace_root: Path) -> Path | None:
    """Return the chatSessions folder for the current workspace, or None."""
    appdata = os.environ.get("APPDATA", "")
    storage_root = Path(appdata) / "Code" / "User" / "workspaceStorage"

    # Try workspace.json lookup first
    ws_hash = find_workspace_hash(workspace_root)
    if ws_hash:
        candidate = storage_root / ws_hash / "chatSessions"
        if candidate.exists():
            return candidate

    # Fallback: find most recently modified chatSessions folder
    best = None
    best_time = 0.0
    for entry in storage_root.iterdir():
        candidate = entry / "chatSessions"
        if candidate.exists():
            mtime = candidate.stat().st_mtime
            if mtime > best_time:
                best_time = mtime
                best = candidate
    return best


# ---------------------------------------------------------------------------
# Session parsing
# ---------------------------------------------------------------------------

def read_session_metadata(jsonl_path: Path) -> dict:
    """Return title, creation date, and exchange count from a JSONL session file."""
    title = ""
    creation_ts = None
    exchange_count = 0

    try:
        for raw in jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue

            kind = obj.get("kind")

            # kind=0 has session metadata including creationDate
            if kind == 0:
                v = obj.get("v", {})
                if isinstance(v, dict):
                    creation_ts = v.get("creationDate")

            # kind=1 with key "customTitle" has the chat window title
            if kind == 1:
                keys = obj.get("k", [])
                if "customTitle" in keys:
                    title = obj.get("v", "")

            # kind=2 has request arrays
            if kind == 2:
                vals = obj.get("v", [])
                if isinstance(vals, list):
                    exchange_count += len(vals)
    except Exception:
        pass

    # Parse creation date
    created = None
    if creation_ts:
        try:
            created = datetime.fromtimestamp(creation_ts / 1000, tz=timezone.utc)
        except Exception:
            pass

    return {
        "path": jsonl_path,
        "session_id": jsonl_path.stem,
        "title": title or "(untitled)",
        "created": created,
        "exchange_count": exchange_count,
        "size_kb": round(jsonl_path.stat().st_size / 1024, 1),
    }


def list_sessions(sessions_dir: Path) -> list[dict]:
    """Return metadata for all JSONL session files, sorted newest first."""
    sessions = []
    for f in sessions_dir.glob("*.jsonl"):
        meta = read_session_metadata(f)
        sessions.append(meta)
    sessions.sort(key=lambda s: s["created"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return sessions


# ---------------------------------------------------------------------------
# Conversation extraction
# ---------------------------------------------------------------------------

def clean_tool_message(msg: str) -> str:
    """Normalize tool invocation message strings."""
    msg = re.sub(r'(Reading|Read|Ran|Running|Searching|Searched|Edited|Editing)\s+\[\]\(file://[^\)]+\)', r'\1 file', msg)
    msg = re.sub(r'file:///[^\s\]]+', '', msg)
    msg = re.sub(r'%[0-9A-Fa-f]{2}', '', msg)
    return msg.strip()


def extract_response_text(response_items: list) -> str:
    """Extract readable AI response text from a response array."""
    thinking_parts = []
    text_parts = []
    tool_parts = []

    for item in response_items:
        if not isinstance(item, dict):
            continue
        kind = item.get("kind")

        # Plain prose text
        if kind is None and "value" in item and isinstance(item["value"], str):
            val = item["value"].strip()
            if val:
                text_parts.append(val)

        # Thinking blocks
        if kind == "thinking":
            thinking_text = item.get("value", "").strip()
            if thinking_text:
                thinking_parts.append(f"> *[Thinking: {thinking_text[:200]}...]*")

        # Tool invocations
        if kind == "toolInvocationSerialized":
            past = item.get("pastTenseMessage") or item.get("invocationMessage")
            if isinstance(past, dict):
                msg_val = clean_tool_message(past.get("value", ""))
                if msg_val:
                    tool_parts.append(f"*[{msg_val}]*")
            elif isinstance(past, str) and past.strip():
                msg_val = clean_tool_message(past)
                if msg_val:
                    tool_parts.append(f"*[{msg_val}]*")

        # Fallback rendered node structures
        if "supportThemeIcons" in item:
            val = item.get("value")
            if isinstance(val, str) and val.strip():
                text_parts.append(val.strip())

    # Deduplicate text parts
    seen = set()
    deduped = []
    for p in text_parts:
        key = re.sub(r'\s+', ' ', p).strip()
        if key not in seen:
            seen.add(key)
            deduped.append(p)

    parts = []
    if deduped:
        parts.extend(deduped)
    elif thinking_parts:
        parts.extend(thinking_parts[:1])

    seen_tools = set()
    for t in tool_parts:
        if t not in seen_tools and len(t) > 8:
            seen_tools.add(t)
            parts.append(t)

    return "\n\n".join(p for p in parts if p)


def extract_user_message(request_obj: dict) -> str:
    """Extract user message from a request object."""
    msg = request_obj.get("message", {})
    if isinstance(msg, dict):
        text = msg.get("text", "").strip()
        if text:
            return text
        parts = msg.get("parts", [])
        texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
        return " ".join(t for t in texts if t).strip()
    return ""


def extract_exchanges(jsonl_path: Path) -> tuple[str, list[tuple[str, str]]]:
    """Parse a JSONL session file. Returns (session_title, [(user, ai), ...])."""
    session_title = ""
    exchanges = []

    for raw in jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue

        kind = obj.get("kind")

        if kind == 1:
            keys = obj.get("k", [])
            if "customTitle" in keys:
                session_title = obj.get("v", "")

        if kind == 2:
            vals = obj.get("v", [])
            for req in vals:
                if not isinstance(req, dict):
                    continue
                user_text = extract_user_message(req)
                ai_text = extract_response_text(req.get("response", []))
                if user_text or ai_text:
                    exchanges.append((user_text, ai_text))

    return session_title, exchanges


# ---------------------------------------------------------------------------
# Markdown output
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Make a filesystem-safe slug from a string."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[\s_-]+', '_', text)
    return text[:60].strip('_')


def write_markdown(meta: dict, exchanges: list, output_dir: Path) -> Path:
    """Write one session to a Markdown file. Returns the output path."""
    output_dir.mkdir(parents=True, exist_ok=True)

    title = meta["title"]
    created = meta["created"]
    date_str = created.strftime("%Y-%m-%d") if created else "unknown"
    slug = slugify(title)
    filename = f"Chat_Log_{slug}_{date_str}.md"
    out_path = output_dir / filename

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# Chat Log: {title}\n\n")
        if created:
            f.write(f"**Date:** {created.strftime('%B %d, %Y')}\n\n")
        f.write(f"**Session ID:** `{meta['session_id']}`\n\n")
        f.write(f"**Exchanges:** {len(exchanges)}\n\n")
        f.write("---\n\n")

        if not exchanges:
            f.write("*No conversation content could be extracted.*\n")
        else:
            for i, (user, ai) in enumerate(exchanges, 1):
                f.write(f"## Exchange {i}\n\n")
                if user:
                    f.write(f"**User:**\n\n{user}\n\n")
                if ai:
                    f.write(f"**Copilot:**\n\n{ai}\n\n")
                f.write("---\n\n")

    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_session_table(sessions: list[dict]) -> None:
    print(f"\n{'#':<4}  {'Date':<12}  {'Title':<50}  {'Exch':>5}  {'KB':>7}  Session ID")
    print("-" * 110)
    for i, s in enumerate(sessions, 1):
        date_str = s["created"].strftime("%Y-%m-%d") if s["created"] else "?"
        title = s["title"][:48]
        print(f"{i:<4}  {date_str:<12}  {title:<50}  {s['exchange_count']:>5}  {s['size_kb']:>7.1f}  {s['session_id']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Extract Copilot Chat conversation logs to Markdown."
    )
    parser.add_argument("--list", action="store_true", help="List sessions without exporting")
    parser.add_argument("--all", action="store_true", help="Export all sessions")
    parser.add_argument("--sessions", nargs="+", metavar="ID", help="Export specific session IDs")
    parser.add_argument("--output", default=None, metavar="DIR",
                        help="Output folder (default: _scratch/chat_logs/)")
    parser.add_argument("--workspace", default=None, metavar="PATH",
                        help="Workspace root path (default: auto-detect from cwd)")
    args = parser.parse_args()

    # Locate chatSessions folder
    workspace_root = Path(args.workspace) if args.workspace else Path.cwd()
    sessions_dir = find_chat_sessions_dir(workspace_root)

    if not sessions_dir:
        print("ERROR: Could not find VS Code chatSessions folder for this workspace.")
        print("  Ensure you are running from the workspace root or pass --workspace PATH")
        sys.exit(1)

    print(f"Chat sessions folder: {sessions_dir}")

    sessions = list_sessions(sessions_dir)
    if not sessions:
        print("No chat sessions found.")
        sys.exit(0)

    # --list: just print the table
    if args.list:
        print_session_table(sessions)
        return

    # Determine which sessions to export
    if args.all:
        to_export = sessions
    elif args.sessions:
        id_set = set(args.sessions)
        to_export = [s for s in sessions if s["session_id"] in id_set]
        if not to_export:
            print(f"No sessions matched the given IDs: {args.sessions}")
            sys.exit(1)
    else:
        # Interactive: show list, ask user to pick
        print_session_table(sessions)
        raw = input("Enter session numbers to export (e.g. 1 3 5), or 'all': ").strip()
        if raw.lower() == "all":
            to_export = sessions
        else:
            try:
                indices = [int(x) - 1 for x in raw.split()]
                to_export = [sessions[i] for i in indices if 0 <= i < len(sessions)]
            except (ValueError, IndexError):
                print("Invalid selection.")
                sys.exit(1)

    if not to_export:
        print("Nothing to export.")
        return

    # Determine output folder
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = workspace_root / "_scratch" / "chat_logs"

    # Export
    print(f"\nExporting {len(to_export)} session(s) to: {output_dir}\n")
    for meta in to_export:
        _, exchanges = extract_exchanges(meta["path"])
        out_path = write_markdown(meta, exchanges, output_dir)
        size_kb = round(out_path.stat().st_size / 1024, 1)
        print(f"  [OK] {out_path.name}  ({len(exchanges)} exchanges, {size_kb} KB)")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
