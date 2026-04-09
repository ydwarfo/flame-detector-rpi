#!/usr/bin/env python3
"""
MCP Server — Messages
======================
Exposes the gift-giver message queue to PicoClaw as MCP tools.

Messages are fetched from the cloud API and cached locally so the
candle works offline. Played message IDs are tracked to prevent repeats.

Tools provided:
  get_pending_messages()           → list of unplayed messages
  mark_message_played(message_id)  → records message as played
  get_message_count()              → how many unplayed messages are waiting

PicoClaw spawns this as a subprocess and communicates over stdio (JSON-RPC).
"""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = REPO_ROOT / "config.json"
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

MESSAGE_CACHE = DATA_DIR / "messages.json"
PLAYED_LOG = DATA_DIR / "played_messages.json"


def _load_config() -> dict:
    try:
        return json.loads(CONFIG_FILE.read_text())
    except Exception:
        return {}


def _load_played() -> set:
    try:
        if PLAYED_LOG.exists():
            return set(json.loads(PLAYED_LOG.read_text()))
    except Exception:
        pass
    return set()


def _save_played(played: set):
    PLAYED_LOG.write_text(json.dumps(sorted(played), indent=2))


def _load_cached_messages() -> list:
    try:
        if MESSAGE_CACHE.exists():
            return json.loads(MESSAGE_CACHE.read_text())
    except Exception:
        pass
    return []


def _fetch_messages_from_cloud(api_base: str, device_id: str) -> list:
    """
    Fetch pending messages from the cloud API.
    Returns a list of message dicts: {id, sender_name, audio_url, text_preview, created_at}
    Falls back to cache if the request fails.
    """
    try:
        import urllib.request
        url = f"{api_base}/devices/{device_id}/messages/pending"
        with urllib.request.urlopen(url, timeout=5) as resp:
            messages = json.loads(resp.read())
            MESSAGE_CACHE.write_text(json.dumps(messages, indent=2))
            return messages
    except Exception:
        # Offline — return cached messages
        return _load_cached_messages()


# ── MCP server ─────────────────────────────────────────────────────────────────

server = Server("candle-messages")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_pending_messages",
            description=(
                "Returns a list of unplayed voice messages sent by the gift-giver. "
                "Each message includes the sender name, a text preview, and an audio filename. "
                "Call this when the candle is lit to check if there are waiting messages."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "boolean",
                        "description": "If true, fetch fresh messages from the cloud. Defaults to false (use cache).",
                        "default": False,
                    }
                },
                "required": [],
            },
        ),
        types.Tool(
            name="mark_message_played",
            description=(
                "Mark a message as played so it is not delivered again. "
                "Always call this after playing a message."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "message_id": {
                        "type": "string",
                        "description": "The ID of the message that was just played.",
                    }
                },
                "required": ["message_id"],
            },
        ),
        types.Tool(
            name="get_message_count",
            description=(
                "Returns how many unplayed messages are waiting. "
                "Use this for a quick check before deciding whether to mention waiting messages."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    cfg = _load_config()
    api_base = cfg.get("cloud", {}).get("api_base", "")
    device_id = cfg.get("device", {}).get("id", "")
    played = _load_played()

    if name == "get_pending_messages":
        refresh = arguments.get("refresh", False)
        if refresh and api_base and device_id:
            all_messages = _fetch_messages_from_cloud(api_base, device_id)
        else:
            all_messages = _load_cached_messages()

        pending = [m for m in all_messages if m.get("id") not in played]
        result = {
            "count": len(pending),
            "messages": pending,
        }

    elif name == "mark_message_played":
        message_id = arguments.get("message_id", "")
        if message_id:
            played.add(message_id)
            _save_played(played)
            result = {"status": "marked", "message_id": message_id}
        else:
            result = {"error": "message_id is required"}

    elif name == "get_message_count":
        all_messages = _load_cached_messages()
        pending = [m for m in all_messages if m.get("id") not in played]
        result = {"count": len(pending)}

    else:
        result = {"error": f"Unknown tool: {name}"}

    return [types.TextContent(type="text", text=json.dumps(result))]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
