"""Tests for module games.visualization.board.geometry.go."""

import pytest

from games.visualization.board.geometry.go import GoGeometry


@pytest.mark.geometry
def test_go_origin() -> None:
    """Go coordinates should map directly to intersections."""
    geo = GoGeometry()

    assert geo.cell_position(0, 0) == (0.0, 0.0)


@pytest.mark.geometry
def test_go_consistency() -> None:
    """Go geometry should preserve grid coordinates exactly."""
    geo = GoGeometry()

    assert geo.cell_position(10, 7) == (7.0, 10.0)


@pytest.mark.geometry
def test_go_monotonicity() -> None:
    """Go geometry should preserve ordering of coordinates."""
    geo = GoGeometry()

    x1, y1 = geo.cell_position(0, 0)
    x2, y2 = geo.cell_position(5, 5)

    assert x2 > x1
    assert y2 > y1
