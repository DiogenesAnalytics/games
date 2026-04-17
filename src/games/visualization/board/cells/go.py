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

    def piece_color(self) -> str:
        """Return logical stone color."""
        return self.color

    def render_color(self) -> str:
        """Return display color."""
        if self.piece_color() == "white":
            return "#f4f2ec"
        return "#111111"

    def draw(
        self,
        ax: Any,
        x: float,
        y: float,
        board_size: int,
    ) -> bool:
        """Draw stone scaled to board size."""
        radius: float = 0.42

        edgecolor = "#111111" if self.piece_color() == "white" else None

        circle = StoneCircle(
            (x, y),
            radius,
            facecolor=self.render_color(),
            edgecolor=edgecolor,
            linewidth=1.0,
            zorder=3,
        )

        circle.is_stone = True

        ax.add_patch(circle)

        return True
