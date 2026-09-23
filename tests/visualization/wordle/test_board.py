"""Tests for the Wordle board visualization model."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell
from games.visualization.wordle.board import create_wordle_board


@pytest.mark.renderer
@pytest.mark.wordle
def test_wordle_cell() -> None:
    """Test a Wordle cell."""
    cell = WordleCell("A", FeedbackTile.GREEN)

    assert cell.letter == "A"
    assert cell.feedback is FeedbackTile.GREEN


@pytest.mark.renderer
@pytest.mark.wordle
def test_wordle_board() -> None:
    """Test a Wordle board."""
    row = (
        WordleCell("A", FeedbackTile.GREEN),
        WordleCell("B", FeedbackTile.YELLOW),
    )
    board = WordleBoard((row,))

    assert board.rows == (row,)


@pytest.mark.renderer
@pytest.mark.wordle
def test_create_wordle_board() -> None:
    """Create a Wordle board from guesses and feedback."""
    board = create_wordle_board(
        guesses=("SLATE",),
        feedback=(
            (
                FeedbackTile.GRAY,
                FeedbackTile.YELLOW,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GRAY,
            ),
        ),
    )

    assert board.rows[0] == (
        WordleCell("S", FeedbackTile.GRAY),
        WordleCell("L", FeedbackTile.YELLOW),
        WordleCell("A", FeedbackTile.GRAY),
        WordleCell("T", FeedbackTile.GREEN),
        WordleCell("E", FeedbackTile.GRAY),
    )


@pytest.mark.renderer
@pytest.mark.wordle
def test_create_wordle_board_pads_empty_rows() -> None:
    """Pad a Wordle board with empty rows."""
    board = create_wordle_board(
        guesses=(),
        feedback=(),
    )

    assert len(board.rows) == 6
    assert all(
        row == tuple(WordleCell(None, None) for _ in range(5)) for row in board.rows
    )
