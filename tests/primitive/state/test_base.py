"""Tests for module games.primitive.state.base."""

import inspect

import pytest

from games.primitive.state.base import State


@pytest.mark.abc
@pytest.mark.state
def test_state_abc_is_abstract() -> None:
    """State should be abstract."""
    assert inspect.isabstract(State)
