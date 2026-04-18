"""Tests for module games.visualization.board.scene.go."""

from typing import Any

import pytest
from sgfmill import boards

from games.visualization.board.cells.go import StoneCircle
from games.visualization.board.renderer import RenderSpec
from games.visualization.board.scene.go import GoScene


@pytest.mark.scene
def test_go_scene_renders_without_error() -> None:
    """Test should execute full render pipeline."""
    board = boards.Board(9)
    scene = GoScene(board)

    ax: Any = scene.render(return_ax=True)

    assert ax is not None


@pytest.mark.scene
def test_go_scene_renders_stone_patch() -> None:
    """Test that Go stones are rendered as Circle patches with stone tag."""
    board = boards.Board(9)
    board.play(3, 3, "b")

    scene = GoScene(board)

    ax: Any = scene.render(return_ax=True)

    stone_patches = [p for p in ax.patches if isinstance(p, StoneCircle)]

    assert len(stone_patches) >= 1


@pytest.mark.scene
def test_go_scene_identity_geometry() -> None:
    """Test preserve identity coordinate mapping for Go stones."""
    board = boards.Board(9)
    board.play(3, 3, "b")

    scene = GoScene(board)

    ax: Any = scene.render(return_ax=True)

    stone_patches = [p for p in ax.patches if isinstance(p, StoneCircle)]

    centers = {p.center for p in stone_patches}

    assert (3.0, 3.0) in centers


@pytest.mark.scene
def test_go_scene_stores_render_spec() -> None:
    """Test scene preserves provided RenderSpec."""
    spec: RenderSpec = RenderSpec(
        figsize=(10.0, 10.0),
        dpi=250,
    )

    scene: GoScene = GoScene(
        boards.Board(9),
        spec=spec,
    )

    assert scene.spec is spec
