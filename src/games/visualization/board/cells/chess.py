"""Chess-specific renderable cell definitions."""

from typing import Any

import chess
import matplotlib.patheffects as pe


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

    def piece_color(self) -> str:
        """Return logical side."""
        return "white" if self.piece.color == chess.WHITE else "black"

    def render_color(self) -> str:
        """Return display color for the piece."""
        return "#e8e6df" if self.piece_color() == "white" else "#111111"

    def draw(
        self,
        ax: Any,
        x: float,
        y: float,
        board_size: int,
    ) -> bool:
        """Draw chess piece scaled to board size."""
        fontsize = 280 / board_size

        color = self.render_color()
        outline = "#111111" if self.piece_color() == "white" else "#f5f5f5"

        text = ax.text(
            x,
            y,
            self.render_symbol(),
            ha="center",
            va="center",
            color=color,
            fontsize=fontsize,
            fontfamily="DejaVu Sans",
            zorder=3,
        )

        text.set_path_effects([pe.withStroke(linewidth=0.8, foreground=outline)])

        return True
