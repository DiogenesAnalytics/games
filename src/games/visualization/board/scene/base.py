"""Abstract interface for rendering orchestration layer."""

from abc import ABC
from abc import abstractmethod
from typing import Any


class Scene(ABC):
    """High-level rendering unit that produces complete board visualization."""

    @abstractmethod
    def render(self, *, return_ax: bool = False) -> Any:
        """Render the scene."""
        raise NotImplementedError
