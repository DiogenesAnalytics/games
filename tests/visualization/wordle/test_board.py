"""Tests for the Wordle board visualization model."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell


@pytest.mark.wordle
def test_wordle_cell() -> None:
    """Test a Wordle cell."""
    cell = WordleCell("A", FeedbackTile.GREEN)

    assert cell.letter == "A"
    assert cell.feedback is FeedbackTile.GREEN


@pytest.mark.wordle
def test_wordle_board() -> None:
    """Test a Wordle board."""
    row = (
        WordleCell("A", FeedbackTile.GREEN),
        WordleCell("B", FeedbackTile.YELLOW),
    )
    board = WordleBoard((row,))

    assert board.rows == (row,)
