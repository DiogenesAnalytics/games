"""Define state-space analysis for Wordle."""

from typing import Dict
from typing import FrozenSet
from typing import Set

from games.catalog.simulation.wordle.feedback import Feedback
from games.catalog.simulation.wordle.feedback import feedback


def successors(
    candidates: Set[str],
    guess: str,
) -> Dict[Feedback, Set[str]]:
    """Return possible successor candidate sets for a Wordle guess."""
    result: Dict[Feedback, Set[str]] = {}

    for candidate in candidates:
        result.setdefault(
            feedback(candidate, guess),
            set(),
        ).add(candidate)

    return result


def wordle_successors(
    candidates: FrozenSet[str],
    guess: str,
) -> Set[FrozenSet[str]]:
    """Return the candidate sets reachable from a Wordle guess."""
    return {
        frozenset(candidate_set)
        for candidate_set in successors(
            set(candidates),
            guess,
        ).values()
    }
