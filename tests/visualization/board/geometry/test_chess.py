"""Tests for module games.visualization.board.geometry.chess."""

import pytest

from games.visualization.board.geometry.chess import ChessGeometry


@pytest.mark.geometry
def test_chess_origin() -> None:
    """Chess (0,0) should map to center of first square."""
    geo = ChessGeometry()

    assert geo.cell_position(0, 0) == (0.5, 0.5)


@pytest.mark.geometry
def test_chess_consistency() -> None:
    """Chess coordinates should follow uniform +0.5 offset rule."""
    geo = ChessGeometry()

    assert geo.cell_position(7, 7) == (7.5, 7.5)


@pytest.mark.geometry
def test_chess_monotonicity() -> None:
    """Increasing r/c should increase y/x monotonically."""
    geo = ChessGeometry()

    x1, y1 = geo.cell_position(0, 0)
    x2, y2 = geo.cell_position(1, 1)

    assert x2 > x1
    assert y2 > y1
