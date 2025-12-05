from __future__ import annotations

import pytest

from audio_converter import cli


def test_cli_help_exits_cleanly() -> None:
    """Ensure the CLI help flag exits with a success status."""

    with pytest.raises(SystemExit) as excinfo:
        cli.parse_args(["-h"])

    assert excinfo.value.code == 0
