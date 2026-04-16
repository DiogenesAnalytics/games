"""Full rendering pipeline for chess visualization."""

from typing import Any

import chess

from games.visualization.board.adapter.chess import ChessBoardWrapper
from games.visualization.board.adapter.chess import chess_board_to_grid
from games.visualization.board.background.chess import ChessBackground
from games.visualization.board.geometry.chess import ChessGeometry
from games.visualization.board.renderer import MatplotlibBoardRenderer

from .base import Scene


class ChessScene(Scene):
    """High-level chess rendering orchestration."""

    def __init__(self, board: chess.Board) -> None:
        """Initialize chess scene."""
        self.board = board

        self.renderer = MatplotlibBoardRenderer(
            background=ChessBackground(),
            geometry=ChessGeometry(),
        )

    def render(self, *, return_ax: bool = False) -> Any:
        """Render chess board state."""
        wrapper = ChessBoardWrapper(self.board)
        grid = chess_board_to_grid(wrapper)

        return self.renderer.render(grid, return_ax=return_ax)
