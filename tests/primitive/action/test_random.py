"""Tests for module games.primitive.action.random."""

import pytest

from games.primitive.action.random import RandomChoiceAction


@pytest.mark.action
def test_random_choice_action_describe() -> None:
    """Test describe() method of RandomChoiceAction."""
    action = RandomChoiceAction()
    assert isinstance(action.describe(), str)
    assert "Randomly select" in action.describe()
