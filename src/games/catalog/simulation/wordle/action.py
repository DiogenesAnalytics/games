"""Define actions for the Wordle simulation."""

from games.primitive.action.base import Action


class WordleGuess(Action):
    """Represent a proposed Wordle guess.

    A Wordle guess contains the word proposed by an actor. The legality of
    the proposed guess is determined by a Wordle rule using the current
    game state.

    Args:
        word: The word proposed as the guess.
    """

    def __init__(self, word: str) -> None:
        """Initialize the Wordle guess with a proposed word."""
        super().__init__()
        self.word = word

    def describe(self) -> str:
        """Return a human-readable description of the proposed guess."""
        return f"Guess {self.word!r}"
