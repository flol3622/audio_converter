from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class ConversionError(Exception):
    """Raised when an audio conversion fails."""


class AudioConverter:
    """Convert audio files using FFmpeg.

    The converter streams data through FFmpeg, making it suitable for very long
    recordings without loading them entirely into memory.
    """

    def __init__(self, ffmpeg_path: str = "ffmpeg") -> None:
        self.ffmpeg_path = ffmpeg_path
        if shutil.which(self.ffmpeg_path) is None:
            raise ConversionError(
                "FFmpeg is required but was not found on PATH. "
                "Install FFmpeg and try again."
            )

    def convert_m4a_to_mp3(
        self,
        input_path: Path | str,
        output_path: Optional[Path | str] = None,
        *,
        bitrate: str = "192k",
        normalize: bool = False,
        overwrite: bool = False,
    ) -> Path:
        """Convert an M4A file to MP3.

        Args:
            input_path: Path to the source `.m4a` file.
            output_path: Optional destination path. Defaults to the same stem
                with an `.mp3` extension in the input directory.
            bitrate: Target audio bitrate for the MP3 output.
            normalize: Apply EBU R128 loudness normalization for consistent
                output levels.
            overwrite: Replace existing output files if ``True``.

        Returns:
            Path to the converted MP3 file.
        """

        input_path = Path(input_path)
        if not input_path.exists():
            raise ConversionError(f"Input file does not exist: {input_path}")

        if output_path is None:
            output_path = input_path.with_suffix(".mp3")
        else:
            output_path = Path(output_path)

        if output_path.exists() and not overwrite:
            raise ConversionError(
                f"Output file already exists: {output_path}. "
                "Use overwrite=True to replace it."
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".mp3", dir=output_path.parent, delete=False
        )
        temp_path = Path(temp_file.name)
        temp_file.close()

        filters = []
        if normalize:
            filters.append("loudnorm")

        command = [
            self.ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-i",
            str(input_path),
            "-vn",
            "-acodec",
            "libmp3lame",
            "-b:a",
            bitrate,
            "-ar",
            "44100",
            "-map_metadata",
            "0",
        ]

        if filters:
            command.extend(["-af", ",".join(filters)])

        command.append(str(temp_path))

        try:
            subprocess.run(command, check=True)
            temp_path.replace(output_path)
        except subprocess.CalledProcessError as exc:  # pragma: no cover - thin wrapper
            raise ConversionError(
                "FFmpeg failed to convert the file. Ensure the input is valid "
                "and FFmpeg supports the necessary codecs."
            ) from exc
        finally:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

        return output_path
