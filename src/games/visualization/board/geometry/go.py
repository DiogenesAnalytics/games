"""Go geometry mapping."""

from typing import Tuple

from .base import Geometry


class GoGeometry(Geometry):
    """Geometry for intersection-based board systems (Go)."""

    def cell_position(self, r: int, c: int) -> Tuple[float, float]:
        """Return intersection coordinate for (r, c)."""
        return float(c), float(r)
