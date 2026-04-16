"""Tests for module games.visualization.board.background.checkerboard."""

from types import SimpleNamespace
from typing import Any
from typing import Tuple

import pytest

from games.visualization.board.background.checkerboard import CheckerboardBackground


@pytest.mark.background
def test_checkerboard_initialization() -> None:
    """Checkerboard should store light and dark colors."""
    bg = CheckerboardBackground()

    assert bg.light is not None
    assert bg.dark is not None


@pytest.mark.background
def test_checkerboard_draw_calls_imshow() -> None:
    """Checkerboard should draw a matrix via imshow."""
    bg = CheckerboardBackground()

    ax = SimpleNamespace()

    called = {}

    def fake_imshow(board: Any, extent: Tuple[float, float, float, float]) -> None:
        """Spy for Axes.imshow capturing board data and extent arguments."""
        called["board"] = board
        called["extent"] = extent

    ax.imshow = fake_imshow

    bg.draw(ax, size=3)

    assert "board" in called
    assert called["board"].shape == (3, 3, 3)
