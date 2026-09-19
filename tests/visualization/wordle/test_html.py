"""Tests for the Wordle HTML renderer."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.state import WordleState
from games.visualization.wordle.html import HtmlWordleRenderer


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_state(wordle_state: WordleState) -> None:
    """Render six empty rows for a new state."""
    renderer = HtmlWordleRenderer()

    result = renderer.render(wordle_state)

    assert result.count("#d3d6da") == 30


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_feedback_tiles(wordle_state: WordleState) -> None:
    """Render letters with their feedback colors."""
    wordle_state.update(
        (
            "SLATE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.YELLOW,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GRAY,
            ),
        )
    )

    renderer = HtmlWordleRenderer()

    result = renderer.render(wordle_state)

    assert "S" in result
    assert "L" in result
    assert "A" in result
    assert "T" in result
    assert "E" in result

    assert "#787c7e" in result
    assert "#c9b458" in result
    assert "#6aaa64" in result


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_multiple_guesses(wordle_state: WordleState) -> None:
    """Render multiple guesses in their existing order."""
    wordle_state.update(
        (
            "SLATE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.YELLOW,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GRAY,
            ),
        )
    )
    wordle_state.update(
        (
            "CRANE",
            (
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
            ),
        )
    )

    renderer = HtmlWordleRenderer()

    result = renderer.render(wordle_state)

    assert result.index("S") < result.index("C")
    assert result.count("#d3d6da") == 20
