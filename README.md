# audio_converter

A lightweight, FFmpeg-powered utility to convert **M4A** recordings to **MP3**.
The converter streams data directly through FFmpeg, making it reliable for very
long audio files without loading them into memory.

## Requirements

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/) available on your `PATH` (includes `libmp3lame`)

## Quickstart

The project works well with [uv](https://github.com/astral-sh/uv) for fast,
locked installs. A classic `venv` + `pip` setup also works.

### With uv (recommended locally)

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv run python -m audio_converter.cli --help
```

### With pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m audio_converter.cli --help
```

### uv-oriented project style

If you prefer uv to manage dependencies, use the optional `dev` group for
tooling and run commands through uv:

```bash
uv sync --extra dev
uv run python -m audio_converter.cli --help
uv run pytest
```

### Convert a file

```bash
python -m audio_converter.cli path/to/input.m4a -o path/to/output.mp3
```

### Additional options

- `-b/--bitrate`: Set MP3 bitrate (e.g., `192k`, `256k`).
- `-n/--normalize`: Apply EBU R128 loudness normalization to smooth out volume
  on long recordings.
- `--overwrite`: Replace the output file if it already exists.

## Why it handles long files well

- Conversion is streamed by FFmpeg—no large buffers or in-memory decoding.
- Temporary files are used to guarantee atomic writes: the destination file is
  only replaced after a successful conversion.

## Library usage

```python
from audio_converter import AudioConverter

converter = AudioConverter()
mp3_path = converter.convert_m4a_to_mp3(
    "podcast_episode.m4a", bitrate="256k", normalize=True, overwrite=True
)
print(mp3_path)
```

## Deploying to Replicate

Replicate supports simple Python projects with a `replicate.yaml` manifest and a
`Predictor` class. The sample config below installs FFmpeg, wires this package
as the runtime dependency, and exposes a callable entrypoint.

1. Add a `replicate.yaml` like the example in this repo. Key fields:
   - `python_version`: set to `3.10` or newer.
   - `system_packages`: include `ffmpeg` so the converter can encode MP3s.
   - `python_packages`: install the local project (e.g., `- .`).
   - `predict`: point to `predict.py:Predictor`.

2. Create `predict.py` with a `Predictor` class that wraps `AudioConverter`.
   The sample file provided here converts an uploaded `.m4a` and returns the
   resulting `.mp3` path so Replicate can stream the output file.

3. Log in to Replicate and push the model:

```bash
replicate login
replicate push --create
```

4. Run inference from the CLI or API (replace `username/model` with your model
   slug):

```bash
replicate run username/model --input audio=@/path/to/input.m4a bitrate=256k normalize=true
```

The Replicate build will install FFmpeg, pull this package, and invoke
`Predictor.predict` to perform the conversion, making it suitable for long M4A
files.
