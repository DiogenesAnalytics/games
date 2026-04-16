"""Go board background implementation."""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from matplotlib.patches import Circle

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
        (15, 9),
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
    """Return standard star-point coordinates for a Go board size."""
    return list(_STAR_POINTS.get(size, ()))


class GoBackground(Background):
    """Go board background with grid lines and star points."""

    def __init__(self, color: str = "#d2b48c") -> None:
        """Initialize Go board background."""
        self.color = color

    def draw(self, ax: Any, size: int) -> None:
        """Render the Go board background onto a matplotlib axis."""
        self._draw_background(ax)
        self._draw_grid(ax, size)
        self._draw_star_points(ax, size)

    def _draw_background(self, ax: Any) -> None:
        """Set the board background color."""
        ax.set_facecolor(self.color)

    def _draw_grid(self, ax: Any, size: int) -> None:
        """Draw the Go grid lines."""
        for i in range(size):
            ax.plot([0, size - 1], [i, i], linewidth=1)
            ax.plot([i, i], [0, size - 1], linewidth=1)

    def _draw_star_points(self, ax: Any, size: int) -> None:
        """Draw star points (hoshi) for standard Go board sizes."""
        for r, c in default_star_points(size):
            ax.add_patch(Circle((c, r), 0.12))
