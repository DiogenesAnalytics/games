"""Tests for module games.catalog.simulation.wordle.game."""

import pytest

from games.catalog.simulation.wordle.feedback import feedback
from games.catalog.simulation.wordle.game import WordleGame
from games.primitive.action.base import Action
from games.primitive.actor.base import Player
from games.primitive.state.base import State


class DummyPlayer(Player):
    """Player implementation for testing WordleGame."""

    def decide(self, state: State) -> Action:
        """Return an action for the supplied state."""
        raise NotImplementedError


@pytest.fixture
def player() -> DummyPlayer:
    """Return a dummy player."""
    return DummyPlayer()


@pytest.fixture
def game(player: DummyPlayer) -> WordleGame:
    """Return a Wordle game for testing."""
    return WordleGame(
        solutions={"CRANE", "PLANE"},
        target="CRANE",
        player=player,
    )


@pytest.mark.wordle
def test_wordle_game_registers_state(game: WordleGame) -> None:
    """A Wordle game should register its state."""
    assert len(game.states) == 1
    assert game.states[0] is game.state


@pytest.mark.wordle
def test_wordle_game_registers_rule(game: WordleGame) -> None:
    """A Wordle game should register its rule."""
    assert len(game.rules) == 1


@pytest.mark.wordle
def test_wordle_game_registers_player(
    game: WordleGame,
    player: DummyPlayer,
) -> None:
    """A Wordle game should register its player."""
    assert len(game.actors) == 1
    assert game.actors[0] is player


@pytest.mark.wordle
def test_wordle_game_authorizes_player(
    game: WordleGame,
    player: DummyPlayer,
) -> None:
    """A Wordle game should authorize its player for its state."""
    assert game.is_authorized(player, game.state)


@pytest.mark.wordle
def test_wordle_game_is_not_done_initially(game: WordleGame) -> None:
    """A newly initialized Wordle game should not be done."""
    assert not game.is_done()


@pytest.mark.wordle
def test_wordle_game_is_done_when_target_is_guessed(
    game: WordleGame,
) -> None:
    """A Wordle game should be done when the target has been guessed."""
    game.state.update(("CRANE", feedback("CRANE", "CRANE")))

    assert game.is_done()
