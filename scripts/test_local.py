#!/usr/bin/env python3
"""
Local test runner — Connected Talking Candle
=============================================
Tests each component independently on macOS before deploying to the Pi.
No Raspberry Pi hardware required.

Usage:
  python3 scripts/test_local.py           # run all tests
  python3 scripts/test_local.py sensor    # run one suite
  python3 scripts/test_local.py audio
  python3 scripts/test_local.py messages
  python3 scripts/test_local.py mcp       # launch MCP servers and probe them
"""

import sys
import json
import time
import asyncio
import subprocess
import platform
import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_server(name: str):
    """
    Load one of our local mcp/*.py files by file path, bypassing sys.path.
    This avoids the name collision between our mcp/ directory and the
    installed `mcp` Python package.
    """
    path = REPO_ROOT / "mcp" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# ── Helpers ────────────────────────────────────────────────────────────────────

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
INFO = "\033[34m·\033[0m"

def ok(msg):  print(f"  {PASS} {msg}")
def fail(msg, err=""): print(f"  {FAIL} {msg}" + (f"\n      {err}" if err else ""))
def info(msg): print(f"  {INFO} {msg}")

def section(title):
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


# ── Suite: imports ─────────────────────────────────────────────────────────────

def test_imports():
    section("1. Imports & dependencies")
    results = []

    for module, install_hint in [
        ("mcp",        "pip install mcp"),
        ("gpiozero",   "pip install gpiozero  (or: sudo apt install python3-gpiozero on Pi)"),
        ("gtts",       "pip install gtts"),
    ]:
        try:
            __import__(module)
            ok(f"{module}")
            results.append(True)
        except ImportError:
            if module == "gpiozero":
                info(f"{module} not installed — simulation mode will be used (expected on macOS)")
                results.append(True)
            else:
                fail(f"{module} missing  →  {install_hint}")
                results.append(False)

    for tool, purpose in [
        (["afplay", "--help"],  "MP3 playback"),
        (["say", ""],           "TTS speech"),
    ]:
        try:
            subprocess.run(tool, capture_output=True, timeout=2)
            ok(f"{tool[0]}  ({purpose})")
            results.append(True)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            fail(f"{tool[0]} not found  ({purpose})")
            results.append(False)

    return all(results)


# ── Suite: sensor simulation ───────────────────────────────────────────────────

def test_sensor():
    section("2. Sensor server (simulation mode)")
    results = []

    try:
        sensor_server = _load_server("sensor_server")
        SensorState = sensor_server.SensorState
        state = SensorState()
        ok("SensorState initialised in simulation mode")
        results.append(True)
    except Exception as e:
        fail("SensorState init failed", str(e))
        return False

    # Force a simulated flame-on
    state._sim_state = True
    state._sim_toggle_at = time.time() + 60   # hold it on
    state.poll()

    if state.flame_on:
        ok("flame_on=True after simulated flame detected")
        results.append(True)
    else:
        fail("flame_on should be True after simulation")
        results.append(False)

    time.sleep(0.1)
    state.poll()
    dur = state.session_duration_seconds
    if dur >= 0:
        ok(f"session_duration_seconds = {dur}s")
        results.append(True)
    else:
        fail("session_duration_seconds returned negative")
        results.append(False)

    # Simulate flame off — keep toggle time in the future so _raw_flame()
    # doesn't immediately re-toggle the state before poll() reads it
    state._sim_state = False
    state._sim_toggle_at = time.time() + 60
    state.poll()

    if not state.flame_on:
        ok("flame_on=False after simulated flame off")
        results.append(True)
    else:
        fail("flame_on should be False after flame off")
        results.append(False)

    if state.total_sessions >= 1:
        ok(f"total_sessions = {state.total_sessions}")
        results.append(True)
    else:
        fail("total_sessions should be ≥ 1")
        results.append(False)

    return all(results)


# ── Suite: audio ───────────────────────────────────────────────────────────────

def test_audio():
    section("3. Audio server (macOS)")
    results = []

    try:
        audio_server = _load_server("audio_server")
        _Player = audio_server._Player
        player = _Player()
        ok("_Player initialised")
        results.append(True)
    except Exception as e:
        fail("_Player init failed", str(e))
        return False

    # TTS test — uses macOS `say`
    info("Speaking test phrase via TTS (you should hear: 'Connected Candle test')")
    try:
        status = player.speak("Connected Candle test", language="en")
        time.sleep(3)   # wait for speech to finish
        ok(f"speak() → {status}")
        results.append(True)
    except Exception as e:
        fail("speak() raised an exception", str(e))
        results.append(False)

    # File playback test — only if hello.mp3 exists
    hello = REPO_ROOT / "audio" / "hello.mp3"
    if hello.exists():
        info("Playing hello.mp3 (you should hear the hello message)")
        status = player.play_file(hello)
        time.sleep(4)
        ok(f"play_file(hello.mp3) → {status}")
        results.append(True)
    else:
        info("audio/hello.mp3 not found — skipping file playback test")
        info("Generate it with:  python3 scripts/generate_audio.py")

    return all(results)


