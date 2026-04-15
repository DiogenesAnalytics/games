"""Go stone cell rendering primitives."""


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
