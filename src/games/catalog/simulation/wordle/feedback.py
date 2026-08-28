"""Defines the Wordle feedback mechanism."""

from enum import Enum
from typing import List
from typing import Optional
from typing import Tuple


class FeedbackTile(Enum):
    """Represent the possible feedback values for a Wordle tile."""

    GREEN = "green"
    YELLOW = "yellow"
    GRAY = "gray"


Feedback = Tuple[FeedbackTile, ...]


def feedback(target: str, guess: str) -> Feedback:
    """Generate Wordle feedback for a guess against a target.

    Args:
        target: The hidden solution word.
        guess: The word being evaluated.

    Returns:
        A five-element tuple containing the feedback for each letter.

    Raises:
        ValueError: If either word does not contain exactly five letters.
    """
    target = target.upper()
    guess = guess.upper()

    if len(target) != 5:
        raise ValueError("Target must contain exactly five letters.")

    if len(guess) != 5:
        raise ValueError("Guess must contain exactly five letters.")

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
