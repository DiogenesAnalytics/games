"""Tests for module games.visualization.board.scene.chess."""

from typing import Any

import chess
import pytest

from games.visualization.board.scene.chess import ChessScene


@pytest.mark.scene
def test_chess_scene_renders_without_error() -> None:
    """Test execute full render pipeline without failure."""
    scene = ChessScene(chess.Board())

    ax: Any = scene.render(return_ax=True)

    assert ax is not None
    assert hasattr(ax, "texts")


@pytest.mark.scene
def test_chess_scene_returns_text_elements() -> None:
    """Test produce rendered text elements."""
    scene = ChessScene(chess.Board())

    ax: Any = scene.render(return_ax=True)

    assert len(ax.texts) > 0


@pytest.mark.scene
def test_chess_scene_initial_position_has_correct_piece_count() -> None:
    """Chess initial position should render all pieces."""
    scene = ChessScene(chess.Board())

    ax: Any = scene.render(return_ax=True)

    assert len(ax.texts) == 32


@pytest.mark.scene
def test_chess_scene_geometry_is_consistent() -> None:
    """Test maintain consistent spatial layout."""
    scene = ChessScene(chess.Board())

    ax: Any = scene.render(return_ax=True)

    positions = {t.get_position() for t in ax.texts}

    # Back rank (white side)
    expected = [
        (0.5, 7.5),
        (1.5, 7.5),
        (2.5, 7.5),
        (3.5, 7.5),
        (4.5, 7.5),
        (5.5, 7.5),
        (6.5, 7.5),
        (7.5, 7.5),
    ]

    for p in expected:
        assert p in positions
