"""Defines the concrete Wordle simulation."""

from typing import Set

from games.catalog.simulation.base import Simulation
from games.primitive.actor.base import Player

from .rule import WordleRule
from .state import WordleState


class WordleGame(Simulation):
    """A simulation of a game of Wordle."""

    def __init__(
        self,
        solutions: Set[str],
        target: str,
        player: Player,
    ) -> None:
        """Initialize a Wordle game."""
        super().__init__()

        self._state = WordleState(solutions, target)
        rule = WordleRule()

        self._register_state(self._state)
        self._register_rule(rule)
        self._register_actor(player)

        self.authorize(player, self._state)

    @property
    def state(self) -> WordleState:
        """Return the current Wordle state."""
        return self._state

    def is_done(self) -> bool:
        """Return whether the Wordle game has ended."""
        return self._state.is_terminal
