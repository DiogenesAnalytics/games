"""Tests for module games.visualization.board.scene.go."""

from typing import Any

import pytest
from sgfmill import boards

from games.visualization.board.scene.go import GoScene


@pytest.mark.scene
def test_go_scene_renders_without_error() -> None:
    """Test execute full render pipeline."""
    board = boards.Board(9)
    scene = GoScene(board)

    ax: Any = scene.render(return_ax=True)

    assert ax is not None


@pytest.mark.scene
def test_go_scene_renders_stone() -> None:
    """Test render at least one stone when present."""
    board = boards.Board(9)
    board.play(3, 3, "b")

    scene = GoScene(board)

    ax: Any = scene.render(return_ax=True)

    assert len(ax.texts) >= 1


@pytest.mark.scene
def test_go_scene_identity_geometry() -> None:
    """Test preserve identity coordinate mapping."""
    board = boards.Board(9)
    board.play(3, 3, "b")

    scene = GoScene(board)

    ax: Any = scene.render(return_ax=True)

    positions = {t.get_position() for t in ax.texts}

    assert (3.0, 3.0) in positions
