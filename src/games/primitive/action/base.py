"""Base module for defining the abstract base class (ABC) for game actions."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from games.primitive.state.mapping import StateDiff
from games.primitive.state.mapping import View


class Action(ABC):
    """Abstract base class for all actions."""

    def __init__(
        self, actor_id: str, view: View, diff: Optional[StateDiff] = None
    ) -> None:
        """Store Actor info and initialize state."""
        self.actor_id = actor_id
        self.view = view
        self._diff = diff if diff is not None else StateDiff({})
        self._valid: bool = False
        self._invalidated: bool = False

    # accessors for StateDiff
    @property
    def diff(self) -> StateDiff:
        """Return the StateDiff object."""
        return self._diff

    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair in the StateDiff."""
        self.diff[key] = value

    def get(self, key: str) -> Any:
        """Get a value for a given key from the StateDiff."""
        return self.diff[key]

    def items(self) -> List[Tuple[str, Any]]:
        """Return all key-value pairs in the StateDiff."""
        return list(self.diff.items())

    def __getitem__(self, key: str) -> Any:
        """Allow direct access to the StateDiff using indexing."""
        return self.diff[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Allow direct modification of the StateDiff using indexing."""
        self.diff[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the StateDiff."""
        return key in self.diff

    @property
    def is_valid(self) -> bool:
        """Check whether the action has passed validation."""
        return self._valid

    def invalidate(self) -> None:
        """Mark the action as invalid (permanent)."""
        if not self._invalidated:
            self._valid = False
            self._invalidated = True

    def validate(self) -> None:
        """Mark the action as valid unless already invalidated."""
        if not self._invalidated:
            self._valid = True

    @abstractmethod
    def describe(self) -> str:
        """Describe the action in human-readable terms."""
        pass

    def __repr__(self) -> str:
        """Return a string representation of the action."""
        # format description str in a compact way
        try:
            desc = self.describe()
            summary = (desc[:47] + "...") if len(desc) > 50 else desc
        except Exception:
            summary = "N/A"

        # format StateDiff in a compact way
        try:
            diff_items = list(self.diff._data.items())
            diff_summary = "{...}" if len(diff_items) > 3 else str(self.diff._data)
        except Exception:
            diff_summary = "N/A"

        return (
            f"<{self.__class__.__name__}: "
            f"actor={self.actor_id}, "
            f"valid={self.is_valid}, "
            f"diff={diff_summary}, "
            f"desc={summary!r}>"
        )
