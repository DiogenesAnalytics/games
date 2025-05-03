"""Tests for module games.primitive.actor.random."""

import pytest

from games.primitive.action.base import Action
from games.primitive.actor.random import RandomActor
from games.primitive.state.base import State


@pytest.mark.actor
def test_random_actor_raises_with_no_actions() -> None:
    """Test that RandomActor raises a ValueError when initialized."""
    with pytest.raises(ValueError):
        RandomActor([])


@pytest.mark.actor
def test_random_actor_returns_action_instance(
    mock_action: Action, mock_state: State
) -> None:
    """Test that RandomActor's decide method correctly returns an Action."""
    # provide the type, not instance
    actor = RandomActor([type(mock_action)])
    action = actor.decide(mock_state)

    # ensure that the returned action is of the correct type
    assert isinstance(action, Action)
    assert isinstance(action, type(mock_action))
