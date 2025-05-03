"""Defines actors that make randomized decisions."""

import random
from typing import List
from typing import Type

from games.primitive.action.base import Action
from games.primitive.actor.base import Actor
from games.primitive.state.base import State


class RandomActor(Actor):
    """An actor that randomly selects an available action."""

    def __init__(self, possible_actions: List[Type[Action]]) -> None:
        """Initialize with a list of possible actions."""
        if not possible_actions:
            raise ValueError("RandomActor requires at least one possible Action.")
        self.possible_actions = possible_actions

    def decide(self, state: State) -> Action:
        """Randomly instantiate and return one of the possible action types."""
        action_cls = random.choice(self.possible_actions)
        return action_cls()
