"""Abstract interface for board background rendering strategies."""

from abc import ABC
from abc import abstractmethod
from typing import Any


class Background(ABC):
    """Defines board geometry and visual background."""

    @abstractmethod
    def draw(self, ax: Any, size: int) -> None:
        """Draw the board background."""
        ...
