"""Test the state-space explorer."""

from typing import FrozenSet
from typing import Set

import pytest

from games.analysis.state_space.explorer import reachable_states


def successors(
    state: FrozenSet[str],
    action: str,
) -> Set[FrozenSet[str]]:
    """Return successors for a simple test state space."""
    if state == frozenset({"A"}) and action == "guess":
        return {
            frozenset({"B"}),
            frozenset({"C"}),
        }

    return set()


@pytest.mark.analysis
def test_reachable_states() -> None:
    """Test that reachable states are returned."""
    initial_state = frozenset({"A"})

    result = reachable_states(
        initial_state,
        {"guess"},
        successors,
    )

    assert result == {
        frozenset({"A"}),
        frozenset({"B"}),
        frozenset({"C"}),
    }


@pytest.mark.analysis
def test_reachable_states_includes_initial_state() -> None:
    """Test that the initial state is included."""
    initial_state = frozenset({"A"})

    result = reachable_states(
        initial_state,
        set(),
        successors,
    )

    assert result == {initial_state}


@pytest.mark.analysis
def test_reachable_states_handles_cycles() -> None:
    """Test that cycles do not cause repeated exploration."""
    initial_state = frozenset({"A"})

    def cyclic_successors(
        state: FrozenSet[str],
        action: str,
    ) -> Set[FrozenSet[str]]:
        """Return a successor that cycles back to the initial state."""
        if state == frozenset({"A"}) and action == "guess":
            return {frozenset({"B"})}

        if state == frozenset({"B"}) and action == "guess":
            return {frozenset({"A"})}

        return set()

    result = reachable_states(
        initial_state,
        {"guess"},
        cyclic_successors,
    )

    assert result == {
        frozenset({"A"}),
        frozenset({"B"}),
    }