# ── Suite: messages ────────────────────────────────────────────────────────────

def test_messages():
    section("4. Messages server")
    results = []

    sample = REPO_ROOT / "data" / "messages.json"
    if not sample.exists():
        fail("data/messages.json not found")
        info("Creating it now from sample data...")
        sample.parent.mkdir(exist_ok=True)
        sample.write_text(json.dumps([
            {"id": "msg_test_001", "sender_name": "Sophie",
             "text_preview": "Thinking of you", "audio_filename": "msg_test_001.mp3",
             "created_at": "2026-04-10T08:30:00"}
        ], indent=2))
        ok("Created data/messages.json with one sample message")

    try:
        messages_server = _load_server("messages_server")
        _load_cached_messages = messages_server._load_cached_messages
        _load_played         = messages_server._load_played
        _save_played         = messages_server._save_played
        messages = _load_cached_messages()
        ok(f"_load_cached_messages() → {len(messages)} message(s)")
        results.append(True)
    except Exception as e:
        fail("messages import failed", str(e))
        return False

    played = _load_played()
    info(f"Played log contains {len(played)} message ID(s)")

    pending = [m for m in messages if m.get("id") not in played]
    ok(f"{len(pending)} pending (unplayed) message(s)")
    results.append(True)

    if pending:
        test_id = pending[0]["id"]
        played.add(test_id)
        _save_played(played)
        ok(f"Marked '{test_id}' as played")

        reloaded = _load_played()
        if test_id in reloaded:
            ok("Played state persisted to disk")
            results.append(True)
        else:
            fail("Played state was not persisted")
            results.append(False)

        # Clean up
        played.discard(test_id)
        _save_played(played)
        info(f"Restored '{test_id}' to unplayed (test cleanup)")

    return all(results)


# ── Suite: MCP server launch ───────────────────────────────────────────────────

async def _probe_mcp_server(script: str) -> bool:
    """Spawn an MCP server as a subprocess and send an initialize request."""
    proc = await asyncio.create_subprocess_exec(
        sys.executable, script,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    init_request = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-runner", "version": "0.1"}
        }
    }) + "\n"

    try:
        proc.stdin.write(init_request.encode())
        await proc.stdin.drain()

        response_line = await asyncio.wait_for(proc.stdout.readline(), timeout=5.0)
        response = json.loads(response_line)

        if "result" in response:
            server_name = response["result"].get("serverInfo", {}).get("name", "unknown")
            ok(f"{Path(script).name}  →  server '{server_name}' responded to initialize")
            proc.terminate()
            return True
        else:
            fail(f"{Path(script).name}  →  unexpected response: {response}")
            proc.terminate()
            return False

    except asyncio.TimeoutError:
        fail(f"{Path(script).name}  →  timed out waiting for initialize response")
        proc.terminate()
        return False
    except Exception as e:
        fail(f"{Path(script).name}  →  {e}")
        proc.kill()
        return False


def test_mcp():
    section("5. MCP servers — launch & initialize")
    results = []

    servers = [
        str(REPO_ROOT / "mcp" / "sensor_server.py"),
        str(REPO_ROOT / "mcp" / "audio_server.py"),
        str(REPO_ROOT / "mcp" / "messages_server.py"),
    ]

    async def run_all():
        for script in servers:
            r = await _probe_mcp_server(script)
            results.append(r)

    asyncio.run(run_all())
    return all(results)


# ── Suite: picoclaw binary ─────────────────────────────────────────────────────

def test_picoclaw():
    section("6. PicoClaw binary")

    try:
        result = subprocess.run(["picoclaw", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            ok(f"picoclaw found: {result.stdout.strip()}")
            return True
        else:
            fail("picoclaw returned a non-zero exit code")
            info(result.stderr.strip())
            return False
    except FileNotFoundError:
        fail("picoclaw binary not found in PATH")
        info("Download from: https://github.com/sipeed/picoclaw/releases")
        info("Then:  sudo mv picoclaw /usr/local/bin/  &&  chmod +x /usr/local/bin/picoclaw")
        return False


# ── Main ───────────────────────────────────────────────────────────────────────

SUITES = {
    "imports":  test_imports,
    "sensor":   test_sensor,
    "audio":    test_audio,
    "messages": test_messages,
    "mcp":      test_mcp,
    "picoclaw": test_picoclaw,
}

def main():
    args = sys.argv[1:]
    to_run = [SUITES[a] for a in args if a in SUITES] or list(SUITES.values())

    print("\nConnected Talking Candle — Local Test Runner")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python:   {sys.version.split()[0]}")

    passed, failed = 0, 0
    for suite in to_run:
        ok_result = suite()
        if ok_result:
            passed += 1
        else:
            failed += 1

    print(f"\n{'─' * 50}")
    print(f"  Results: {passed} passed, {failed} failed")
    if failed == 0:
        print(f"  {PASS} All tests passed — ready to deploy")
    else:
        print(f"  {FAIL} Fix failing tests before deploying to the Pi")
    print()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
