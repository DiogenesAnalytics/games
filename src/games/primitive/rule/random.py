"""Module defining rules for random decision-making."""

import random

from games.primitive.rule.base import Rule
from games.primitive.state.base import State
from games.primitive.state.discrete import ChoiceState


class RandomChoiceRule(Rule):
    """A rule that randomly selects a valid choice from the state's options."""

    def apply(self, state: State) -> None:
        """Apply the rule to a given state by randomly choosing a valid option."""
        if not self.supports_state(state):
            raise ValueError("This rule cannot be applied to the given state.")

        new_value = random.choice(list(state.available_values))
        state.value = new_value

    def supports_state(self, state: State) -> bool:
        """Check if the rule is compatible with the given state."""
        return isinstance(state, ChoiceState)
