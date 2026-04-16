"""Integration tests for full chess rendering pipeline."""

from typing import Any

import chess
import pytest

from games.visualization.board.adapter.chess import ChessBoardWrapper
from games.visualization.board.adapter.chess import chess_board_to_grid
from tests.visualization.board.integration.helpers import extract_text_positions
from tests.visualization.board.integration.helpers import make_chess_renderer


@pytest.mark.integration
def test_chess_full_render_pipeline() -> None:
    """Ensure full chess pipeline executes without error and produces output.

    Pipeline:
    python-chess → adapter → grid → geometry → renderer → matplotlib
    """
    board = chess.Board()

    wrapper = ChessBoardWrapper(board)
    grid = chess_board_to_grid(wrapper)

    renderer = make_chess_renderer()

    ax: Any = renderer.render(grid, return_ax=True)

    assert len(ax.texts) > 0


@pytest.mark.integration
def test_chess_back_rank_rendered_correctly() -> None:
    """Validate structural correctness of chess back rank placement.

    This ensures geometry is consistent across all pieces, not just one.
    """
    board = chess.Board()

    wrapper = ChessBoardWrapper(board)
    grid = chess_board_to_grid(wrapper)

    ax: Any = make_chess_renderer().render(grid, return_ax=True)

    positions = extract_text_positions(ax)

    # Back rank (white side at y = 7.5)
    expected_back_rank = [
        (0.5, 7.5),
        (1.5, 7.5),
        (2.5, 7.5),
        (3.5, 7.5),
        (4.5, 7.5),
        (5.5, 7.5),
        (6.5, 7.5),
        (7.5, 7.5),
    ]

    for pos in expected_back_rank:
        assert pos in positions
