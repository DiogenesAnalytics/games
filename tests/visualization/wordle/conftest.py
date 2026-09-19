"""Fixtures for Wordle visualization tests."""

import pytest

from games.catalog.simulation.wordle.state import WordleState


@pytest.fixture
def wordle_state() -> WordleState:
    """Return a simple Wordle state for visualization tests."""
    return WordleState(
        solutions={"CRANE"},
        available_guesses={"SLATE", "CRANE"},
        target="CRANE",
    )
