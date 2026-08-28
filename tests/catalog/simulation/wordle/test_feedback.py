"""Tests for the Wordle feedback mechanism."""

import pytest

from games.catalog.simulation.wordle.feedback import CountConstraint
from games.catalog.simulation.wordle.feedback import FeedbackInformation
from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.feedback import feedback
from games.catalog.simulation.wordle.feedback import interpret_feedback


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


@pytest.mark.wordle
def test_interpret_all_green() -> None:
    """Test information decoded from entirely green feedback."""
    result = interpret_feedback(
        "CRANE",
        (
            FeedbackTile.GREEN,
            FeedbackTile.GREEN,
            FeedbackTile.GREEN,
            FeedbackTile.GREEN,
            FeedbackTile.GREEN,
        ),
    )

    assert result == FeedbackInformation(
        required={
            0: "C",
            1: "R",
            2: "A",
            3: "N",
            4: "E",
        },
        excluded={},
        counts={
            "C": CountConstraint(1, None),
            "R": CountConstraint(1, None),
            "A": CountConstraint(1, None),
            "N": CountConstraint(1, None),
            "E": CountConstraint(1, None),
        },
    )


@pytest.mark.wordle
def test_interpret_all_gray() -> None:
    """Test information decoded from entirely gray feedback."""
    result = interpret_feedback(
        "BLITZ",
        (
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
        ),
    )

    assert result == FeedbackInformation(
        required={},
        excluded={
            0: {"B"},
            1: {"L"},
            2: {"I"},
            3: {"T"},
            4: {"Z"},
        },
        counts={
            "B": CountConstraint(0, 0),
            "L": CountConstraint(0, 0),
            "I": CountConstraint(0, 0),
            "T": CountConstraint(0, 0),
            "Z": CountConstraint(0, 0),
        },
    )


@pytest.mark.wordle
def test_interpret_yellow() -> None:
    """Test information decoded from yellow feedback."""
    result = interpret_feedback(
        "EAGLE",
        (
            FeedbackTile.GRAY,
            FeedbackTile.YELLOW,
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
            FeedbackTile.GREEN,
        ),
    )

    assert result == FeedbackInformation(
        required={
            4: "E",
        },
        excluded={
            0: {"E"},
            1: {"A"},
            2: {"G"},
            3: {"L"},
        },
        counts={
            "E": CountConstraint(1, 1),
            "A": CountConstraint(1, None),
            "G": CountConstraint(0, 0),
            "L": CountConstraint(0, 0),
        },
    )


@pytest.mark.wordle
def test_interpret_repeated_letters() -> None:
    """Test information decoded from repeated letters."""
    result = interpret_feedback(
        "EERIE",
        (
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
            FeedbackTile.YELLOW,
            FeedbackTile.GRAY,
            FeedbackTile.GREEN,
        ),
    )

    assert result == FeedbackInformation(
        required={
            4: "E",
        },
        excluded={
            0: {"E"},
            1: {"E"},
            2: {"R"},
            3: {"I"},
        },
        counts={
            "E": CountConstraint(1, 1),
            "R": CountConstraint(1, None),
            "I": CountConstraint(0, 0),
        },
    )


@pytest.mark.wordle
def test_interpret_repeated_target_and_guess_letters() -> None:
    """Test information decoded from repeated target and guess letters."""
    result = interpret_feedback(
        "EASES",
        (
            FeedbackTile.YELLOW,
            FeedbackTile.GRAY,
            FeedbackTile.YELLOW,
            FeedbackTile.GREEN,
            FeedbackTile.GRAY,
        ),
    )

    assert result == FeedbackInformation(
        required={
            3: "E",
        },
        excluded={
            0: {"E"},
            1: {"A"},
            2: {"S"},
            4: {"S"},
        },
        counts={
            "E": CountConstraint(2, None),
            "A": CountConstraint(0, 0),
            "S": CountConstraint(1, 1),
        },
    )


@pytest.mark.wordle
def test_interpret_guess_must_have_five_letters() -> None:
    """Test that interpretation requires a five-letter guess."""
    with pytest.raises(ValueError):
        interpret_feedback(
            "CRAN",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
            ),
        )


@pytest.mark.wordle
def test_interpret_feedback_must_have_five_tiles() -> None:
    """Test that interpretation requires five feedback tiles."""
    with pytest.raises(ValueError):
        interpret_feedback(
            "CRANE",
            (
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
                FeedbackTile.GRAY,
            ),
        )
