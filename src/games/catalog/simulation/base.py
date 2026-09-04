"""This module defines the abstract base class for simulations."""

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple
from uuid import UUID

from games.primitive.actor.base import Actor
from games.primitive.rule.base import Rule
from games.primitive.state.base import State


class Simulation(ABC):
    """Abstract Base Class for simulations that evolve over time."""

    def __init__(self) -> None:
        """Initialize the simulation by preparing internal components."""
        self._states: List[State] = []
        self._rules: List[Rule] = []
        self._actors: List[Actor] = []
        self._permissions: Dict[Actor, Set[UUID]] = {}

    @property
    def states(self) -> Tuple[State, ...]:
        """Return the states registered with the simulation."""
        return tuple(self._states)

    @property
    def rules(self) -> Tuple[Rule, ...]:
        """Return the rules registered with the simulation."""
        return tuple(self._rules)

    @property
    def actors(self) -> Tuple[Actor, ...]:
        """Return the actors registered with the simulation."""
        return tuple(self._actors)

    def _register_state(self, state: State) -> None:
        """Register a state with the simulation.

        Args:
            state: State to register.
        """
        self._states.append(state)

    def _register_rule(self, rule: Rule) -> None:
        """Register a rule with the simulation.

        Args:
            rule: Rule to register.
        """
        self._rules.append(rule)

    def _register_actor(self, actor: Actor) -> None:
        """Register an actor with the simulation.

        Args:
            actor: Actor to register.
        """
        self._actors.append(actor)

    def authorize(self, actor: Actor, state: State) -> None:
        """Authorize an actor to interact with a state.

        Args:
            actor: Actor that should be granted access.
            state: State the actor may interact with.
        """
        self._permissions.setdefault(actor, set()).add(state.id)

    def is_authorized(self, actor: Actor, state: State) -> bool:
        """Return whether an actor may interact with a state.

        Args:
            actor: Actor whose authorization should be checked.
            state: State the actor wants to interact with.

        Returns:
            ``True`` if the actor is authorized for the state.
        """
        return state.id in self._permissions.get(actor, set())

    def _run_cycle(self) -> None:
        """Run one actor–action–rule–state resolution cycle."""
        for actor in self._actors:
            for state in self._states:
                if not self.is_authorized(actor, state):
                    continue

                action = actor.decide(state)

                for rule in self._rules:
                    if rule.accepts(action, state):
                        rule.apply(action, state)
                        break

                if action.is_resolved:
                    action.apply(state)
                else:
                    raise RuntimeError(f"No rule could resolve action: {action}")

    def step(self) -> None:
        """Advance the simulation by one step."""
        self._run_cycle()

    @abstractmethod
    def is_done(self) -> bool:
        """Check whether the simulation has reached a stopping condition."""
        pass
