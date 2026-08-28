"""Defines the Wordle feedback mechanism."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple


class FeedbackTile(Enum):
    """Represent the possible feedback values for a Wordle tile."""

    GREEN = "green"
    YELLOW = "yellow"
    GRAY = "gray"


Feedback = Tuple[FeedbackTile, ...]


@dataclass(frozen=True)
class CountConstraint:
    """Represent lower and upper bounds on a letter's occurrence count."""

    minimum: int
    maximum: Optional[int]


@dataclass(frozen=True)
class FeedbackInformation:
    """Represent the information encoded by Wordle feedback.

    Attributes:
        required: Letters known to occur at specific positions.
        excluded: Letters known not to occur at specific positions.
        counts: Minimum and maximum occurrence constraints for letters.
    """

    required: Dict[int, str]
    excluded: Dict[int, Set[str]]
    counts: Dict[str, CountConstraint]


def _validate_word_length(word: str, name: str) -> None:
    """Validate that a Wordle word contains exactly five letters.

    Args:
        word: The word to validate.
        name: The name to use in the error message.

    Raises:
        ValueError: If the word does not contain exactly five letters.
    """
    if len(word) != 5:
        raise ValueError(f"{name} must contain exactly five letters.")


def _validate_feedback(result: Feedback) -> None:
    """Validate that Wordle feedback contains five valid tiles.

    Args:
        result: The feedback to validate.

    Raises:
        ValueError: If the feedback does not contain exactly five tiles or
            contains an invalid tile.
    """
    if len(result) != 5:
        raise ValueError("Feedback must contain exactly five tiles.")

    if not all(isinstance(tile, FeedbackTile) for tile in result):
        raise ValueError("Feedback contains an invalid tile.")


def feedback(target: str, guess: str) -> Feedback:
    """Generate Wordle feedback for a guess against a target.

    Args:
        target: The hidden solution word.
        guess: The word being evaluated.

    Returns:
        A five-element tuple containing the feedback for each letter.
    """
    target = target.upper()
    guess = guess.upper()

    _validate_word_length(target, "Target")
    _validate_word_length(guess, "Guess")

    result = [FeedbackTile.GRAY] * 5
    remaining: List[Optional[str]] = list(target)

    # First identify exact matches.
    for index, letter in enumerate(guess):
        if letter == target[index]:
            result[index] = FeedbackTile.GREEN
            remaining[index] = None

    # Then identify letters occurring elsewhere in the target.
    for index, letter in enumerate(guess):
        if result[index] is FeedbackTile.GREEN:
            continue

        if letter in remaining:
            result[index] = FeedbackTile.YELLOW
            remaining[remaining.index(letter)] = None

    return tuple(result)


def interpret_feedback(
    guess: str,
    result: Feedback,
) -> FeedbackInformation:
    """Decode Wordle feedback into its information content.

    Args:
        guess: The word that produced the feedback.
        result: The feedback associated with the guess.

    Returns:
        The positional and letter-count constraints encoded by the feedback.
    """
    guess = guess.upper()

    _validate_word_length(guess, "Guess")
    _validate_feedback(result)

    required: Dict[int, str] = {}
    excluded: Dict[int, Set[str]] = {}
    positive_counts: Dict[str, int] = {}
    gray_counts: Set[str] = set()

    for index, (letter, tile) in enumerate(zip(guess, result, strict=True)):
        if tile is FeedbackTile.GREEN:
            required[index] = letter
            positive_counts[letter] = positive_counts.get(letter, 0) + 1

        elif tile is FeedbackTile.YELLOW:
            excluded.setdefault(index, set()).add(letter)
            positive_counts[letter] = positive_counts.get(letter, 0) + 1

        else:
            excluded.setdefault(index, set()).add(letter)
            gray_counts.add(letter)

    counts: Dict[str, CountConstraint] = {}

    for letter in set(guess):
        minimum = positive_counts.get(letter, 0)

        if letter in gray_counts:
            maximum = minimum
        else:
            maximum = None

        if minimum > 0 or maximum == 0:
            counts[letter] = CountConstraint(
                minimum=minimum,
                maximum=maximum,
            )

    return FeedbackInformation(
        required=required,
        excluded=excluded,
        counts=counts,
    )
