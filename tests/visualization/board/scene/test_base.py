"""Tests for module games.visualization.board.scene.base."""

import pytest

from games.visualization.board.scene.base import Scene


@pytest.mark.scene
def test_scene_is_abstract() -> None:
    """Scene cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Scene()  # type: ignore[abstract]
