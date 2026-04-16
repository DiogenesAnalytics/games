"""Integration tests for full Go rendering pipeline."""

from typing import Any

import pytest
from sgfmill import boards

from games.visualization.board.adapter.go import GoBoardWrapper
from games.visualization.board.adapter.go import go_board_to_grid
from tests.visualization.board.integration.helpers import extract_text_positions
from tests.visualization.board.integration.helpers import make_go_renderer


@pytest.mark.integration
def test_go_full_render_pipeline() -> None:
    """Ensure Go pipeline executes end-to-end without failure.

    Pipeline:
    sgfmill → adapter → grid → geometry → renderer
    """
    board = boards.Board(9)
    board.play(3, 3, "b")

    wrapper = GoBoardWrapper(board)
    grid = go_board_to_grid(wrapper)

    ax: Any = make_go_renderer().render(grid, return_ax=True)

    assert len(ax.texts) >= 1


@pytest.mark.integration
def test_go_stone_positions_are_correct() -> None:
    """Validate Go geometry correctness (identity mapping)."""
    board = boards.Board(9)
    board.play(3, 3, "b")

    wrapper = GoBoardWrapper(board)
    grid = go_board_to_grid(wrapper)

    ax: Any = make_go_renderer().render(grid, return_ax=True)

    positions = extract_text_positions(ax)

    # Identity geometry: (c, r)
    assert (3.0, 3.0) in positions

    # No phantom rendering
    assert len(positions) == 1
