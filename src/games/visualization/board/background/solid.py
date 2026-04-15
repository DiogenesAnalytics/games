"""Solid color background implementation for board visualization."""

from typing import Any

from .base import Background


class SolidBackground(Background):
    """Background that fills the board with a single solid color."""

    def __init__(self, color: str) -> None:
        """Initialize with a matplotlib-compatible color string."""
        self.color = color

    def draw(self, ax: Any, size: int) -> None:
        """Set the axes facecolor to the configured background color."""
        ax.set_facecolor(self.color)
