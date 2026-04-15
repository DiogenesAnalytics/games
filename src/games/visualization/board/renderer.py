"""Core board rendering engine."""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional
from typing import Sequence

import matplotlib.pyplot as plt

from .background.base import Background
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
    ) -> None:
        """Render a grid state."""
        raise NotImplementedError


class MatplotlibBoardRenderer(BoardRenderer):
    """Matplotlib-based implementation of board rendering."""

    def __init__(
        self,
        background: Background,
        show_grid: bool = False,
    ) -> None:
        """Initialize renderer."""
        self.background = background
        self.show_grid = show_grid

    def render(
        self,
        grid: Grid,
        *,
        title: str = "",
        overlays: Optional[Sequence[Overlay]] = None,
    ) -> None:
        """Render a board grid using matplotlib."""
        size: int = grid.shape[0]
        fig, ax = plt.subplots(figsize=(6, 6))

        self.background.draw(ax, size)
        self._draw_cells(ax, grid)
        self._draw_grid(ax, size)

        if overlays:
            for overlay in overlays:
                overlay(ax)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect("equal")

        if title:
            ax.set_title(title)

        plt.show()

    def _draw_cells(self, ax: Any, grid: Grid) -> None:
        """Render all non-empty grid cells."""
        size: int = grid.shape[0]

        for r in range(size):
            for c in range(size):
                value: Optional[CellValue] = grid[r, c]

                if value is None:
                    continue

                ax.text(
                    c + 0.5,
                    r + 0.5,
                    value.render_symbol(),
                    ha="center",
                    va="center",
                    color=value.render_color(),
                    fontsize=16,
                )

    def _draw_grid(self, ax: Any, size: int) -> None:
        """Draw optional grid lines."""
        if not self.show_grid:
            return

        for i in range(size):
            ax.plot([0, size - 1], [i, i], linewidth=1)
            ax.plot([i, i], [0, size - 1], linewidth=1)
