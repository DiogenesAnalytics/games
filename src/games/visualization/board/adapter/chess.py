"""Adapter for converting python-chess game state into visualization grids."""

import chess
import numpy as np

from games.visualization.board.types import Grid


def board_to_grid(board: chess.Board) -> Grid:
    """Convert python-chess board into an 8x8 grid representation."""

    grid: Grid = np.empty((8, 8), dtype=object)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        r, c = divmod(square, 8)
        grid[r, c] = piece

    return grid
