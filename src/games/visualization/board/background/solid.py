"""Solid color background implementation for board visualization."""

from typing import Any
from .base import Background


class SolidBackground(Background):
    """Single-color background."""

    def __init__(self, color: str) -> None:
        self.color = color

    def draw(self, ax: Any, size: int) -> None:
        ax.set_facecolor(self.color)
