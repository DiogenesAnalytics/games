"""This module defines the abstract base class for simulations."""

from abc import ABC
from abc import abstractmethod

from games.primitive.rule.base import Rule
from games.primitive.state.base import State


class Simulation(ABC):
    """Abstract Base Class for simulations that can run steps and have a state."""

    @abstractmethod
    def __init__(self, state: State, rule: Rule) -> None:
        """Initialize the simulation with a state and a rule."""
        self.state = state
        self.rule = rule

    @abstractmethod
    def step(self) -> None:
        """Run a single step of the simulation."""
        pass

    @abstractmethod
    def is_done(self) -> bool:
        """Check if the simulation is done or ongoing."""
        pass
