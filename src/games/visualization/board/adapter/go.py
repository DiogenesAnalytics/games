"""Adapter for converting sgfmill game state into visualization grids."""

from typing import Optional

import numpy as np
from sgfmill import boards

from ..cells.go import GoStone
from ..protocol import BoardProtocol
from ..types import Grid


class GoBoardWrapper:
    """Wraps sgfmill Go board state into a BoardProtocol-compatible interface."""

    def __init__(self, board: boards.Board) -> None:
        """Initialize wrapper with an sgfmill Go board."""
        self._board = board  # rename avoids accidental direct Any leakage

    def size(self) -> int:
        """Return board size."""
        return int(self._board.side)

    def get(self, r: int, c: int) -> Optional[str]:
        """Return stone at (r, c) or None."""
        value = self._board.get(r, c)

        # Explicit normalization boundary (important for mypy)
        if value is None:
            return None

        return str(value)


def go_board_to_grid(board: BoardProtocol) -> Grid:
    """Convert a Go board into a grid of GoStone or None."""
    size: int = board.size()
    grid: Grid = np.full((size, size), None, dtype=object)

    for r in range(size):
        for c in range(size):
            color = board.get(r, c)

            if color == "b":
                grid[r, c] = GoStone("black")
            elif color == "w":
                grid[r, c] = GoStone("white")

    return grid
