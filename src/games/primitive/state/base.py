"""Base module for defining the abstract base class (ABC) for game state."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Set


class State(ABC):
    """Abstract Base Class for representing a single atomic state."""

    @abstractmethod
    def __init__(self) -> None:
        """Initialize the state with its value."""
        self._value = None

    @abstractmethod
    def reset(self) -> None:
        """Reset the state to its initial value."""
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """Check if the state is valid."""
        pass

    @abstractmethod
    def update(self, value: Any) -> None:
        """Update the value of the state."""
        pass

    @property
    def value(self) -> Any:
        """Return the current value of the state."""
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the value of the state."""
        self.update(new_value)

    @property
    @abstractmethod
    def available_values(self) -> Set[Any]:
        """Return the available values or choices for this state."""
        pass
