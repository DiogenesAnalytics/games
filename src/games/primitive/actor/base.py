"""Base module for defining the abstract base class (ABC) for game actors."""

from abc import ABC
from abc import abstractmethod
from typing import Type

from games.primitive.action.base import Action
from games.primitive.state.base import State


class Actor(ABC):
    """Abstract base class for all entities capable of generating actions."""

    @abstractmethod
    def decide(self, state: State) -> Action:
        """Decide on an action to take based on the current state."""
        pass


class Player(Actor, ABC):
    """Abstract base class for a human or agent player in a game."""

    # this might collect input, interface with UI, or be a trained agent.
    pass


class NonPlayer(Actor, ABC):
    """Abstract base class for an automated or environmental actor in a game."""

    # intended for systems like randomness, environment, or automated agents.
    pass


class SimpleNonPlayer(NonPlayer):
    """A non-player actor that always returns the same action."""

    def __init__(self, action_type: Type[Action]) -> None:
        """Initialize with a single action type to always use."""
        self.action_type = action_type

    def decide(self, state: State) -> Action:
        """Always instantiate and return the same action type."""
        return self.action_type()
