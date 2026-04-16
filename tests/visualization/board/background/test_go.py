"""Tests for module games.visualization.board.background.go."""

from types import SimpleNamespace
from typing import Any

import pytest

from games.visualization.board.background.go import GoBackground
from games.visualization.board.background.go import default_star_points


@pytest.mark.background
def test_star_point_counts() -> None:
    """Go boards should return correct star-point counts."""
    assert len(default_star_points(19)) == 9
    assert len(default_star_points(13)) == 5
    assert len(default_star_points(9)) == 1
    assert default_star_points(7) == []


@pytest.mark.background
def test_star_points_are_immutable() -> None:
    """Returned star points must not mutate internal constants."""
    pts = default_star_points(19)
    pts.append((999, 999))

    assert (999, 999) not in default_star_points(19)


@pytest.mark.background
def test_go_draw_sets_background_color() -> None:
    """Go background should set the board face color when drawn."""
    bg = GoBackground(color="#d2b48c")

    ax = SimpleNamespace()

    called: dict[str, str] = {}

    def fake_set_facecolor(color: str) -> None:
        """Spy for ax.set_facecolor capturing the applied color."""
        called["color"] = color

    def fake_plot(*args: Any, **kwargs: Any) -> None:
        """No-op stub for ax.plot used by grid drawing."""
        return None

    def fake_add_patch(*args: Any, **kwargs: Any) -> None:
        """No-op stub for ax.add_patch used by star point drawing."""
        return None

    ax.set_facecolor = fake_set_facecolor
    ax.plot = fake_plot
    ax.add_patch = fake_add_patch

    bg.draw(ax, size=19)

    assert called["color"] == "#d2b48c"
