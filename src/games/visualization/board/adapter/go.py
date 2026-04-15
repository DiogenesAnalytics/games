"""Adapter for converting sgfmill game state into visualization grids."""

from typing import Any
from typing import cast

import numpy as np
from sgfmill import sgf_moves

from ..cells.go import GoStone
from ..protocol import BoardProtocol
from ..types import Grid


class GoBoardWrapper:
    """Wraps sgfmill Go board state into a BoardProtocol-compatible interface."""

    def __init__(self, board: sgf_moves.Board) -> None:
        """Initialize wrapper with an sgfmill Go board."""
        self.board = board

    def size(self) -> int:
        """Return board size."""
        return cast(int, self.board.side)

    def get(self, r: int, c: int) -> Any:
        """Return stone at (r, c) or None."""
        return self.board.get(r, c)


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
