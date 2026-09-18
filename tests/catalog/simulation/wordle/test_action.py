"""Tests for the Wordle action module."""

import pytest

from games.catalog.simulation.wordle.action import WordleGuess


@pytest.mark.wordle
def test_wordle_guess_initializes_with_word() -> None:
    """Test that a Wordle guess stores its proposed word."""
    guess = WordleGuess("CRANE")

    assert guess.word == "CRANE"


@pytest.mark.wordle
def test_wordle_guess_is_initially_invalid() -> None:
    """Test that a new Wordle guess is initially invalid."""
    guess = WordleGuess("CRANE")

    assert not guess.is_valid


@pytest.mark.wordle
def test_wordle_guess_is_initially_unresolved() -> None:
    """Test that a new Wordle guess is initially unresolved."""
    guess = WordleGuess("CRANE")

    assert not guess.is_resolved


@pytest.mark.wordle
def test_wordle_guess_has_no_executor_initially() -> None:
    """Test that a new Wordle guess has no executor."""
    guess = WordleGuess("CRANE")

    assert guess.executor is None


@pytest.mark.wordle
def test_wordle_guess_can_be_validated() -> None:
    """Test that a Wordle guess can be validated."""
    guess = WordleGuess("CRANE")

    guess.validate()

    assert guess.is_valid


@pytest.mark.wordle
def test_wordle_guess_describes_itself() -> None:
    """Test the human-readable description of a Wordle guess."""
    guess = WordleGuess("CRANE")

    assert guess.describe() == "Guess 'CRANE'"


@pytest.mark.wordle
def test_wordle_guess_repr() -> None:
    """Test the representation of a Wordle guess."""
    guess = WordleGuess("CRANE")

    assert repr(guess) == "<WordleGuess: valid=False, desc=\"Guess 'CRANE'\">"


@pytest.mark.wordle
def test_wordle_guess_can_be_invalidated() -> None:
    """Test that a Wordle guess can be invalidated."""
    guess = WordleGuess("CRANE")

    guess.validate()
    guess.invalidate()

    assert not guess.is_valid
    assert not guess.is_resolved
    assert guess.executor is None


@pytest.mark.wordle
def test_wordle_guess_normalizes_word() -> None:
    """A Wordle guess should normalize its word to uppercase."""
    action = WordleGuess("slate")

    assert action.word == "SLATE"
