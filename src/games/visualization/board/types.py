"""Shared type definitions for board visualization."""

from typing import Any, Callable
import numpy as np

# Core grid type (NumPy-backed for now)
Grid = np.ndarray

# Overlay: modifies matplotlib axis after base render
Overlay = Callable[[Any], None]

# Cell renderer: renders a single grid cell
RenderCell = Callable[[Any, int, int, Any], None]
