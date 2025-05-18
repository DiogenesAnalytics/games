"""Defines classes responsible for state access."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple


class StateMapping(ABC):
    """Base class for state key-value mappings."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize with a dictionary of state data."""
        self._data: dict[str, Any] = dict(data)

    def get(self, key: str) -> Any:
        """Get the value for a given key."""
        return self._data[key]

    def keys(self) -> List[str]:
        """Return a list of all keys."""
        return list(self._data.keys())

    def __getitem__(self, key: str) -> Any:
        """Enable read access via bracket notation."""
        return self.get(key)

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        """Define how values are set via bracket notation."""
        pass


class View(StateMapping):
    """Read-only view of the simulation state."""

    def __setitem__(self, key: str, value: Any) -> None:
        """Raise error on write attempts (read-only)."""
        raise TypeError("View is read-only")


class StateDiff(StateMapping):
    """Writable mapping of proposed state changes."""

    def set(self, key: str, value: Any) -> None:
        """Set a value in the diff."""
        self._data[key] = value

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable write access via bracket notation."""
        self.set(key, value)

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Return an iterator over key-value pairs in the diff."""
        yield from self._data.items()
