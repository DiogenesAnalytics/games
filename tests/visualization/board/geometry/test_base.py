"""Tests for module games.visualization.board.geometry.base."""

import pytest

from games.visualization.board.geometry.base import Geometry


@pytest.mark.geometry
def test_geometry_is_abstract() -> None:
    """Geometry should not be instantiable directly."""
    with pytest.raises(TypeError):
        Geometry()  # type: ignore[abstract]
