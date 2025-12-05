from __future__ import annotations

from pathlib import Path
from typing import Optional

from audio_converter import AudioConverter


class Predictor:
    """Replicate predictor that converts M4A uploads to MP3."""

    def __init__(self) -> None:
        self.converter = AudioConverter()

    def predict(
        self,
        audio: Path,
        bitrate: str = "192k",
        normalize: bool = False,
        overwrite: bool = True,
    ) -> Path:
        """Convert an input M4A file to MP3 and return the output path."""

        input_path = Path(audio)
        output_path: Optional[Path] = input_path.with_suffix(".mp3")
        return self.converter.convert_m4a_to_mp3(
            input_path=input_path,
            output_path=output_path,
            bitrate=bitrate,
            normalize=normalize,
            overwrite=overwrite,
        )
