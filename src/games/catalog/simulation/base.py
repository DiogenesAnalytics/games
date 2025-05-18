"""This module defines the abstract base class for simulations."""

from abc import ABC
from abc import abstractmethod
from typing import List

from games.primitive.actor.base import Actor
from games.primitive.rule.base import Rule
from games.primitive.state.manager import StateManager


class Simulation(ABC):
    """Abstract Base Class for simulations that evolve over time."""

    def __init__(self) -> None:
        """Initialize the simulation with a state manager, actors, and rules."""
        self.state_manager = StateManager()
        self.actors: List[Actor] = []
        self.rules: List[Rule] = []
        self._register_components()

    @abstractmethod
    def _register_components(self) -> None:
        """Set up states, rules, actors, and access control."""
        pass

    def _run_cycle(self) -> None:
        """Run one full actor–view–action–rule–state cycle."""
        for actor in self.actors:
            view = self.state_manager.get_view(actor.id)
            action = actor.decide(view)

            # apply rules
            for rule in self.rules:
                rule.process(action)
                if not action.is_valid:
                    break

            # update state
            if action.is_valid:
                self.state_manager.apply_diff(action.diff)
            else:
                raise RuntimeError(f"Invalid action from actor {actor.id}: {action}")

    def step(self) -> None:
        """Advance the simulation by one step."""
        self._run_cycle()

    @abstractmethod
    def is_done(self) -> bool:
        """Check whether the simulation has reached a stopping condition."""
        pass
