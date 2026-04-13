"""Abstract interface for board background rendering strategies."""

from abc import ABC, abstractmethod
from typing import Any


class Background(ABC):
    """Abstract background rendering strategy."""

    @abstractmethod
    def draw(self, ax: Any, size: int) -> None:
        """Render background onto axis."""
        raise NotImplementedError
