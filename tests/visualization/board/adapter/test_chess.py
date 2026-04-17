"""Tests for module games.visualization.board.adapter.chess."""

import chess
import pytest

from games.visualization.board.adapter.chess import ChessBoardWrapper
from games.visualization.board.adapter.chess import chess_board_to_grid


@pytest.mark.adapter
def test_chess_adapter_single_piece() -> None:
    """Adapter should map a single piece to correct grid position."""
    board = chess.Board()
    board.clear()

    square = chess.E4
    board.set_piece_at(square, chess.Piece(chess.KING, chess.WHITE))

    wrapper = ChessBoardWrapper(board)
    grid = chess_board_to_grid(wrapper)

    assert grid.shape == (8, 8)

    r, c = divmod(square, 8)
    cell = grid[r, c]

    assert cell is not None

    assert cell.render_symbol() is not None
    assert cell.piece_color() == "white"


@pytest.mark.adapter
def test_chess_adapter_empty_board() -> None:
    """Empty board should produce a grid of all None."""
    board = chess.Board()
    board.clear()

    wrapper = ChessBoardWrapper(board)
    grid = chess_board_to_grid(wrapper)

    assert all(cell is None for cell in grid.flatten())


@pytest.mark.adapter
def test_chess_adapter_multiple_pieces() -> None:
    """Adapter should correctly map multiple pieces."""
    board = chess.Board()
    board.clear()

    placements = {
        chess.A1: chess.Piece(chess.ROOK, chess.WHITE),
        chess.H8: chess.Piece(chess.KING, chess.BLACK),
        chess.E4: chess.Piece(chess.PAWN, chess.WHITE),
    }

    for square, piece in placements.items():
        board.set_piece_at(square, piece)

    wrapper = ChessBoardWrapper(board)
    grid = chess_board_to_grid(wrapper)

    for square in placements:
        r, c = divmod(square, 8)
        cell = grid[r, c]

        assert cell is not None

        assert cell.render_symbol() is not None
        assert cell.piece_color() in {"white", "black"}


@pytest.mark.adapter
def test_chess_adapter_fen_position() -> None:
    """Adapter should correctly map a known FEN position."""
    board = chess.Board("8/8/8/4k3/4P3/8/5K2/5R2 w - - 0 1")

    wrapper = ChessBoardWrapper(board)
    grid = chess_board_to_grid(wrapper)

    # e5 black king
    r, c = divmod(chess.E5, 8)
    cell = grid[r, c]
    assert cell is not None
    assert cell.piece_color() == "black"

    # e4 white pawn
    r, c = divmod(chess.E4, 8)
    cell = grid[r, c]
    assert cell is not None
    assert cell.piece_color() == "white"

    # f1 white rook
    r, c = divmod(chess.F1, 8)
    cell = grid[r, c]
    assert cell is not None
    assert cell.piece_color() == "white"
