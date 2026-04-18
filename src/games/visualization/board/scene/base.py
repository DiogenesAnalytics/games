"""Abstract interface for rendering orchestration layer."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional

from games.visualization.board.renderer import RenderSpec


class Scene(ABC):
    """High-level rendering unit that produces complete board visualization."""

    def __init__(self, spec: Optional[RenderSpec] = None) -> None:
        """Initialize Scene with rendering configuration."""
        self.spec: RenderSpec = spec or RenderSpec()

    @abstractmethod
    def render(self, *, return_ax: bool = False) -> Any:
        """Render the scene."""
        raise NotImplementedError
