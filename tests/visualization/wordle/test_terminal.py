"""Tests for module games.visualization.wordle.terminal."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.state import WordleState
from games.visualization.wordle.terminal import TerminalWordleRenderer


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_empty_state() -> None:
    """An empty Wordle state should render six empty rows."""
    state = WordleState({"CRANE"}, "CRANE")
    renderer = TerminalWordleRenderer()

    rendered = renderer.render(state)

    assert rendered == "\n".join(["⬜⬜⬜⬜⬜"] * 6)


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_single_guess() -> None:
    """A single guess should render in the first row."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")
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
    renderer = TerminalWordleRenderer()

    rendered = renderer.render(state)

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

    assert rendered == expected


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_multiple_guesses() -> None:
    """Multiple guesses should render in the order they were made."""
    state = WordleState(
        {"CRANE", "PLANE", "SLATE"},
        "CRANE",
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
    state.update(
        (
            "SLATE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
                FeedbackTile.GRAY,
                FeedbackTile.GREEN,
            ),
        )
    )
    renderer = TerminalWordleRenderer()

    rendered = renderer.render(state)

    expected = "\n".join(
        [
            "⬛P⬛L🟩A🟩N🟩E",
            "⬛S⬛L🟩A⬛T🟩E",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
        ]
    )

    assert rendered == expected


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_does_not_modify_state() -> None:
    """Rendering should not modify the Wordle state."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")
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
    renderer = TerminalWordleRenderer()

    guesses = state.guesses
    state_feedback = state.feedback
    candidates = state.candidates

    renderer.render(state)

    assert state.guesses == guesses
    assert state.feedback == state_feedback
    assert state.candidates == candidates


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_six_guesses() -> None:
    """Six guesses should fill all six rows."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")

    result = (
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GREEN,
        FeedbackTile.GREEN,
        FeedbackTile.GREEN,
    )

    for _ in range(6):
        state.update(("PLANE", result))

    renderer = TerminalWordleRenderer()

    rendered = renderer.render(state)

    assert rendered.count("\n") == 5
    assert all(row == "⬛P⬛L🟩A🟩N🟩E" for row in rendered.splitlines())


@pytest.mark.renderer
@pytest.mark.wordle
def test_render_yellow_feedback() -> None:
    """Yellow feedback should render with yellow tiles."""
    state = WordleState({"CRANE", "RECAP"}, "CRANE")
    state.update(
        (
            "RECAP",
            (
                FeedbackTile.YELLOW,
                FeedbackTile.YELLOW,
                FeedbackTile.YELLOW,
                FeedbackTile.YELLOW,
                FeedbackTile.GRAY,
            ),
        )
    )
    renderer = TerminalWordleRenderer()

    rendered = renderer.render(state)

    expected = "\n".join(
        [
            "🟨R🟨E🟨C🟨A⬛P",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜",
        ]
    )

    assert rendered == expected
