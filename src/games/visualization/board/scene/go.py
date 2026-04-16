"""Full rendering pipeline for Go visualization."""

from __future__ import annotations

from typing import Any

from sgfmill import boards

from games.visualization.board.adapter.go import GoBoardWrapper
from games.visualization.board.adapter.go import go_board_to_grid
from games.visualization.board.background.go import GoBackground
from games.visualization.board.geometry.go import GoGeometry
from games.visualization.board.renderer import MatplotlibBoardRenderer

from .base import Scene


class GoScene(Scene):
    """High-level Go rendering orchestration."""

    def __init__(self, board: boards.Board) -> None:
        """Initialize Go scene."""
        self.board = board

        self.renderer = MatplotlibBoardRenderer(
            background=GoBackground(),
            geometry=GoGeometry(),
        )

    def render(self, *, return_ax: bool = False) -> Any:
        """Render Go board state."""
        wrapper = GoBoardWrapper(self.board)
        grid = go_board_to_grid(wrapper)

        return self.renderer.render(grid, return_ax=return_ax)
