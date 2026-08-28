"""Tests for the Wordle feedback mechanism."""

import pytest

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.feedback import feedback


@pytest.mark.wordle
def test_all_green() -> None:
    """Test feedback when the guess exactly matches the target."""
    assert feedback("CRANE", "CRANE") == (
        FeedbackTile.GREEN,
        FeedbackTile.GREEN,
        FeedbackTile.GREEN,
        FeedbackTile.GREEN,
        FeedbackTile.GREEN,
    )


@pytest.mark.wordle
def test_all_gray() -> None:
    """Test feedback when no guessed letters occur in the target."""
    assert feedback("CRANE", "BLITZ") == (
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
    )


@pytest.mark.wordle
def test_yellow() -> None:
    """Test feedback for letters present in the wrong positions."""
    assert feedback("CRANE", "EAGLE") == (
        FeedbackTile.GRAY,
        FeedbackTile.YELLOW,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GREEN,
    )


@pytest.mark.wordle
def test_mixed_feedback() -> None:
    """Test feedback containing green, yellow, and gray tiles."""
    assert feedback("CRANE", "CARDS") == (
        FeedbackTile.GREEN,
        FeedbackTile.YELLOW,
        FeedbackTile.YELLOW,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
    )


@pytest.mark.wordle
def test_repeated_guess_letter_consumed_by_green() -> None:
    """Test that a green match consumes the corresponding target letter."""
    assert feedback("CRANE", "EERIE") == (
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.YELLOW,
        FeedbackTile.GRAY,
        FeedbackTile.GREEN,
    )


@pytest.mark.wordle
def test_repeated_target_letter() -> None:
    """Test feedback when the target contains repeated letters."""
    assert feedback("SHEEP", "EERIE") == (
        FeedbackTile.YELLOW,
        FeedbackTile.YELLOW,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
    )


@pytest.mark.wordle
def test_repeated_target_and_guess_letters() -> None:
    """Test feedback when both target and guess contain repeated letters."""
    assert feedback("SHEEP", "EASES") == (
        FeedbackTile.YELLOW,
        FeedbackTile.GRAY,
        FeedbackTile.YELLOW,
        FeedbackTile.GREEN,
        FeedbackTile.GRAY,
    )


@pytest.mark.wordle
def test_feedback_is_case_insensitive() -> None:
    """Test that feedback is independent of capitalization."""
    assert feedback("crane", "arise") == feedback("CRANE", "ARISE")


@pytest.mark.wordle
def test_target_must_have_five_letters() -> None:
    """Test that the target must contain exactly five letters."""
    with pytest.raises(ValueError):
        feedback("CRANEY", "CRANE")


@pytest.mark.wordle
def test_guess_must_have_five_letters() -> None:
    """Test that the guess must contain exactly five letters."""
    with pytest.raises(ValueError):
        feedback("CRANE", "CRAN")
