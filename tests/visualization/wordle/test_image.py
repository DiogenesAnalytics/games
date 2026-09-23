"""Tests for the Wordle image renderer."""

from xml.dom import minidom

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell
from games.visualization.wordle.image import ImageRenderer


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_board(
    empty_wordle_board: WordleBoard,
) -> None:
    """Render an empty Wordle board as SVG."""
    renderer = ImageRenderer()

    result = renderer.render(empty_wordle_board)

    minidom.parseString(result)

    assert result.startswith(b"<svg")
    assert result.endswith(b"</svg>")
    assert result.count(b"<rect") == 30
    assert result.count(b"#d3d6da") == 30


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_feedback_tiles() -> None:
    """Render feedback tiles with their corresponding colors."""
    board = WordleBoard(
        (
            (
                WordleCell("S", FeedbackTile.GRAY),
                WordleCell("L", FeedbackTile.YELLOW),
                WordleCell("A", FeedbackTile.GRAY),
                WordleCell("T", FeedbackTile.GREEN),
                WordleCell("E", FeedbackTile.GRAY),
            ),
        )
    )

    renderer = ImageRenderer()

    result = renderer.render(board)

    assert b">S<" in result
    assert b">L<" in result
    assert b">A<" in result
    assert b">T<" in result
    assert b">E<" in result

    assert b"#787c7e" in result
    assert b"#c9b458" in result
    assert b"#6aaa64" in result


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_multiple_rows() -> None:
    """Render multiple board rows in their existing order."""
    board = WordleBoard(
        (
            (
                WordleCell("S", FeedbackTile.GRAY),
                WordleCell("L", FeedbackTile.YELLOW),
                WordleCell("A", FeedbackTile.GRAY),
                WordleCell("T", FeedbackTile.GREEN),
                WordleCell("E", FeedbackTile.GRAY),
            ),
            (
                WordleCell("C", FeedbackTile.GREEN),
                WordleCell("R", FeedbackTile.GREEN),
                WordleCell("A", FeedbackTile.GREEN),
                WordleCell("N", FeedbackTile.GREEN),
                WordleCell("E", FeedbackTile.GREEN),
            ),
        )
    )

    renderer = ImageRenderer()

    result = renderer.render(board)

    assert result.index(b">S<") < result.index(b">C<")
    assert result.count(b"<rect") == 10
    assert result.count(b"#d3d6da") == 0


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_unsupported_format(
    empty_wordle_board: WordleBoard,
) -> None:
    """Reject unsupported image formats."""
    renderer = ImageRenderer()

    with pytest.raises(ValueError, match="Unsupported image format"):
        renderer.render(empty_wordle_board, "png")
