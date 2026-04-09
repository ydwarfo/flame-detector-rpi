#!/usr/bin/env python3
"""
MCP Server — Audio
===================
Exposes speaker playback to PicoClaw as MCP tools.

Tools provided:
  play_file(filename)          → plays audio/<filename> via mpg123 / afplay
  speak(text, language?)       → TTS via espeak (Linux) or say (macOS)
  get_audio_status()           → whether audio is currently playing

PicoClaw spawns this as a subprocess and communicates over stdio (JSON-RPC).
"""

import asyncio
import json
import platform
import subprocess
import threading
from pathlib import Path

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO_ROOT / "audio"
CONFIG_FILE = REPO_ROOT / "config.json"
IS_LINUX = platform.system() == "Linux"


def _load_audio_config() -> dict:
    defaults = {"output": "headphone", "volume_percent": 80}
    try:
        data = json.loads(CONFIG_FILE.read_text())
        defaults.update(data.get("audio", {}))
    except Exception:
        pass
    return defaults


# ── Playback state ─────────────────────────────────────────────────────────────

class _Player:
    def __init__(self):
        cfg = _load_audio_config()
        self.volume = cfg["volume_percent"]
        self._lock = threading.Lock()
        self.playing = False
        self.current = ""

        if IS_LINUX:
            self._configure_alsa(cfg["output"], self.volume)

    @staticmethod
    def _configure_alsa(output: str, volume: int):
        mapping = {"auto": 0, "headphone": 1, "hdmi": 2}
        numid = mapping.get(output, 0)
        if output != "usb":
            subprocess.run(["amixer", "cset", f"numid=3", str(numid)],
                           check=False, capture_output=True)
        for control in ("Master", "PCM"):
            subprocess.run(["amixer", "set", control, f"{volume}%"],
                           check=False, capture_output=True)

    def play_file(self, path: Path) -> str:
        if not path.exists():
            return f"error: file not found: {path}"
        threading.Thread(target=self._play_blocking, args=(path,), daemon=True).start()
        return f"playing: {path.name}"

    def speak(self, text: str, language: str = "en") -> str:
        threading.Thread(target=self._speak_blocking, args=(text, language), daemon=True).start()
        return f"speaking: {text[:60]}"

    def _play_blocking(self, path: Path):
        with self._lock:
            self.playing = True
            self.current = path.name
        try:
            if IS_LINUX:
                subprocess.run(["mpg123", "-q", "-g", str(self.volume), str(path)], check=False)
            else:
                subprocess.run(["afplay", "-v", str(self.volume / 100), str(path)], check=False)
        finally:
            with self._lock:
                self.playing = False
                self.current = ""

    def _speak_blocking(self, text: str, language: str):
        with self._lock:
            self.playing = True
            self.current = f"[tts] {text[:30]}"
        try:
            if IS_LINUX:
                subprocess.run(["espeak", "-v", language, "-s", "140", "-a", "150", text],
                               check=False, capture_output=True)
            else:
                subprocess.run(["say", text], check=False)
        finally:
            with self._lock:
                self.playing = False
                self.current = ""


_player = _Player()

# ── MCP server ─────────────────────────────────────────────────────────────────

server = Server("candle-audio")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="play_file",
            description=(
                "Play a pre-generated audio file from the audio/ directory. "
                "Use for high-quality pre-recorded clips (hello, goodbye, personality phrases). "
                "Prefer this over speak() when the file exists."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename inside the audio/ directory, e.g. 'hello.mp3'",
                    }
                },
                "required": ["filename"],
            },
        ),
        types.Tool(
            name="speak",
            description=(
                "Synthesise and speak a short phrase aloud using the system TTS engine. "
                "Use for dynamic, generated messages. Keep text under 30 words for best results."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The phrase to speak. Keep it short — under 30 words.",
                    },
                    "language": {
                        "type": "string",
                        "description": "BCP-47 language code, e.g. 'en', 'fr'. Defaults to 'en'.",
                        "default": "en",
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="get_audio_status",
            description="Returns whether audio is currently playing. Use to avoid interrupting ongoing speech.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "play_file":
        filename = arguments.get("filename", "")
        result = {"status": _player.play_file(AUDIO_DIR / filename)}

    elif name == "speak":
        text = arguments.get("text", "")
        language = arguments.get("language", "en")
        result = {"status": _player.speak(text, language)}

    elif name == "get_audio_status":
        with _player._lock:
            result = {"playing": _player.playing, "current": _player.current}

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
