"""Base module for defining the abstract base class (ABC) for game actions."""

from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Optional

from games.primitive.state.base import State


class Action(ABC):
    """Abstract base class for all actions."""

    def __init__(self) -> None:
        """Initialize executor function to default None value."""
        self._executor: Optional[Callable[[State], None]] = None
        self._valid: bool = False
        self._invalidated: bool = False

    @property
    def is_valid(self) -> bool:
        """Check whether the action has passed validation."""
        return self._valid

    def invalidate(self) -> None:
        """Mark the action as invalid and remove executor."""
        if not self._invalidated:
            self._valid = False
            self._executor = None
            self._invalidated = True

    def validate(self) -> None:
        """Validate the action (mark as valid), but skip if invalidated."""
        if not self._invalidated:
            self._valid = True

    @property
    def is_resolved(self) -> bool:
        """Check whether the action is validated and has an executor."""
        return self._valid and self._executor is not None

    @property
    def apply(self) -> Callable[[State], None]:
        """Return the executor function that applies the action."""
        if not self.is_resolved:
            raise NotImplementedError("Action has not been resolved by any Rule.")
        assert self._executor is not None  # for mypy and safety
        return self._executor

    @property
    def executor(self) -> Optional[Callable[[State], None]]:
        """Access the underlying executor function, if set."""
        return self._executor

    @executor.setter
    def executor(self, func: Callable[[State], None]) -> None:
        """Set the function that will execute the action on the state."""
        if not callable(func):
            raise TypeError("Executor must be a callable.")
        self._executor = func

    @abstractmethod
    def describe(self) -> str:
        """Describe the action in human-readable terms."""
        pass

    def __repr__(self) -> str:
        """Return a string representation of the action."""
        try:
            desc = self.describe()
            summary = (desc[:47] + "...") if len(desc) > 50 else desc
        except Exception:
            summary = "N/A"

        return (
            f"<{self.__class__.__name__}: "
            f"valid={self.is_valid}, "
            f"desc={summary!r}>"
        )
