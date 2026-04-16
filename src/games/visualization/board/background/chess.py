"""Chess board background implementation."""

from .checkerboard import CheckerboardBackground


class ChessBackground(CheckerboardBackground):
    """Chessboard visual styling (inherits checker pattern)."""

    def __init__(self) -> None:
        """Initialize a chessboard background."""
        super().__init__()
