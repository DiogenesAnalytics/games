"""Tests for the Wordle command-line interface."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from games.cli.wordle import _select_target
from games.cli.wordle import wordle


@pytest.mark.cli
@pytest.mark.wordle
def test_wordle_wins() -> None:
    """The Wordle command reports a successful game."""
    runner = CliRunner()

    with patch(
        "games.cli.wordle._select_target",
        return_value="CRANE",
    ):
        result = runner.invoke(wordle, input="CRANE\n")

    assert result.exit_code == 0
    assert "You got it in 1 guesses!" in result.output


@pytest.mark.cli
@pytest.mark.wordle
def test_wordle_loses() -> None:
    """The Wordle command reports the target after six guesses."""
    runner = CliRunner()

    with patch(
        "games.cli.wordle._select_target",
        return_value="CRANE",
    ):
        result = runner.invoke(
            wordle,
            input="SLATE\nSLATE\nSLATE\nSLATE\nSLATE\nSLATE\n",
        )

    assert result.exit_code == 0
    assert "The word was CRANE." in result.output


@pytest.mark.cli
@pytest.mark.wordle
def test_wordle_rejects_invalid_guess() -> None:
    """The Wordle command rejects an unavailable guess."""
    runner = CliRunner()

    with patch(
        "games.cli.wordle._select_target",
        return_value="CRANE",
    ):
        result = runner.invoke(
            wordle,
            input="ZZZZZ\nCRANE\n",
        )

    assert result.exit_code == 0
    assert "Invalid guess. Please try again." in result.output
    assert "You got it in 1 guesses!" in result.output


@pytest.mark.cli
@pytest.mark.wordle
def test_select_target_returns_answer() -> None:
    """Test that target selection returns an available answer."""
    answers = {"CRANE", "STAIN", "PLANE"}

    assert _select_target(answers) in answers
