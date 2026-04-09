#!/usr/bin/env python3
"""
MCP Server — Sensor
====================
Exposes flame sensor state and burn session data to PicoClaw as MCP tools.

Tools provided:
  get_flame_state()    → current flame on/off and duration
  get_burn_session()   → active session details
  get_burn_history()   → lifetime burn statistics

PicoClaw spawns this as a subprocess and communicates over stdio (JSON-RPC).

Run standalone for testing:
  python3 mcp/sensor_server.py
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

# ── GPIO (optional — simulation mode on macOS) ────────────────────────────────
try:
    from gpiozero import InputDevice
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = REPO_ROOT / "config.json"
HISTORY_FILE = REPO_ROOT / "data" / "burn_history.json"
HISTORY_FILE.parent.mkdir(exist_ok=True)


def _load_config() -> dict:
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception:
        return {"gpio": {"flame_sensor_pin": 17}}


# ── Sensor state (shared across tool calls) ───────────────────────────────────

class SensorState:
    def __init__(self):
        cfg = _load_config()
        pin = cfg["gpio"]["flame_sensor_pin"]

        self._simulation = not GPIO_AVAILABLE
        self._sensor = InputDevice(pin) if not self._simulation else None
        self._sim_state = False
        self._sim_toggle_at = time.time() + 5

        self.flame_on = False
        self.session_start: float | None = None
        self.total_sessions = 0
        self.total_burn_seconds = 0

        self._load_history()

    def _load_history(self):
        try:
            if HISTORY_FILE.exists():
                data = json.loads(HISTORY_FILE.read_text())
                self.total_sessions = data.get("total_sessions", 0)
                self.total_burn_seconds = data.get("total_burn_seconds", 0)
        except Exception:
            pass

    def _save_history(self):
        data = {
            "total_sessions": self.total_sessions,
            "total_burn_seconds": self.total_burn_seconds,
            "last_updated": datetime.now().isoformat(),
        }
        HISTORY_FILE.write_text(json.dumps(data, indent=2))

    def _raw_flame(self) -> bool:
        if self._simulation:
            now = time.time()
            if now >= self._sim_toggle_at:
                self._sim_state = not self._sim_state
                self._sim_toggle_at = now + 5
            return self._sim_state
        return not self._sensor.is_active

    def poll(self):
        """Update internal state. Called before each tool invocation."""
        raw = self._raw_flame()
        now = time.time()

        if raw and not self.flame_on:
            # Flame just came on
            self.flame_on = True
            self.session_start = now
            self.total_sessions += 1

        elif not raw and self.flame_on:
            # Flame just went off
            if self.session_start:
                self.total_burn_seconds += int(now - self.session_start)
            self.flame_on = False
            self.session_start = None
            self._save_history()

    @property
    def session_duration_seconds(self) -> int:
        if self.flame_on and self.session_start:
            return int(time.time() - self.session_start)
        return 0

    @property
    def total_burn_hours(self) -> float:
        return round(self.total_burn_seconds / 3600, 2)


_state = SensorState()

# ── MCP server ─────────────────────────────────────────────────────────────────

server = Server("candle-sensor")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_flame_state",
            description=(
                "Returns whether the candle is currently burning and for how long. "
                "Use this to decide whether to greet the owner or say goodbye."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_burn_session",
            description=(
                "Returns details about the current or most recent burn session. "
                "Use this to add context to your message (e.g. 'you've been burning for 20 minutes')."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_burn_history",
            description=(
                "Returns lifetime burn statistics: total sessions and total hours burned. "
                "Use this to personalise messages (e.g. milestone reactions)."
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
    _state.poll()

    if name == "get_flame_state":
        result = {
            "flame_on": _state.flame_on,
            "session_duration_seconds": _state.session_duration_seconds,
            "simulation_mode": _state._simulation,
        }

    elif name == "get_burn_session":
        result = {
            "active": _state.flame_on,
            "duration_seconds": _state.session_duration_seconds,
            "started_at": (
                datetime.fromtimestamp(_state.session_start).isoformat()
                if _state.session_start else None
            ),
        }

    elif name == "get_burn_history":
        result = {
            "total_sessions": _state.total_sessions,
            "total_burn_hours": _state.total_burn_hours,
            "total_burn_seconds": _state.total_burn_seconds,
        }

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
