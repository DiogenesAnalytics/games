"""Define the state-space explorer."""

from typing import Callable
from typing import FrozenSet
from typing import Set


def reachable_states(
    initial_state: FrozenSet[str],
    actions: Set[str],
    successors: Callable[
        [FrozenSet[str], str],
        Set[FrozenSet[str]],
    ],
) -> Set[FrozenSet[str]]:
    """Return all states reachable from an initial state."""
    states: Set[FrozenSet[str]] = {initial_state}
    pending: Set[FrozenSet[str]] = {initial_state}

    while pending:
        state = pending.pop()

        for action in actions:
            for successor in successors(state, action):
                if successor not in states:
                    states.add(successor)
                    pending.add(successor)

    return states
