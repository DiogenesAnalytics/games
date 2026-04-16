"""Abstract geometry layer for board visualization."""

from abc import ABC
from abc import abstractmethod
from typing import Tuple


class Geometry(ABC):
    """Maps grid indices to rendering coordinates."""

    @abstractmethod
    def cell_position(self, r: int, c: int) -> Tuple[float, float]:
        """Convert (row, column) indices into (x, y) plot coordinates."""
        raise NotImplementedError
