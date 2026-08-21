"""Defines the state representation for a Wordle simulation."""

from typing import List
from typing import Set
from typing import Tuple

from games.primitive.state.base import State


Feedback = Tuple[Tuple[str, str], ...]


class WordleState(State):
    """Represent the current state of a Wordle game simulation.

    A Wordle state contains the complete solution universe, the hidden
    solution, the current hypothesis space, and the observations produced
    by guesses made so far.

    The hidden solution and solution universe remain fixed throughout the
    game. The candidate set is progressively reduced as observations
    eliminate inconsistent solutions.
    """

    def __init__(
        self,
        solutions: Set[str],
        target: str,
    ) -> None:
        """Initialize a Wordle game state.

        Args:
            solutions: Complete set of valid Wordle solution words.
            target: Hidden solution word.

        Raises:
            ValueError: If the target is not contained in the solution
                dictionary.
        """
        super().__init__()

        self._solutions = {word.upper() for word in solutions}

        self._target = target.upper()

        if self._target not in self._solutions:
            raise ValueError("Target must be contained in the solution dictionary.")

        self._candidates = set(self._solutions)
        self._guesses: List[str] = []
        self._feedback: List[Feedback] = []

    @property
    def solutions(self) -> Set[str]:
        """Return the complete set of valid solution words."""
        return set(self._solutions)

    @property
    def target(self) -> str:
        """Return the hidden solution word."""
        return self._target

    @property
    def candidates(self) -> Set[str]:
        """Return the current hypothesis space."""
        return set(self._candidates)

    @property
    def guesses(self) -> List[str]:
        """Return the guesses made so far."""
        return list(self._guesses)

    @property
    def feedback(self) -> List[Feedback]:
        """Return the feedback produced by previous guesses."""
        return list(self._feedback)

    @property
    def available_values(self) -> Set[str]:
        """Return the currently possible solution words."""
        return set(self._candidates)

    def reset(self) -> None:
        """Reset the game to its initial information state."""
        self._candidates = set(self._solutions)
        self._guesses = []
        self._feedback = []

    def is_valid(self) -> bool:
        """Return whether the current Wordle state is valid."""
        return (
            len(self._target) == 5
            and self._target in self._solutions
            and self._candidates <= self._solutions
            and len(self._guesses) == len(self._feedback)
            and all(len(guess) == 5 for guess in self._guesses)
        )

    def update(self, value: object) -> None:
        """Replace this state with another Wordle state.

        Args:
            value: Wordle state from which to copy the state.

        Raises:
            TypeError: If ``value`` is not a ``WordleState``.
        """
        if not isinstance(value, WordleState):
            raise TypeError("WordleState can only be updated from WordleState.")

        self._solutions = set(value.solutions)
        self._target = value.target
        self._candidates = set(value.candidates)
        self._guesses = list(value.guesses)
        self._feedback = list(value.feedback)
