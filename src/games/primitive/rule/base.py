"""Base module for defining the abstract base class (ABC) for game rules."""

from abc import ABC
from abc import abstractmethod

from games.primitive.state.base import State


class Rule(ABC):
    """Abstract Base Class for rules that define state transitions."""

    @abstractmethod
    def apply(self, state: State) -> None:
        """Apply the rule to a given state, potentially modifying it."""
        pass

    @abstractmethod
    def supports_state(self, state: State) -> bool:
        """Check if the rule is compatible with the given state."""
        pass
