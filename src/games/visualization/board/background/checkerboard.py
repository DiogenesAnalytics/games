"""Checkerboard background implementation for grid-based boards."""

from typing import Any, Sequence
import numpy as np

from .base import Background


class CheckerboardBackground:
    """Alternating light/dark board background."""

    def __init__(self, light=(1.0, 0.9, 0.8), dark=(0.6, 0.4, 0.2)) -> None:
        """Initialize checkerboard colors."""
        self.light = light
        self.dark = dark

    def draw(self, ax, size: int) -> None:
        """Draw checkerboard background."""
        board = np.zeros((size, size, 3))

        for r in range(size):
            for c in range(size):
                board[r, c] = self.light if (r + c) % 2 == 0 else self.dark

        ax.imshow(board, extent=[0, size, 0, size])
