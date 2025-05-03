"""Test suite for 'games.primitive.rule.random' module."""

import pytest

from games.primitive.action.random import RandomChoiceAction
from games.primitive.rule.random import RandomChoiceRule
from games.primitive.state.discrete import ChoiceState


@pytest.mark.rule
def test_random_choice_applies_value() -> None:
    """Test RandomChoiceRule assigns a valid value from available choices."""
    state = ChoiceState(choices={10, 20, 30})
    action = RandomChoiceAction()
    rule = RandomChoiceRule()

    # Ensure rule accepts the action and state
    assert rule.accepts(action, state)

    # Apply the rule to set executor and mark as valid
    rule.apply(action, state)
    assert action.is_valid
    assert action.executor is not None

    # Execute the action's effect on the state
    action.apply(state)
    assert state.value in state.available_values
