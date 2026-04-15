"""Shared type definitions for board visualization system."""

from typing import Any
from typing import Callable
from typing import Tuple

from numpy.typing import NDArray

from .protocol import CellValue


# Grid of renderable cells (or empty)
Grid = NDArray[Any]

# Overlay: modifies matplotlib axis after base render
Overlay = Callable[[Any], None]


# Cell renderer hook: draws a single CellValue at (r, c)
RenderCell = Callable[[Any, int, int, CellValue], None]


# RGB color tuple (matplotlib-compatible)
CellColor = Tuple[float, float, float]
