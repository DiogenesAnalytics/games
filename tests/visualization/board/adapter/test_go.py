"""Tests for module games.visualization.board.adapter.go."""

import pytest
from pytest import FixtureRequest
from sgfmill import boards

from games.visualization.board.adapter.go import GoBoardWrapper
from games.visualization.board.adapter.go import go_board_to_grid
from games.visualization.board.types import Grid


def build_grid(board: boards.Board) -> Grid:
    """Convert an sgfmill Go board into a renderable grid."""
    return go_board_to_grid(GoBoardWrapper(board))


@pytest.fixture(params=[9, 13, 19], scope="function")
def empty_go_board(request: FixtureRequest) -> boards.Board:
    """Provide a parameterized empty sgfmill Go board."""
    return boards.Board(request.param)


@pytest.mark.adapter
def test_go_adapter_single_stone(empty_go_board: boards.Board) -> None:
    """Verify that a single stone is correctly mapped into the grid."""
    board = empty_go_board
    size = board.side

    board.play(3, 3, "b")

    grid = build_grid(board)

    assert grid.shape[0] == size

    cell = grid[3, 3]
    assert cell is not None
    assert cell.render_symbol() == "●"
    assert cell.render_color() == "black"


@pytest.mark.adapter
def test_go_adapter_empty_board(empty_go_board: boards.Board) -> None:
    """Verify that an empty board produces a fully empty render grid."""
    board = empty_go_board
    size = board.side

    grid = build_grid(board)

    assert grid.shape[0] == size
    assert all(cell is None for cell in grid.flatten())


@pytest.mark.adapter
def test_go_adapter_multiple_stones(empty_go_board: boards.Board) -> None:
    """Verify that multiple stones are correctly mapped into the grid."""
    board = empty_go_board
    size = board.side

    placements = [
        (3, 3, "b"),
        (size - 1, size - 1, "w"),
        (5 % size, 7 % size, "b"),
    ]

    for r, c, color in placements:
        board.play(r, c, color)

    grid = build_grid(board)

    for r, c, color in placements:
        cell = grid[r, c]

        assert cell is not None
        assert cell.render_symbol() == "●"
        assert cell.render_color() == ("black" if color == "b" else "white")
