"""Tests for the Wordle renderer."""

import pytest

from games.catalog.simulation.wordle.state import WordleState
from games.visualization.wordle.renderer import WordleRenderer


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_text(wordle_state: WordleState) -> None:
    """Render a Wordle state as text."""
    renderer = WordleRenderer()

    result = renderer.render_text(wordle_state)

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
def test_render_html(wordle_state: WordleState) -> None:
    """Render a Wordle state as HTML."""
    renderer = WordleRenderer()

    result = renderer.render_html(wordle_state)

    assert "P" in result
    assert "L" in result
    assert "A" in result
    assert "N" in result
    assert "E" in result
    assert "#787c7e" in result
    assert "#6aaa64" in result


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_image(wordle_state: WordleState) -> None:
    """Render a Wordle state as an SVG image."""
    renderer = WordleRenderer()

    result = renderer.render_image(wordle_state)

    assert result.startswith(b"<svg")
    assert result.endswith(b"</svg>")
    assert result.count(b"<rect") == 30
    assert b"#787c7e" in result
    assert b"#6aaa64" in result


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_state(
    empty_wordle_state: WordleState,
) -> None:
    """Render an empty Wordle state through each representation."""
    renderer = WordleRenderer()

    text = renderer.render_text(empty_wordle_state)
    html = renderer.render_html(empty_wordle_state)
    image = renderer.render_image(empty_wordle_state)

    assert text == "\n".join(["⬜⬜⬜⬜⬜"] * 6)
    assert html.count("#d3d6da") == 30
    assert image.count(b"#d3d6da") == 30


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_does_not_modify_state(
    wordle_state: WordleState,
) -> None:
    """Rendering should not modify the Wordle state."""
    renderer = WordleRenderer()

    guesses = wordle_state.guesses
    feedback = wordle_state.feedback
    candidates = wordle_state.candidates

    renderer.render_text(wordle_state)
    renderer.render_html(wordle_state)
    renderer.render_image(wordle_state)

    assert wordle_state.guesses == guesses
    assert wordle_state.feedback == feedback
    assert wordle_state.candidates == candidates
