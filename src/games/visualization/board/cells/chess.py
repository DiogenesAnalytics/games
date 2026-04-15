"""Chess-specific renderable cell definitions."""

import chess


_piece_unicode = {
    "P": "♟",
    "N": "♞",
    "B": "♝",
    "R": "♜",
    "Q": "♛",
    "K": "♚",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}


class ChessPiece:
    """Renderable representation of a chess piece for visualization."""

    def __init__(self, piece: chess.Piece) -> None:
        """Initialize a renderable wrapper around a python-chess Piece."""
        self.piece = piece

    def render_symbol(self) -> str:
        """Return glyph based directly on python-chess symbol."""
        return _piece_unicode[self.piece.symbol()]

    def render_color(self) -> str:
        """Return rendering color for the piece."""
        return "white" if self.piece.color == chess.WHITE else "black"
