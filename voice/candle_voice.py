#!/usr/bin/env python3
"""
Connected Talking Candle — Voice Module
========================================

Plays a voice message when the candle is lit ("Hello") and when it
goes out ("Goodbye").  Audio files are looked up in the audio/ directory
next to this repo.  Falls back to espeak (system TTS) when no file is
found so the script always runs, even without pre-generated audio.

Hardware:
  - IR Flame Sensor  → GPIO17 (DO pin)
  - Speaker          → 3.5mm jack, USB audio, or I2S amp

Audio playback (no display/SDL required — works headless):
  - Linux / Raspberry Pi  : mpg123 (MP3) or aplay (WAV) via ALSA
  - macOS (dev machine)   : afplay (built-in)
  - Last resort           : espeak system TTS

Run on Pi:
  python3 voice/candle_voice.py

Run on macOS for development (simulation mode, no GPIO required):
  python3 voice/candle_voice.py
"""

import sys
import time
import signal
import json
import logging
import threading
import subprocess
import platform
from pathlib import Path

# ── Optional GPIO ──────────────────────────────────────────────────────────────
try:
    from gpiozero import InputDevice
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = REPO_ROOT / "audio"
CONFIG_FILE = REPO_ROOT / "config.json"

# ── Audio output constants (Linux/ALSA) ───────────────────────────────────────
# amixer numid=3: 0=auto, 1=headphone jack, 2=HDMI
_ALSA_OUTPUT = {"auto": 0, "headphone": 1, "hdmi": 2}


def _load_config() -> dict:
    defaults = {
        "gpio": {"flame_sensor_pin": 17},
        "detection": {"check_interval": 0.5, "debounce_time": 2.0},
        "voice": {
            "enabled": True,
            "hello_file": "hello.mp3",
            "goodbye_file": "goodbye.mp3",
            "language": "en",
        },
        "audio": {
            "output": "headphone",   # headphone | hdmi | usb | auto
            "volume_percent": 80,    # 0–100, applied via amixer on Linux
        },
        "logging": {"level": "INFO"},
    }
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                loaded = json.load(f)
            for key, value in loaded.items():
                if isinstance(value, dict) and key in defaults:
                    defaults[key].update(value)
                else:
                    defaults[key] = value
    except Exception as e:
        print(f"Warning: could not load config.json ({e}), using defaults.")
    return defaults


# ── Audio player ───────────────────────────────────────────────────────────────

class AudioPlayer:
    """
    Plays MP3/WAV files using the system CLI player — no SDL, no display needed.

    Linux / Raspberry Pi:
      MP3  → mpg123 -q -g <vol> <file>
      WAV  → aplay -q <file>
      TTS  → espeak

    macOS (development):
      MP3/WAV → afplay -v <vol_0_1> <file>
      TTS     → say

    Volume and output routing are configured once at startup via amixer (Linux only).
    """

    _LOG = logging.getLogger("AudioPlayer")

    def __init__(self, output: str = "headphone", volume_percent: int = 80):
        self._lock = threading.Lock()
        self._playing = False
        self._volume_percent = max(0, min(100, volume_percent))
        self._is_linux = platform.system() == "Linux"

        if self._is_linux:
            self._configure_alsa(output, volume_percent)

    # ── ALSA setup (Pi only) ───────────────────────────────────────────────────

    def _configure_alsa(self, output: str, volume_percent: int) -> None:
        """Route audio output and set master volume via amixer."""
        numid = _ALSA_OUTPUT.get(output, 0)
        if output != "usb":
            # Route to the right output (skip for USB — handled by ALSA device index)
            self._run_silent(["amixer", "cset", "numid=3", str(numid)])

        # Set master volume
        self._run_silent(["amixer", "set", "Master", f"{volume_percent}%"])
        # Some Pi setups use PCM instead of Master
        self._run_silent(["amixer", "set", "PCM", f"{volume_percent}%"])

        self._LOG.info(f"ALSA: output={output}, volume={volume_percent}%")

    @staticmethod
    def _run_silent(cmd: list[str]) -> None:
        """Run a shell command, ignoring errors (amixer may not have all controls)."""
        try:
            subprocess.run(cmd, check=False, capture_output=True)
        except FileNotFoundError:
            pass  # amixer not available — not a Pi

    # ── Public API ─────────────────────────────────────────────────────────────

    def play(self, audio_path: Path, fallback_text: str = "") -> None:
        """Trigger playback in a daemon thread (non-blocking)."""
        threading.Thread(
            target=self._play_blocking,
            args=(audio_path, fallback_text),
            daemon=True,
        ).start()

    # ── Internal ───────────────────────────────────────────────────────────────

    def _play_blocking(self, audio_path: Path, fallback_text: str) -> None:
        with self._lock:
            if self._playing:
                return  # already playing — don't interrupt
            self._playing = True
        try:
            if audio_path.exists():
                self._play_file(audio_path)
            elif fallback_text:
                self._speak(fallback_text)
            else:
                self._LOG.warning(f"Audio file not found and no fallback: {audio_path}")
        except Exception as e:
            self._LOG.error(f"Playback error: {e}")
        finally:
            self._playing = False

    def _play_file(self, path: Path) -> None:
        suffix = path.suffix.lower()
        if self._is_linux:
            if suffix == ".mp3":
                vol_arg = str(self._volume_percent)
                subprocess.run(["mpg123", "-q", "-g", vol_arg, str(path)], check=False)
            else:
                subprocess.run(["aplay", "-q", str(path)], check=False)
        else:
            # macOS — afplay volume is 0.0–1.0
            vol = self._volume_percent / 100
            subprocess.run(["afplay", "-v", str(vol), str(path)], check=False)

    def _speak(self, text: str) -> None:
        if self._is_linux:
            try:
                subprocess.run(["espeak", "-s", "140", "-a", "150", text],
                               check=False, capture_output=True)
            except FileNotFoundError:
                self._LOG.warning(f"espeak not found. Would have said: '{text}'")
        else:
            try:
                subprocess.run(["say", text], check=False)
            except FileNotFoundError:
                self._LOG.warning(f"'say' not found. Would have said: '{text}'")


