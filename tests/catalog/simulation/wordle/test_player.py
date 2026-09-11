"""Tests for module games.catalog.simulation.wordle.player."""

import pytest

from games.catalog.simulation.wordle.action import WordleGuess
from games.catalog.simulation.wordle.player import InteractiveWordlePlayer
from games.primitive.state.base import State


@pytest.mark.wordle
def test_interactive_player_returns_entered_guess(
    mock_state: State,
) -> None:
    """The interactive player should return the entered word as an action."""
    player = InteractiveWordlePlayer(
        input_func=lambda prompt: "PLANE",
    )

    action = player.decide(mock_state)

    assert isinstance(action, WordleGuess)
    assert action.word == "PLANE"
