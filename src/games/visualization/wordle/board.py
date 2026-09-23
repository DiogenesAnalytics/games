"""Defines the Wordle board visualization."""

from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Tuple

from games.catalog.simulation.wordle.feedback import Feedback
from games.catalog.simulation.wordle.feedback import FeedbackTile


class WordleCell(NamedTuple):
    """Represent a cell on a Wordle board."""

    letter: Optional[str]
    feedback: Optional[FeedbackTile]


WordleRow = Tuple[WordleCell, ...]


class WordleBoard(NamedTuple):
    """Represent a Wordle board."""

    rows: Tuple[WordleRow, ...]


def create_wordle_board(
    guesses: Sequence[str],
    feedback: Sequence[Feedback],
    rows: int = 6,
) -> WordleBoard:
    """Create a Wordle board from guesses and feedback."""
    board_rows = [
        tuple(
            WordleCell(letter, tile)
            for letter, tile in zip(
                guess,
                result,
                strict=True,
            )
        )
        for guess, result in zip(
            guesses,
            feedback,
            strict=True,
        )
    ]

    while len(board_rows) < rows:
        board_rows.append(tuple(WordleCell(None, None) for _ in range(5)))

    return WordleBoard(tuple(board_rows[:rows]))
