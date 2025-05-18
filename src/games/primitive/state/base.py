"""Base module for defining the abstract base class (ABC) for game state."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional
from typing import Set
from typing import Tuple


class State(ABC):
    """Abstract base class representing a single piece of simulation state."""

    def __init__(self) -> None:
        """Initialize the state with its value."""
        self._value: Optional[Any] = None

    @abstractmethod
    def reset(self) -> None:
        """Reset the state to its initial value."""
        pass

    @abstractmethod
    def is_valid_value(self, value: Any) -> bool:
        """Return True if the proposed value is valid for this state."""
        pass

    def update(self, value: Any) -> None:
        """Update the value after checking validity."""
        if not self.is_valid_value(value):
            raise ValueError(f"Invalid value for {self.__class__.__name__}: {value}")
        self._value = value

    @property
    def value(self) -> Any:
        """Current state value."""
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set a new value using update logic."""
        self.update(new_value)

    @abstractmethod
    def domain(self) -> str:
        """Return a human-readable description of valid values."""
        pass


class DiscreteState(State, ABC):
    """States with a finite set of valid values."""

    @property
    @abstractmethod
    def available_values(self) -> Set[Any]:
        """All valid discrete options for this state."""
        pass

    def is_valid_value(self, value: Any) -> bool:
        """Check if the value is one of the available discrete values."""
        return value in self.available_values

    def domain(self) -> str:
        """Human-readable description of the discrete value space."""
        values = sorted(self.available_values)
        preview = ", ".join(map(str, values[:5]))
        suffix = ", ..." if len(values) > 5 else ""
        return f"One of [{preview}{suffix}] ({len(values)} total)"


class ContinuousState(State, ABC):
    """States with continuous or unbounded values."""

    @property
    @abstractmethod
    def bounds(self) -> Optional[Tuple[float, float]]:
        """Lower and upper numeric bounds, if defined. Otherwise unbounded."""
        pass

    def is_valid_value(self, value: Any) -> bool:
        """Check if the value is a valid real number within bounds."""
        if not isinstance(value, (int, float)):
            return False
        if self.bounds is None:
            return True
        lower, upper = self.bounds
        return lower <= value <= upper

    def domain(self) -> str:
        """Human-readable description of the numeric value space."""
        if self.bounds is None:
            return "Any real number"
        lower, upper = self.bounds
        return f"Real number between {lower} and {upper}"
