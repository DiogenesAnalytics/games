"""Tests for module games.catalog.simulation.wordle.game."""

import pytest

from games.catalog.simulation.wordle.action import WordleGuess
from games.catalog.simulation.wordle.feedback import feedback
from games.catalog.simulation.wordle.game import WordleGame
from games.primitive.action.base import Action
from games.primitive.actor.base import Player
from games.primitive.state.base import State


class WordleTestPlayer(Player):
    """Player that returns a predetermined Wordle guess."""

    def __init__(self, word: str) -> None:
        """Initialize the player with a predetermined guess."""
        self.word = word

    def decide(self, state: State) -> Action:
        """Return the predetermined Wordle guess."""
        return WordleGuess(self.word)


@pytest.fixture
def player() -> WordleTestPlayer:
    """Return a test player with a valid guess."""
    return WordleTestPlayer("PLANE")


@pytest.fixture
def game(player: WordleTestPlayer) -> WordleGame:
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
    player: WordleTestPlayer,
) -> None:
    """A Wordle game should register its player."""
    assert len(game.actors) == 1
    assert game.actors[0] is player


@pytest.mark.wordle
def test_wordle_game_authorizes_player(
    game: WordleGame,
    player: WordleTestPlayer,
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


@pytest.mark.wordle
def test_wordle_game_step_applies_valid_guess(
    game: WordleGame,
) -> None:
    """A valid player guess should update the Wordle state."""
    game.step()

    assert game.state.guesses == ["PLANE"]
    assert game.state.feedback == [feedback("CRANE", "PLANE")]


@pytest.mark.wordle
def test_wordle_game_step_rejects_invalid_guess() -> None:
    """An invalid player guess should not update the Wordle state."""
    player = WordleTestPlayer("XXXXX")
    game = WordleGame(
        solutions={"CRANE", "PLANE"},
        target="CRANE",
        player=player,
    )

    with pytest.raises(RuntimeError, match="No rule could resolve action"):
        game.step()

    assert game.state.guesses == []
    assert game.state.feedback == []
