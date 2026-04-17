"""Full rendering pipeline for Go visualization."""

from typing import Any
from typing import Optional

from sgfmill import boards

from games.visualization.board.adapter.go import GoBoardWrapper
from games.visualization.board.adapter.go import go_board_to_grid
from games.visualization.board.background.go import GoBackground
from games.visualization.board.geometry.go import GoGeometry
from games.visualization.board.renderer import MatplotlibBoardRenderer

from .base import RenderSpec
from .base import Scene


class GoScene(Scene):
    """High-level Go rendering orchestration."""

    def __init__(self, board: boards.Board, spec: Optional[RenderSpec] = None) -> None:
        """Initialize Go scene."""
        super().__init__(spec=spec)

        self.board = board

        self.renderer = MatplotlibBoardRenderer(
            background=GoBackground(),
            geometry=GoGeometry(),
        )

    def render(self, *, return_ax: bool = False) -> Any:
        """Render Go board state."""
        wrapper = GoBoardWrapper(self.board)
        grid = go_board_to_grid(wrapper)

        return self.renderer.render(
            grid,
            spec=self.spec,
            return_ax=return_ax,
        )
