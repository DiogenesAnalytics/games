"""Tests for module games.catalog.simulation.base."""

import inspect

import pytest

from games.catalog.simulation.base import Simulation
from games.primitive.action.base import Action
from games.primitive.actor.base import Actor
from games.primitive.rule.base import Rule
from games.primitive.state.base import State


class DummySimulation(Simulation):
    """Concrete implementation of Simulation for testing."""

    def __init__(self, actor: Actor, state: State, rules: list[Rule]) -> None:
        """Initialize the DummySimulation with one actor, one state, and rules."""
        self._custom_actor = actor
        self._custom_state = state
        self._custom_rules = rules
        super().__init__()

    def _register_components(self) -> None:
        """Register a single actor, a single state, and provided rules."""
        self.actors.append(self._custom_actor)
        self.states["dummy_state"] = self._custom_state
        self.rules.extend(self._custom_rules)

    def is_done(self) -> bool:
        """Always return True to prevent continued simulation."""
        return True


@pytest.mark.abc
@pytest.mark.simulation
def test_simulation_abc_is_abstract() -> None:
    """Simulation should be abstract."""
    assert inspect.isabstract(Simulation)


@pytest.mark.simulation
def test_simulation_step_resolves_action(
    dummy_actor: Actor, mock_state: State, accepting_rule: Rule, mock_action: Action
) -> None:
    """Test that a step runs correctly when the rule resolves the action."""
    sim = DummySimulation(
        actor=dummy_actor,
        state=mock_state,
        rules=[accepting_rule],
    )

    sim.step()  # should succeed with no error

    # assert the action was resolved and applied
    assert mock_action.is_resolved, "Action should be resolved"
    assert mock_action.executor is not None, "Executor should be set on action"


@pytest.mark.simulation
def test_simulation_step_raises_on_unresolved_action(
    dummy_actor: Actor,
    mock_state: State,
    rejecting_rule: Rule,
) -> None:
    """Test that a RuntimeError is raised when no rule resolves the action."""
    sim = DummySimulation(
        actor=dummy_actor,
        state=mock_state,
        rules=[rejecting_rule],  # Will reject everything
    )

    with pytest.raises(RuntimeError, match="No rule could resolve action"):
        sim.step()
