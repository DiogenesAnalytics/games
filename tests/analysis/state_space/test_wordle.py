"""Test Wordle state-space analysis."""

from typing import Dict
from typing import FrozenSet
from typing import Set

import pytest

from games.analysis.state_space.wordle import successors
from games.analysis.state_space.wordle import wordle_successors
from games.catalog.simulation.wordle.feedback import Feedback


@pytest.mark.wordle
def test_successors_partition_candidates() -> None:
    """Test that successors partition the candidate set."""
    candidates = {"CRANE", "STAIN", "PLANE"}

    result: Dict[Feedback, Set[str]] = successors(candidates, "STAIN")

    assert set().union(*result.values()) == candidates


@pytest.mark.wordle
def test_successors_are_disjoint() -> None:
    """Test that successors are pairwise disjoint."""
    candidates = {"CRANE", "STAIN", "PLANE"}

    result: Dict[Feedback, Set[str]] = successors(candidates, "STAIN")
    successor_sets = list(result.values())

    for index, first in enumerate(successor_sets):
        for second in successor_sets[index + 1 :]:
            assert first.isdisjoint(second)


@pytest.mark.wordle
def test_wordle_successors_return_candidate_sets() -> None:
    """Test that Wordle successors return candidate sets."""
    candidates = frozenset({"CRANE", "STAIN", "PLANE"})

    result: Set[FrozenSet[str]] = wordle_successors(
        candidates,
        "STAIN",
    )

    assert set().union(*result) == set(candidates)


@pytest.mark.wordle
def test_wordle_successors_match_successors() -> None:
    """Test that Wordle successors contain the states from successors."""
    candidates = frozenset({"CRANE", "STAIN", "PLANE"})

    feedback_successors = successors(
        set(candidates),
        "STAIN",
    )
    state_successors = wordle_successors(
        candidates,
        "STAIN",
    )

    expected = {
        frozenset(candidate_set) for candidate_set in feedback_successors.values()
    }

    assert state_successors == expected


@pytest.mark.wordle
def test_wordle_successors_partition_candidates() -> None:
    """Test that Wordle successor states partition the candidates."""
    candidates = frozenset({"CRANE", "STAIN", "PLANE"})

    result = wordle_successors(candidates, "STAIN")

    assert set().union(*result) == set(candidates)


@pytest.mark.wordle
def test_wordle_successors_are_disjoint() -> None:
    """Test that Wordle successor states are disjoint."""
    candidates = frozenset({"CRANE", "STAIN", "PLANE"})

    result = wordle_successors(candidates, "STAIN")
    successor_sets = list(result)

    for index, first in enumerate(successor_sets):
        for second in successor_sets[index + 1 :]:
            assert first.isdisjoint(second)


@pytest.mark.wordle
def test_wordle_successors_are_frozen_sets() -> None:
    """Test that Wordle successor states are frozen sets."""
    candidates = frozenset({"CRANE", "STAIN", "PLANE"})

    result = wordle_successors(candidates, "STAIN")

    assert all(isinstance(state, frozenset) for state in result)
