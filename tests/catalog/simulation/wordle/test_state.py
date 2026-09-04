"""Tests for the Wordle state implementation."""

from typing import Set

import pytest

from games.catalog.simulation.wordle.feedback import CountConstraint
from games.catalog.simulation.wordle.feedback import FeedbackInformation
from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.feedback import feedback
from games.catalog.simulation.wordle.state import WordleState


@pytest.fixture
def solutions() -> Set[str]:
    """Return a small solution dictionary for testing."""
    return {"CRANE", "STAIN", "PLANE"}


@pytest.fixture
def state(solutions: Set[str]) -> WordleState:
    """Return a freshly initialized Wordle state."""
    return WordleState(
        solutions=solutions,
        target="CRANE",
    )


@pytest.mark.wordle
def test_initial_state(
    state: WordleState,
    solutions: Set[str],
) -> None:
    """Test that a new state begins with every solution as a candidate."""
    assert state.solutions == solutions
    assert state.target == "CRANE"
    assert state.candidates == solutions
    assert state.guesses == []
    assert state.feedback == []


@pytest.mark.wordle
def test_target_must_be_solution(
    solutions: Set[str],
) -> None:
    """Test that the target must belong to the solution dictionary."""
    with pytest.raises(ValueError):
        WordleState(
            solutions=solutions,
            target="BRICK",
        )


@pytest.mark.wordle
def test_words_are_normalized(
    state: WordleState,
) -> None:
    """Test that solution and target words are normalized to uppercase."""
    assert state.target == "CRANE"
    assert state.solutions == {"CRANE", "STAIN", "PLANE"}


@pytest.mark.wordle
def test_solutions_are_copied(
    state: WordleState,
    solutions: Set[str],
) -> None:
    """Test that external mutation cannot modify the solution dictionary."""
    solutions.add("BRICK")

    assert state.solutions == {"CRANE", "STAIN", "PLANE"}


@pytest.mark.wordle
def test_candidates_are_copied(
    state: WordleState,
) -> None:
    """Test that callers cannot mutate the candidate set directly."""
    candidates = state.candidates

    candidates.remove("CRANE")

    assert state.candidates == {"CRANE", "STAIN", "PLANE"}


@pytest.mark.wordle
def test_available_values_matches_candidates(
    state: WordleState,
) -> None:
    """Test that available state values are the current candidates."""
    assert state.available_values == state.candidates


@pytest.mark.wordle
def test_reset_restores_initial_state(
    state: WordleState,
) -> None:
    """Test that reset restores the initial candidate and history state."""
    state._candidates.remove("CRANE")
    state._guesses.append("STAIN")

    state.reset()

    assert state.candidates == state.solutions
    assert state.guesses == []
    assert state.feedback == []


@pytest.mark.wordle
def test_initial_state_is_valid(
    state: WordleState,
) -> None:
    """Test that a properly initialized state is valid."""
    assert state.is_valid()


@pytest.mark.wordle
def test_candidates_must_be_subset_of_solutions(
    state: WordleState,
) -> None:
    """Test that a valid state cannot contain unknown candidates."""
    state._candidates.add("BRICK")

    assert not state.is_valid()


@pytest.mark.wordle
def test_guess_and_feedback_histories_have_equal_length(
    state: WordleState,
) -> None:
    """Test that every guess must have corresponding feedback."""
    state._guesses.append("STAIN")

    assert not state.is_valid()


@pytest.mark.wordle
def test_update_records_guess_and_feedback(
    state: WordleState,
) -> None:
    """Test that update records a guess and its feedback."""
    result = (
        FeedbackTile.GREEN,
        FeedbackTile.YELLOW,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
        FeedbackTile.GRAY,
    )

    state.update(("CRANE", result))

    assert state.guesses == ["CRANE"]
    assert state.feedback == [result]


@pytest.mark.wordle
def test_update_reduces_candidates(
    state: WordleState,
) -> None:
    """Test that update removes candidates inconsistent with feedback."""
    result = feedback(state.target, "STAIN")

    state.update(("STAIN", result))

    assert state.candidates == {"CRANE", "PLANE"}


@pytest.mark.wordle
def test_matches_information_accepts_matching_word() -> None:
    """Test that a word satisfying all constraints is accepted."""
    state = WordleState(
        solutions={"CRANE", "CRATE", "GRAPE"},
        target="CRANE",
    )

    information = FeedbackInformation(
        required={
            0: "C",
        },
        excluded={
            2: {"R"},
        },
        counts={
            "C": CountConstraint(1, 1),
        },
    )

    assert state._matches_information("CRATE", information)


@pytest.mark.wordle
def test_matches_information_rejects_wrong_required_position() -> None:
    """Test that a word violating a required position is rejected."""
    state = WordleState(
        solutions={"CRANE"},
        target="CRANE",
    )

    information = FeedbackInformation(
        required={
            0: "C",
        },
        excluded={},
        counts={},
    )

    assert not state._matches_information("GRANE", information)


@pytest.mark.wordle
def test_matches_information_rejects_excluded_position() -> None:
    """Test that a word containing an excluded letter at a position is rejected."""
    state = WordleState(
        solutions={"CRANE"},
        target="CRANE",
    )

    information = FeedbackInformation(
        required={},
        excluded={
            1: {"R"},
        },
        counts={},
    )

    assert not state._matches_information("CRANE", information)


@pytest.mark.wordle
def test_matches_information_enforces_minimum_count() -> None:
    """Test that the minimum letter count is enforced."""
    state = WordleState(
        solutions={"CRANE"},
        target="CRANE",
    )

    information = FeedbackInformation(
        required={},
        excluded={},
        counts={
            "R": CountConstraint(2, None),
        },
    )

    assert not state._matches_information("CRANE", information)


@pytest.mark.wordle
def test_matches_information_enforces_maximum_count() -> None:
    """Test that the maximum letter count is enforced."""
    state = WordleState(
        solutions={"SHEEP"},
        target="SHEEP",
    )

    information = FeedbackInformation(
        required={},
        excluded={},
        counts={
            "E": CountConstraint(0, 1),
        },
    )

    assert not state._matches_information("SHEEP", information)


@pytest.mark.wordle
def test_matches_information_accepts_unbounded_maximum() -> None:
    """Test that an unbounded maximum allows additional occurrences."""
    state = WordleState(
        solutions={"SHEEP"},
        target="SHEEP",
    )

    information = FeedbackInformation(
        required={},
        excluded={},
        counts={
            "E": CountConstraint(1, None),
        },
    )

    assert state._matches_information("SHEEP", information)


@pytest.mark.wordle
def test_initial_state_is_not_terminal() -> None:
    """A newly initialized state should not be terminal."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")

    assert not state.is_terminal


@pytest.mark.wordle
def test_state_is_terminal_when_target_is_guessed() -> None:
    """A state should be terminal when the target has been guessed."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")

    state.update(("CRANE", feedback("CRANE", "CRANE")))

    assert state.is_terminal


@pytest.mark.wordle
def test_state_is_not_terminal_after_fewer_than_six_incorrect_guesses() -> None:
    """An incorrect guess before the sixth guess should not be terminal."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")

    for guess in ["PLANE"]:
        state.update((guess, feedback("CRANE", guess)))

    assert not state.is_terminal


@pytest.mark.wordle
def test_state_is_terminal_after_six_guesses() -> None:
    """A state should be terminal after six guesses."""
    state = WordleState({"CRANE", "PLANE"}, "CRANE")

    for guess in ["PLANE"] * 6:
        state.update((guess, feedback("CRANE", guess)))

    assert state.is_terminal
