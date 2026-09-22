"""Fixtures for Wordle visualization tests."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.state import WordleState
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell


@pytest.fixture
def wordle_state() -> WordleState:
    """Return a Wordle state with one guess."""
    state = WordleState(
        solutions={"CRANE", "PLANE"},
        available_guesses={"CRANE", "PLANE"},
        target="CRANE",
    )
    state.update(
        (
            "PLANE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
            ),
        )
    )
    return state


@pytest.fixture
def empty_wordle_state() -> WordleState:
    """Return an empty Wordle state."""
    return WordleState(
        solutions={"CRANE"},
        available_guesses={"CRANE"},
        target="CRANE",
    )


@pytest.fixture
def empty_wordle_board() -> WordleBoard:
    """Return an empty six-row Wordle board."""
    return WordleBoard(
        tuple(tuple(WordleCell(None, None) for _ in range(5)) for _ in range(6))
    )
