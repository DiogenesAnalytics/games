"""Adapter for converting python-chess game state into visualization grids."""

from typing import Optional

import chess
import numpy as np

from ..cells.chess import ChessPiece
from ..protocol import BoardProtocol
from ..types import Grid


class ChessBoardWrapper:
    """Wraps a python-chess board into a BoardProtocol-compatible interface."""

    def __init__(self, board: chess.Board) -> None:
        """Initialize wrapper with a python-chess board."""
        self.board = board

    def size(self) -> int:
        """Return board size."""
        return 8

    def get(self, r: int, c: int) -> Optional[chess.Piece]:
        """Return piece at (r, c) or None."""
        square: int = r * 8 + c
        return self.board.piece_at(square)


def chess_board_to_grid(board: BoardProtocol) -> Grid:
    """Convert BoardProtocol chess wrapper into grid of ChessPiece or None."""
    size = board.size()
    grid: Grid = np.full((size, size), None, dtype=object)

    for r in range(size):
        for c in range(size):
            piece = board.get(r, c)

            if piece is not None:
                grid[r, c] = ChessPiece(piece)

    return grid
