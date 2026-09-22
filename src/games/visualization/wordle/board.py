"""Defines the Wordle board visualization."""

from typing import NamedTuple
from typing import Optional
from typing import Tuple

from games.catalog.simulation.wordle.feedback import FeedbackTile


class WordleCell(NamedTuple):
    """Represent a cell on a Wordle board."""

    letter: Optional[str]
    feedback: Optional[FeedbackTile]


WordleRow = Tuple[WordleCell, ...]


class WordleBoard(NamedTuple):
    """Represent a Wordle board."""

    rows: Tuple[WordleRow, ...]
