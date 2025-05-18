"""Module defining rules for random decision-making."""

import random
from typing import Callable

from games.primitive.action.base import Action
from games.primitive.action.random import RandomChoiceAction
from games.primitive.rule.base import Rule
from games.primitive.state.base import State
from games.primitive.state.discrete import ChoiceState


class RandomChoiceRule(Rule):
    """A rule that randomly selects a valid choice from the state's options."""

    def accepts(self, action: Action, state: State) -> bool:
        """Check if the rule can handle this action and state."""
        return isinstance(action, RandomChoiceAction) and isinstance(state, ChoiceState)

    def bind_executor(self, action: Action, state: State) -> Callable[[State], None]:
        """Return an executor that randomly chooses from state's values."""

        def executor(state: State) -> None:
            """Executor for randomly choosing from available state values."""
            state.value = random.choice(list(state.available_values))

        return executor
