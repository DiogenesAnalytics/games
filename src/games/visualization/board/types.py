"""Shared type definitions for board visualization system."""

from typing import Any
from typing import Callable
from typing import Tuple

from numpy.typing import NDArray


# Grid of renderable cells (or empty)
Grid = NDArray[Any]

# Overlay: modifies matplotlib axis after base render
Overlay = Callable[[Any], None]

# RGB color tuple (matplotlib-compatible)
CellColor = Tuple[float, float, float]
