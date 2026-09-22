"""Fixtures for Wordle visualization tests."""

import pytest

from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell


@pytest.fixture
def empty_wordle_board() -> WordleBoard:
    """Return an empty six-row Wordle board."""
    return WordleBoard(
        tuple(tuple(WordleCell(None, None) for _ in range(5)) for _ in range(6))
    )
