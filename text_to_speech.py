"""Convert a UTF-8 text file into an MP3 using Google Text-to-Speech."""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from gtts import gTTS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a text file into an MP3 with Google Text-to-Speech."
    )
    parser.add_argument(
        "--input", "-i", help="UTF-8 text file to read (default: phrases_<lang>.txt)"
    )
    parser.add_argument(
        "--output", "-o", help="MP3 file to create (default: all_phrases_<lang>.mp3)"
    )
    parser.add_argument(
        "--lang", "-l", default="fr", help="gTTS language code, for example fr or en"
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Playback speed from 0.5x to 2.0x (requires ffmpeg when not 1.0x)",
    )
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Ask gTTS to generate its slower speech option",
    )
    args = parser.parse_args()
    if not 0.5 <= args.speed <= 2.0:
        parser.error("--speed must be between 0.5 and 2.0")
    return args


def change_speed(input_path: Path, output_path: Path, speed: float) -> None:
    """Use ffmpeg's atempo filter to adjust the generated MP3 speed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".mp3", prefix="tts_", dir=output_path.parent, delete=False
        ) as temp_file:
            temporary_output = Path(temp_file.name)
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(input_path),
                "-filter:a",
                f"atempo={speed}",
                "-vn",
                str(temporary_output),
            ],
            check=True,
        )
        os.replace(temporary_output, output_path)
    finally:
        if temporary_output is not None:
            temporary_output.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input or f"phrases_{args.lang}.txt")
    output_path = Path(args.output or f"all_phrases_{args.lang}.mp3")

    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}")
        return 1

    try:
        text = input_path.read_text(encoding="utf-8").strip()
        if not text:
            print(f"Error: input file is empty: {input_path}")
            return 1

        phrase_count = sum(bool(line.strip()) for line in text.splitlines())
        print(f"Reading {input_path} ({phrase_count} non-empty lines)")
        print(f"Language: {args.lang}; requested speed: {args.speed:g}x")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if args.speed == 1.0:
            gTTS(text=text, lang=args.lang, slow=args.slow).save(str(output_path))
        else:
            # Generate at normal speed first, then use ffmpeg to change the rate.
            with tempfile.NamedTemporaryFile(
                suffix=".mp3", prefix="tts_source_", delete=False
            ) as temp_file:
                source_path = Path(temp_file.name)
            try:
                gTTS(text=text, lang=args.lang, slow=args.slow).save(str(source_path))
                change_speed(source_path, output_path, args.speed)
            finally:
                source_path.unlink(missing_ok=True)

        print(f"Created: {output_path}")
        return 0
    except FileNotFoundError as error:
        if error.filename == "ffmpeg":
            print("Error: ffmpeg was not found. Install ffmpeg to use --speed other than 1.")
        else:
            print(f"Error: {error}")
        return 1
    except subprocess.CalledProcessError:
        print("Error: ffmpeg could not adjust the audio speed.")
        return 1
    except Exception as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
