"""Chess-specific cell rendering functions."""
"""
Chess cell rendering using python-chess symbols.
"""

from typing import Any
import chess


_piece_unicode = {
    "P": "♟", "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}


def render_chess_cell(ax: Any, r: int, c: int, value: chess.Piece) -> None:
    """
    Render a chess piece at a given board coordinate.

    value is expected to be a python-chess Piece (not int encoding).
    """

    if value is None:
        return

    symbol = _piece_unicode[value.symbol()]
    color = "white" if value.color else "black"

    ax.text(
        c + 0.5,
        r + 0.5,
        symbol,
        ha="center",
        va="center",
        fontsize=22,
        color=color,
    )
