"""Background rendering strategies for board visualization."""

from .base import Background
from .checkerboard import CheckerboardBackground
from .solid import SolidBackground

__all__ = [
    "Background",
    "CheckerboardBackground",
    "SolidBackground",
]
