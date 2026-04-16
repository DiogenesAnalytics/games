"""Tests for module games.visualization.board.geometry invariants."""

import pytest

from games.visualization.board.geometry.chess import ChessGeometry
from games.visualization.board.geometry.go import GoGeometry


@pytest.mark.geometry
def test_geometry_deterministic() -> None:
    """Geometry functions must be deterministic."""
    chess = ChessGeometry()

    assert chess.cell_position(3, 4) == chess.cell_position(3, 4)


@pytest.mark.geometry
def test_go_vs_chess_differ() -> None:
    """Go and chess geometry must not be identical systems."""
    go = GoGeometry()
    chess = ChessGeometry()

    assert go.cell_position(0, 0) != chess.cell_position(0, 0)
