"""Tests for module games.catalog.simulation.wordle.words."""

import pytest

from games.catalog.simulation.wordle.words import load_answers
from games.catalog.simulation.wordle.words import load_guesses
from games.catalog.simulation.wordle.words import load_words


@pytest.mark.wordle
def test_load_answers() -> None:
    """The answer list should contain valid five-letter words."""
    answers = load_answers()

    assert answers
    assert all(len(word) == 5 for word in answers)
    assert all(word.isalpha() for word in answers)
    assert all(word == word.upper() for word in answers)


@pytest.mark.wordle
def test_load_guesses() -> None:
    """The additional guess list should contain valid five-letter words."""
    guesses = load_guesses()

    assert guesses
    assert all(len(word) == 5 for word in guesses)
    assert all(word.isalpha() for word in guesses)
    assert all(word == word.upper() for word in guesses)


@pytest.mark.wordle
def test_load_words() -> None:
    """All legal guesses should contain answers and additional guesses."""
    answers = load_answers()
    guesses = load_guesses()

    words = load_words()

    assert words == answers | guesses
