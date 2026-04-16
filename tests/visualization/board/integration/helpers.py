"""Shared helpers for board rendering integration tests."""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Tuple

from games.visualization.board.background.chess import ChessBackground
from games.visualization.board.background.go import GoBackground
from games.visualization.board.geometry.chess import ChessGeometry
from games.visualization.board.geometry.go import GoGeometry
from games.visualization.board.renderer import MatplotlibBoardRenderer


def make_chess_renderer() -> MatplotlibBoardRenderer:
    """Construct a standard Chess renderer for integration testing."""
    return MatplotlibBoardRenderer(
        background=ChessBackground(),
        geometry=ChessGeometry(),
        show_grid=False,
    )


def make_go_renderer() -> MatplotlibBoardRenderer:
    """Construct a standard Go renderer for integration testing."""
    return MatplotlibBoardRenderer(
        background=GoBackground(),
        geometry=GoGeometry(),
        show_grid=False,
    )


def extract_text_positions(ax: Any) -> Dict[Tuple[float, float], str]:
    """Extract rendered text positions from a matplotlib Axes object."""
    return {t.get_position(): t.get_text() for t in ax.texts}
