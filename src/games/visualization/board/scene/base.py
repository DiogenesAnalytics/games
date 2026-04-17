"""Abstract interface for rendering orchestration layer."""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Optional


@dataclass(frozen=True)
class RenderSpec:
    """Configuration for scene rendering output."""

    figsize: tuple[float, float] = (6.0, 6.0)
    dpi: int = 150
    show_axes: bool = False


class Scene(ABC):
    """High-level rendering unit that produces complete board visualization."""

    def __init__(self, spec: Optional[RenderSpec] = None) -> None:
        """Initialize Scene with rendering configuration."""
        self.spec: RenderSpec = spec or RenderSpec()

    @abstractmethod
    def render(self, *, return_ax: bool = False) -> Any:
        """Render the scene."""
        raise NotImplementedError
