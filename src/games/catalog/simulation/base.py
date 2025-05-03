"""This module defines the abstract base class for simulations."""

from abc import ABC
from abc import abstractmethod
from typing import List

from games.primitive.actor.base import Actor
from games.primitive.rule.base import Rule
from games.primitive.state.base import State


class Simulation(ABC):
    """Abstract Base Class for simulations that evolve over time."""

    def __init__(self) -> None:
        """Initialize the simulation by preparing internal components."""
        self.states: List[State] = []
        self.rules: List[Rule] = []
        self.actors: List[Actor] = []
        self._register_components()

    @abstractmethod
    def _register_components(self) -> None:
        """Set up states, rules, and actors."""
        pass

    def _run_cycle(self) -> None:
        """Run one actor–action–rule–state resolution cycle."""
        # loop over actors
        for actor in self.actors:
            # loop over states
            for state in self.states:
                # get actor's decision
                action = actor.decide(state)

                # loop over all rules
                for rule in self.rules:
                    # check action against rules
                    if rule.accepts(action, state):
                        # update action with executor if necessary
                        rule.apply(action, state)
                        break

                if action.is_resolved:
                    action.apply(state)
                else:
                    raise RuntimeError(f"No rule could resolve action: {action}")

    def step(self) -> None:
        """Advance the simulation by one step using actor–action–rule–state logic."""
        self._run_cycle()

    @abstractmethod
    def is_done(self) -> bool:
        """Check whether the simulation has reached a stopping condition."""
        pass
