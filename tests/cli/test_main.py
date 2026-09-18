"""Tests for the games command-line interface."""

import pytest
from click.testing import CliRunner

from games.cli.main import main


@pytest.mark.cli
def test_main_displays_help() -> None:
    """Test that the main CLI displays help."""
    runner = CliRunner()

    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
