"""Go board background implementation."""

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from matplotlib.patches import Circle
from matplotlib.patches import Rectangle

from .base import Background


_STAR_POINTS: Dict[int, Tuple[Tuple[int, int], ...]] = {
    19: (
        (3, 3),
        (3, 9),
        (3, 15),
        (9, 3),
        (9, 9),
        (9, 15),
        (15, 3),
        (15, 9),
        (15, 15),
    ),
    13: (
        (3, 3),
        (3, 9),
        (6, 6),
        (9, 3),
        (9, 9),
    ),
    9: ((4, 4),),
}


def default_star_points(size: int) -> List[Tuple[int, int]]:
    """Return deduplicated star-point coordinates for a Go board size."""
    return list(dict.fromkeys(_STAR_POINTS.get(size, ())))


class GoBackground(Background):
    """Go board background with grid lines and star points."""

    def __init__(self, color: str = "#D9A86C") -> None:
        """Initialize Go board background."""
        self.color = color

    def draw(self, ax: Any, size: int) -> None:
        """Render the Go board background onto a matplotlib axis."""
        self._configure_axes(ax, size)
        self._draw_background(ax, size)
        self._draw_grid(ax, size)
        self._draw_star_points(ax, size)

    def _configure_axes(self, ax: Any, size: int) -> None:
        """Lock coordinate system to Go board geometry contract."""
        ax.set_xlim(-0.5, size - 0.5)
        ax.set_ylim(-0.5, size - 0.5)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_autoscale_on(False)

    def _draw_background(self, ax: Any, size: int) -> None:
        """Draw solid background as a stable matplotlib patch."""
        ax.set_facecolor(self.color)

        rect = Rectangle(
            (-0.5, -0.5),
            size,
            size,
            facecolor=self.color,
            edgecolor="none",
            zorder=-1,  # Always behind everything
        )
        ax.add_patch(rect)

    def _draw_grid(self, ax: Any, size: int) -> None:
        """Draw Go grid lines."""
        for i in range(size):
            ax.plot(
                [0, size - 1],
                [i, i],
                color="black",
                linewidth=1,
                zorder=1,
            )
            ax.plot(
                [i, i],
                [0, size - 1],
                color="black",
                linewidth=1,
                zorder=1,
            )

    def _draw_star_points(self, ax: Any, size: int) -> None:
        """Draw star points (hoshi)."""
        for r, c in default_star_points(size):
            ax.add_patch(
                Circle(
                    (c, r),
                    0.12,
                    color="black",
                    zorder=2,
                )
            )
