"""Defines the classes responsible for managing state(s) access."""

from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from games.primitive.state.base import State
from games.primitive.state.mapping import StateDiff
from games.primitive.state.mapping import View


class StateManager:
    """Manages access to all simulation states."""

    def __init__(
        self,
        states: Optional[Dict[str, State]] = None,
        access_control: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Initialize with states and optional actor access control."""
        self._states: Dict[str, State] = states or {}
        self._access_control: Dict[str, List[str]] = access_control or {}

    def add_state(self, *state_pairs: Tuple[str, State]) -> None:
        """Add one or more state objects to the manager."""
        for state_id, state in state_pairs:
            self._states[state_id] = state

    def add_access(self, *access_pairs: Tuple[str, List[str]]) -> None:
        """Grant one or more actors access to specific state IDs."""
        for actor_id, state_ids in access_pairs:
            self._access_control[actor_id] = state_ids

    def get_view(self, actor_id: str) -> View:
        """Return a read-only View limited to an actor's accessible states."""
        state_ids = self._access_control.get(actor_id, [])
        state_data = {
            sid: self._states[sid].get_value()
            for sid in state_ids
            if sid in self._states
        }
        return View(state_data)

    def get_full_view(self) -> View:
        """Return a full read-only View of all states."""
        state_data = {sid: state.get_value() for sid, state in self._states.items()}
        return View(state_data)

    def apply_diff(self, diff: StateDiff) -> None:
        """Apply a StateDiff to the underlying states after validation."""
        for state_id, new_value in diff.items():
            if state_id not in self._states:
                raise KeyError(f"Unknown state ID: {state_id}")
            self._states[state_id].update(new_value)
