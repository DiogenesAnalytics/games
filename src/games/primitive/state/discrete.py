"""Module defining atomic state classes for discrete choices."""

from typing import Any
from typing import Set

from games.primitive.state.base import State


class ChoiceState(State):
    """A state representing a single choice from a predefined set of options."""

    def __init__(self, choices: Set[Any]) -> None:
        """Initialize the state with a predefined set of valid choices."""
        if not choices:
            raise ValueError(
                "ChoiceState must be initialized with at least one choice."
            )
        super().__init__()
        self._choices = choices

    def reset(self) -> None:
        """Reset the state to an initial value (None)."""
        self._value = None

    def is_valid(self) -> bool:
        """Check if the current state value is a valid choice."""
        return self._value in self._choices

    def update(self, new_value: Any) -> None:
        """Update the value of the state, ensuring it's a valid choice."""
        if new_value not in self._choices:
            raise ValueError(
                f"Invalid choice: {new_value}. Allowed values: {self._choices}"
            )
        self._value = new_value

    @property
    def available_values(self) -> Set[Any]:
        """Return the available choices for this state."""
        return self._choices
