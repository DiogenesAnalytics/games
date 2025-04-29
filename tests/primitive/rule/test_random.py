"""Test suite for 'games.primitive.rule.random' module."""

import pytest

from games.primitive.rule.random import RandomChoiceRule
from games.primitive.state.discrete import ChoiceState


@pytest.mark.rule
def test_random_choice_applies_value() -> None:
    """Test RandomChoiceRule assigns a valid value from available choices."""
    state = ChoiceState(choices={10, 20, 30})
    rule = RandomChoiceRule()
    rule.apply(state)
    assert state.value in state.available_values
