"""Defines players for a Wordle simulation."""

from typing import Callable

from games.primitive.action.base import Action
from games.primitive.actor.base import Player
from games.primitive.state.base import State

from .action import WordleGuess


class InteractiveWordlePlayer(Player):
    """A Wordle player that obtains guesses from human input."""

    def __init__(
        self,
        input_func: Callable[[str], str] = input,
    ) -> None:
        """Initialize the interactive player.

        Args:
            input_func: Function used to obtain input from the player.
        """
        self._input = input_func

    def decide(self, state: State) -> Action:
        """Prompt the player for a Wordle guess.

        Args:
            state: Current Wordle game state.

        Returns:
            A WordleGuess action containing the player's input.
        """
        word = self._input("Enter your guess: ")
        return WordleGuess(word)
