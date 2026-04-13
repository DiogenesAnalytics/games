"""Core board rendering engine."""

import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence

from .types import Grid, Overlay


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
    """Matplotlib implementation of board renderer."""

    def __init__(self, background, render_cell, show_grid: bool = False):
        """Initialize renderer with background and cell strategy."""
        self.background = background
        self.render_cell = render_cell
        self.show_grid = show_grid

    def render(
        self,
        grid: Grid,
        *,
        title: str = "",
        overlays: Optional[Sequence[Overlay]] = None,
    ) -> None:
        """Render a grid using matplotlib."""
        size = grid.shape[0]
        fig, ax = plt.subplots(figsize=(6, 6))

        self.background.draw(ax, size)
        self._draw_cells(ax, grid)
        self._draw_grid(ax, size)

        if overlays:
            for o in overlays:
                o(ax)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect("equal")

        if title:
            ax.set_title(title)

        plt.show()

    def _draw_cells(self, ax: Any, grid: Grid) -> None:
        """Render all grid cells."""
        size = grid.shape[0]

        for r in range(size):
            for c in range(size):
                value = grid[r, c]
                if value is not None:
                    self.render_cell(ax, r, c, value)

    def _draw_grid(self, ax: Any, size: int) -> None:
        """Draw optional grid lines."""
        if not self.show_grid:
            return

        for i in range(size):
            ax.plot([0, size - 1], [i, i], linewidth=1)
            ax.plot([i, i], [0, size - 1], linewidth=1)
