#!/usr/bin/env python3
"""
Generate hello/goodbye audio files for the Connected Talking Candle.

Uses gTTS (Google Text-to-Speech) — free, no API key required,
requires internet access only during generation.

Usage:
  pip install gtts
  python3 scripts/generate_audio.py

Options:
  --lang    BCP-47 language code (default: en)
  --hello   Text for the hello message  (default: "Hello, I'm your connected candle.")
  --goodbye Text for the goodbye message (default: "Goodbye, see you next time.")
  --out     Output directory            (default: audio/)

Generated files:
  audio/hello.mp3
  audio/goodbye.mp3
"""

import argparse
import sys
from pathlib import Path

try:
    from gtts import gTTS
except ImportError:
    print("Error: gTTS is not installed.")
    print("Install it with:  pip install gtts")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_HELLO = "Hello, I'm your connected candle. Nice to see you."
DEFAULT_GOODBYE = "Goodbye. Take care, and see you next time."


def generate(text: str, path: Path, lang: str) -> None:
    print(f"  Generating: '{text}'  →  {path}")
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(str(path))
    print(f"  Saved: {path}")


def main():
    parser = argparse.ArgumentParser(description="Generate candle audio files via gTTS")
    parser.add_argument("--lang",    default="en",            help="Language code (e.g. en, fr, es)")
    parser.add_argument("--hello",   default=DEFAULT_HELLO,   help="Hello message text")
    parser.add_argument("--goodbye", default=DEFAULT_GOODBYE, help="Goodbye message text")
    parser.add_argument("--out",     default=str(REPO_ROOT / "audio"), help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Language : {args.lang}")
    print(f"Output   : {out_dir}")
    print()

    generate(args.hello,   out_dir / "hello.mp3",   args.lang)
    generate(args.goodbye, out_dir / "goodbye.mp3", args.lang)

    print()
    print("Done. Run the candle voice with:")
    print("  python3 voice/candle_voice.py")


if __name__ == "__main__":
    main()
