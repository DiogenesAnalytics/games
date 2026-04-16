"""Tests for module games.visualization.board.background.solid."""

from types import SimpleNamespace

import pytest

from games.visualization.board.background.solid import SolidBackground


@pytest.mark.background
def test_draw_sets_facecolor() -> None:
    """Check axis facecolor."""
    bg = SolidBackground("red")

    ax = SimpleNamespace()

    called = {}

    def fake_set_facecolor(color: str) -> None:
        called["color"] = color

    ax.set_facecolor = fake_set_facecolor

    bg.draw(ax, size=10)

    assert called["color"] == "red"
