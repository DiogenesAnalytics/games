"""Core visualization contracts for board rendering system."""

from typing import Any
from typing import Protocol


class BoardProtocol(Protocol):
    """Minimal interface required to read a 2D game board."""

    def size(self) -> int:
        """Return board dimension (e.g. 8 for chess, 19 for Go)."""
        ...

    def get(self, r: int, c: int) -> Any:
        """Return raw game object at (r, c), or None."""
        ...


class CellValue(Protocol):
    """Renderable object that can be displayed in a grid cell."""

    def render_symbol(self) -> str:
        """Return glyph used to represent the object."""

    def piece_color(self) -> str:
        """Return logical game-side or semantic color."""

    def render_color(self) -> str:
        """Return display color used for rendering."""

    def draw(
        self,
        ax: Any,
        x: float,
        y: float,
        board_size: int,
    ) -> bool:
        """Draw custom representation.

        Return True if handled by cell.
        Return False to let renderer fallback to text.
        """
