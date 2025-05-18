"""Base module for defining the abstract base class (ABC) for game actors."""

from abc import ABC
from abc import abstractmethod
from typing import Type

from games.primitive.action.base import Action
from games.primitive.state.mapping import View


class Actor(ABC):
    """Abstract base class for all entities capable of generating actions."""

    def __init__(self, actor_id: str) -> None:
        """Initialize the actor with a unique identifier."""
        self.id = actor_id

    @abstractmethod
    def decide(self, view: View) -> Action:
        """Decide on an action to take based on the current state view."""
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

    def __init__(self, actor_id: str, action_type: Type[Action]) -> None:
        """Initialize with an ID and a fixed action type."""
        super().__init__(actor_id)
        self.action_type = action_type

    def decide(self, view: View) -> Action:
        """Always instantiate and return the same action type."""
        # Use the view to make a decision
        return self.action_type()
