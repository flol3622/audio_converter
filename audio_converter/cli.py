from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .converter import AudioConverter, ConversionError


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert M4A files to MP3 using FFmpeg",
    )
    parser.add_argument("input", type=Path, help="Path to the source .m4a file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Destination path for the .mp3 file (defaults to same name as input)",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        default="192k",
        help="Target bitrate for the MP3 output (e.g. 192k, 256k)",
    )
    parser.add_argument(
        "-n",
        "--normalize",
        action="store_true",
        help="Apply loudness normalization (EBU R128)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace output file if it already exists",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    converter = AudioConverter()
    try:
        result = converter.convert_m4a_to_mp3(
            input_path=args.input,
            output_path=args.output,
            bitrate=args.bitrate,
            normalize=args.normalize,
            overwrite=args.overwrite,
        )
    except ConversionError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Conversion complete: {result}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
