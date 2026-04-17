"""Tests for module games.visualization.board.background.go."""

from typing import Any

import pytest

from games.visualization.board.background.go import GoBackground
from games.visualization.board.background.go import default_star_points


class AxesStub:
    """Minimal matplotlib Axes test double."""

    def __init__(self) -> None:
        """Initialize an empty AxesStub with no recorded state."""
        self.facecolor: str | None = None
        self.calls: dict[str, list[Any]] = {}

    def set_facecolor(self, color: str) -> None:
        """Record facecolor applied to the axes."""
        self.facecolor = color

    def plot(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for line plotting."""
        self.calls.setdefault("plot", []).append((args, kwargs))

    def add_patch(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for patch drawing (e.g. Go star points)."""
        self.calls.setdefault("add_patch", []).append((args, kwargs))

    def set_xlim(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for x-axis limits."""
        self.calls.setdefault("set_xlim", []).append((args, kwargs))

    def set_ylim(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for y-axis limits."""
        self.calls.setdefault("set_ylim", []).append((args, kwargs))

    def set_aspect(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for aspect ratio configuration."""
        self.calls.setdefault("set_aspect", []).append((args, kwargs))

    def set_xticks(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for x tick configuration."""
        self.calls.setdefault("set_xticks", []).append((args, kwargs))

    def set_yticks(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for y tick configuration."""
        self.calls.setdefault("set_yticks", []).append((args, kwargs))

    def set_autoscale_on(self, *args: Any, **kwargs: Any) -> None:
        """No-op stub for matplotlib autoscaling toggle."""
        self.calls.setdefault("set_autoscale_on", []).append((args, kwargs))


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
    """Go background should configure axes state and render board elements."""
    bg = GoBackground(color="#d2b48c")

    ax = AxesStub()

    bg.draw(ax, size=19)

    assert ax.facecolor == "#d2b48c"
