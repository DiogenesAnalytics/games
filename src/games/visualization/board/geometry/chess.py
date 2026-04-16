"""Chess geometry mapping."""

from typing import Tuple

from .base import Geometry


class ChessGeometry(Geometry):
    """Geometry for square-centered board systems (e.g. chess)."""

    def cell_position(self, r: int, c: int) -> Tuple[float, float]:
        """Return center of square at (r, c)."""
        return c + 0.5, r + 0.5
