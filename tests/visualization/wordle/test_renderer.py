"""Tests for the Wordle renderer."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.state import WordleState
from games.visualization.wordle.renderer import WordleRenderer


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_text() -> None:
    """Render a Wordle state as text."""
    state = WordleState(
        solutions={"CRANE", "PLANE"},
        available_guesses={"CRANE", "PLANE"},
        target="CRANE",
    )
    state.update(
        (
            "PLANE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
            ),
        )
    )
    renderer = WordleRenderer()

    result = renderer.render_text(state)

    expected = "\n".join(
        [
            "⬛P⬛L🟩A🟩N🟩E",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
        ]
    )

    assert result == expected


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_html() -> None:
    """Render a Wordle state as HTML."""
    state = WordleState(
        solutions={"CRANE", "PLANE"},
        available_guesses={"CRANE", "PLANE"},
        target="CRANE",
    )
    state.update(
        (
            "PLANE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
            ),
        )
    )
    renderer = WordleRenderer()

    result = renderer.render_html(state)

    assert "P" in result
    assert "L" in result
    assert "A" in result
    assert "N" in result
    assert "E" in result
    assert "#787c7e" in result
    assert "#6aaa64" in result


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_image() -> None:
    """Render a Wordle state as an SVG image."""
    state = WordleState(
        solutions={"CRANE", "PLANE"},
        available_guesses={"CRANE", "PLANE"},
        target="CRANE",
    )
    state.update(
        (
            "PLANE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
            ),
        )
    )
    renderer = WordleRenderer()

    result = renderer.render_image(state)

    assert result.startswith(b"<svg")
    assert result.endswith(b"</svg>")
    assert result.count(b"<rect") == 30
    assert b"#787c7e" in result
    assert b"#6aaa64" in result


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_state() -> None:
    """Render an empty Wordle state through each representation."""
    state = WordleState(
        solutions={"CRANE"},
        available_guesses={"CRANE"},
        target="CRANE",
    )
    renderer = WordleRenderer()

    text = renderer.render_text(state)
    html = renderer.render_html(state)
    image = renderer.render_image(state)

    assert text == "\n".join(["⬜⬜⬜⬜⬜"] * 6)
    assert html.count("#d3d6da") == 30
    assert image.count(b"#d3d6da") == 30


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_does_not_modify_state() -> None:
    """Rendering should not modify the Wordle state."""
    state = WordleState(
        solutions={"CRANE", "PLANE"},
        available_guesses={"CRANE", "PLANE"},
        target="CRANE",
    )
    state.update(
        (
            "PLANE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
                FeedbackTile.GREEN,
            ),
        )
    )
    renderer = WordleRenderer()

    guesses = state.guesses
    feedback = state.feedback
    candidates = state.candidates

    renderer.render_text(state)
    renderer.render_html(state)
    renderer.render_image(state)

    assert state.guesses == guesses
    assert state.feedback == feedback
    assert state.candidates == candidates
