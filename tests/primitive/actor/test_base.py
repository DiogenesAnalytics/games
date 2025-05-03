"""Tests for module games.primitive.actor.base."""

import inspect

import pytest

from games.primitive.action.base import Action
from games.primitive.actor.base import Actor
from games.primitive.actor.base import NonPlayer
from games.primitive.actor.base import Player
from games.primitive.actor.base import SimpleNonPlayer
from games.primitive.state.base import State


@pytest.mark.abc
@pytest.mark.actor
def test_actor_abc_is_abstract() -> None:
    """Simulation should be abstract."""
    assert inspect.isabstract(Actor)


@pytest.mark.actor
def test_actor_inheritance() -> None:
    """Test they are Actor subclasses."""
    assert issubclass(Player, Actor)
    assert issubclass(NonPlayer, Actor)


@pytest.mark.actor
def test_simple_nonplayer_returns_action(
    mock_action: Action, mock_state: State
) -> None:
    """Test that SimpleNonPlayer always returns the correct Action type."""
    actor = SimpleNonPlayer(action_type=type(mock_action))
    action = actor.decide(mock_state)
    assert isinstance(action, type(mock_action))
    assert "Mock action" in action.describe()
