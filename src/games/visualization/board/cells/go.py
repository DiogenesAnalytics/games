"""Go stone cell rendering primitives."""

from typing import Any

from matplotlib.patches import Circle


class StoneCircle(Circle):
    """Matplotlib Circle patch representing a Go stone."""

    is_stone: bool = True


class GoStone:
    """Renderable Go stone."""

    def __init__(self, color: str) -> None:
        """Initialize Go stone with color ('black' or 'white')."""
        self.color = color

    def render_symbol(self) -> str:
        """Return stone symbol."""
        return "●"

    def render_color(self) -> str:
        """Return display color."""
        return self.color

    def draw(
        self,
        ax: Any,
        x: float,
        y: float,
        board_size: int,
    ) -> bool:
        """Draw stone scaled to board size."""
        radius: float = 0.42

        edgecolor = "black" if self.color == "white" else None

        circle = StoneCircle(
            (x, y),
            radius,
            facecolor=self.color,
            edgecolor=edgecolor,
            zorder=3,
        )

        circle.is_stone = True

        ax.add_patch(circle)

        return True
