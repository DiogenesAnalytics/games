"""Tests for module games.visualization.wordle.text."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell
from games.visualization.wordle.text import TextRenderer


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_board(
    empty_wordle_board: WordleBoard,
) -> None:
    """An empty Wordle board should render six empty rows."""
    renderer = TextRenderer()

    rendered = renderer.render(empty_wordle_board)

    assert rendered == "\n".join(["⬜⬜⬜⬜⬜"] * 6)


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_single_row() -> None:
    """A row with feedback should render its letters and tiles."""
    board = WordleBoard(
        (
            (
                WordleCell("P", FeedbackTile.GRAY),
                WordleCell("L", FeedbackTile.GRAY),
                WordleCell("A", FeedbackTile.GREEN),
                WordleCell("N", FeedbackTile.GREEN),
                WordleCell("E", FeedbackTile.GREEN),
            ),
        )
    )
    renderer = TextRenderer()

    rendered = renderer.render(board)

    assert rendered == "⬛P⬛L🟩A🟩N🟩E"


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_multiple_rows() -> None:
    """Multiple rows should render in their existing order."""
    board = WordleBoard(
        (
            (
                WordleCell("P", FeedbackTile.GRAY),
                WordleCell("L", FeedbackTile.GRAY),
                WordleCell("A", FeedbackTile.GREEN),
                WordleCell("N", FeedbackTile.GREEN),
                WordleCell("E", FeedbackTile.GREEN),
            ),
            (
                WordleCell("S", FeedbackTile.GRAY),
                WordleCell("L", FeedbackTile.GRAY),
                WordleCell("A", FeedbackTile.GREEN),
                WordleCell("T", FeedbackTile.GRAY),
                WordleCell("E", FeedbackTile.GREEN),
            ),
        )
    )
    renderer = TextRenderer()

    rendered = renderer.render(board)

    expected = "\n".join(
        [
            "⬛P⬛L🟩A🟩N🟩E",
            "⬛S⬛L🟩A⬛T🟩E",
        ]
    )

    assert rendered == expected


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_yellow_feedback() -> None:
    """Yellow feedback should render with yellow tiles."""
    board = WordleBoard(
        (
            (
                WordleCell("R", FeedbackTile.YELLOW),
                WordleCell("E", FeedbackTile.YELLOW),
                WordleCell("C", FeedbackTile.YELLOW),
                WordleCell("A", FeedbackTile.YELLOW),
                WordleCell("P", FeedbackTile.GRAY),
            ),
        )
    )
    renderer = TextRenderer()

    rendered = renderer.render(board)

    assert rendered == "🟨R🟨E🟨C🟨A⬛P"


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_cells() -> None:
    """Cells without letters or feedback should render as empty tiles."""
    board = WordleBoard(
        (
            (
                WordleCell(None, None),
                WordleCell(None, None),
                WordleCell(None, None),
                WordleCell(None, None),
                WordleCell(None, None),
            ),
        )
    )
    renderer = TextRenderer()

    rendered = renderer.render(board)

    assert rendered == "⬜⬜⬜⬜⬜"
