"""Core board rendering engine."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional
from typing import Sequence

import matplotlib.pyplot as plt

from .background.base import Background
from .geometry.base import Geometry
from .protocol import CellValue
from .types import Grid
from .types import Overlay


class BoardRenderer(ABC):
    """Abstract base class for board renderers."""

    @abstractmethod
    def render(
        self,
        grid: Grid,
        *,
        title: str = "",
        overlays: Optional[Sequence[Overlay]] = None,
    ) -> Any:
        """Render a grid state."""
        raise NotImplementedError


class MatplotlibBoardRenderer(BoardRenderer):
    """Matplotlib-based implementation of board rendering."""

    def __init__(
        self,
        background: Background,
        geometry: Geometry,
        show_grid: bool = False,
    ) -> None:
        """Initialize renderer with board background and geometry."""
        self.background = background
        self.geometry = geometry
        self.show_grid = show_grid

    def render(
        self,
        grid: Grid,
        *,
        title: str = "",
        overlays: Optional[Sequence[Overlay]] = None,
        return_ax: bool = False,
    ) -> Any:
        """Render a board grid using matplotlib."""
        size: int = grid.shape[0]
        _, ax = plt.subplots(figsize=(6, 6))

        self.background.draw(ax, size)
        self._draw_cells(ax, grid)
        self._draw_grid(ax, size)

        if overlays:
            for overlay in overlays:
                overlay(ax)

        if title:
            ax.set_title(title)

        if return_ax:
            return ax

        plt.show()

    def _draw_cells(self, ax: Any, grid: Grid) -> None:
        """Render all non-empty grid cells."""
        size: int = grid.shape[0]

        for r in range(size):
            for c in range(size):
                value: Optional[CellValue] = grid[r, c]

                if value is None:
                    continue

                x, y = self.geometry.cell_position(r, c)

                if hasattr(value, "draw"):
                    if value.draw(ax, x, y, size):
                        continue

                ax.text(
                    x,
                    y,
                    value.render_symbol(),
                    ha="center",
                    va="center",
                    color=value.render_color(),
                    fontsize=16,
                    zorder=3,
                )

    def _draw_grid(self, ax: Any, size: int) -> None:
        """Draw optional renderer-level grid lines."""
        if not self.show_grid:
            return

        for i in range(size):
            ax.plot([0, size - 1], [i, i], linewidth=1)
            ax.plot([i, i], [0, size - 1], linewidth=1)
