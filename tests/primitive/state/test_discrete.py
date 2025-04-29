"""Test suite for 'games.primitive.state.discrete' module."""

import pytest

from games.primitive.state.discrete import ChoiceState


@pytest.mark.state
def test_initial_value_none() -> None:
    """Test that the initial value of a ChoiceState is None."""
    state = ChoiceState(choices={"A", "B", "C"})
    assert state.value is None


@pytest.mark.state
def test_valid_update() -> None:
    """Test that a valid value can be assigned and validated."""
    state = ChoiceState(choices={1, 2, 3})
    state.value = 2
    assert state.value == 2
    assert state.is_valid()


@pytest.mark.state
def test_invalid_update_raises() -> None:
    """Test that assigning an invalid value raises a ValueError."""
    state = ChoiceState(choices={"yes", "no"})
    with pytest.raises(ValueError):
        state.value = "maybe"


@pytest.mark.state
def test_reset_sets_value_to_none() -> None:
    """Test that calling reset sets the state's value back to None."""
    state = ChoiceState(choices={1, 2})
    state.value = 2
    state.reset()
    assert state.value is None


@pytest.mark.state
def test_choices_property_matches_input() -> None:
    """Test that the choices property returns the original set of choices."""
    choices = {"red", "green", "blue"}
    state = ChoiceState(choices=choices)
    assert state.available_values == choices


@pytest.mark.state
def test_empty_choices_raises() -> None:
    """Test ChoiceState raises ValueError when no choices available."""
    with pytest.raises(ValueError):
        ChoiceState(choices=set())
