"""Defines atomic state classes for discrete choices."""

from typing import Any
from typing import Set

from games.primitive.state.base import DiscreteState


class ChoiceState(DiscreteState):
    """A state representing a single choice from a predefined set of options."""

    def __init__(self, choices: Set[Any]) -> None:
        """Initialize the state with a predefined set of valid choices."""
        if not choices:
            raise ValueError(
                "ChoiceState must be initialized with at least one choice."
            )
        super().__init__()
        self._choices = frozenset(choices)

    def reset(self) -> None:
        """Reset the state to its initial value (None)."""
        self._value = None

    @property
    def available_values(self) -> Set[Any]:
        """Return the available choices for this state."""
        return self._choices