# ── Flame sensor ───────────────────────────────────────────────────────────────

class FlameSensor:
    """
    Wraps gpiozero InputDevice.  In simulation mode (no GPIO), alternates
    state every 5 s so the voice logic can be tested on a dev machine.
    """

    def __init__(self, pin: int):
        self._sensor = None
        self._simulation = not GPIO_AVAILABLE
        self._sim_state = False
        self._sim_last_toggle = time.time()

        if not self._simulation:
            self._sensor = InputDevice(pin)

    @property
    def flame_present(self) -> bool:
        if self._simulation:
            # Toggle every 5 s so you can hear hello/goodbye on a dev machine
            now = time.time()
            if now - self._sim_last_toggle >= 5.0:
                self._sim_state = not self._sim_state
                self._sim_last_toggle = now
            return self._sim_state
        return not self._sensor.is_active  # sensor is LOW when flame present

    def close(self):
        if self._sensor:
            self._sensor.close()


# ── Main candle voice loop ─────────────────────────────────────────────────────

class CandleVoice:
    """Monitors the flame sensor and speaks when the candle is lit or blown out."""

    def __init__(self):
        self.config = _load_config()
        self._setup_logging()
        self.logger = logging.getLogger("CandleVoice")

        voice_cfg = self.config["voice"]
        audio_cfg = self.config["audio"]
        self.player = AudioPlayer(
            output=audio_cfg["output"],
            volume_percent=audio_cfg["volume_percent"],
        )
        self.hello_path = AUDIO_DIR / voice_cfg["hello_file"]
        self.goodbye_path = AUDIO_DIR / voice_cfg["goodbye_file"]

        gpio_pin = self.config["gpio"]["flame_sensor_pin"]
        self.sensor = FlameSensor(gpio_pin)

        self._running = False
        self._flame_state = False  # last confirmed state

        signal.signal(signal.SIGINT, self._on_signal)
        signal.signal(signal.SIGTERM, self._on_signal)

    # ── Setup ──────────────────────────────────────────────────────────────────

    def _setup_logging(self):
        level = getattr(logging, self.config["logging"]["level"].upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def _on_signal(self, signum, frame):
        self.logger.info(f"Signal {signum} received — stopping.")
        self._running = False

    # ── Core loop ──────────────────────────────────────────────────────────────

    def run(self):
        sim = not GPIO_AVAILABLE
        mode = "SIMULATION" if sim else f"GPIO{self.config['gpio']['flame_sensor_pin']}"
        self.logger.info(f"Connected Talking Candle started  [{mode}]")
        self.logger.info(f"Hello  audio: {self.hello_path}")
        self.logger.info(f"Goodbye audio: {self.goodbye_path}")

        if not self.config["voice"]["enabled"]:
            self.logger.warning("Voice is disabled in config.json — exiting.")
            return

        if sim:
            self.logger.warning("GPIO unavailable — running in simulation mode (state toggles every 5 s).")

        check_interval = self.config["detection"]["check_interval"]
        debounce_time = self.config["detection"]["debounce_time"]

        # Debounce: candidate state must hold for debounce_time before confirming
        candidate_state = False
        candidate_since: float | None = None

        self._running = True
        try:
            while self._running:
                raw = self.sensor.flame_present
                now = time.time()

                if raw != self._flame_state:
                    # A change is happening — start or extend the debounce window
                    if raw != candidate_state:
                        candidate_state = raw
                        candidate_since = now
                    elif candidate_since is not None and (now - candidate_since) >= debounce_time:
                        # Change confirmed — apply it
                        self._flame_state = candidate_state
                        candidate_since = None
                        self._on_state_change(self._flame_state)
                else:
                    # Back to current confirmed state — reset candidate
                    candidate_state = self._flame_state
                    candidate_since = None

                time.sleep(check_interval)

        finally:
            self.sensor.close()
            self.logger.info("Stopped.")

    def _on_state_change(self, flame_on: bool):
        if flame_on:
            self.logger.info("Flame ON  → playing hello")
            self.player.play(self.hello_path, fallback_text="Hello")
        else:
            self.logger.info("Flame OFF → playing goodbye")
            self.player.play(self.goodbye_path, fallback_text="Goodbye")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    candle = CandleVoice()
    candle.run()


if __name__ == "__main__":
    main()
