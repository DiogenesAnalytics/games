"""Tests for module games.primitive.action.base."""

import inspect
from typing import Callable

import pytest

from games.primitive.action.base import Action
from games.primitive.state.base import State


@pytest.mark.abc
@pytest.mark.action
def test_action_abc_is_abstract() -> None:
    """Simulation should be abstract."""
    assert inspect.isabstract(Action)


@pytest.mark.action
def test_initial_state(mock_action: Action) -> None:
    """Test that a new action is neither valid nor resolved."""
    assert not mock_action.is_valid
    assert not mock_action.is_resolved
    assert mock_action.executor is None


@pytest.mark.action
def test_validate_and_invalidate(mock_action: Action) -> None:
    """Test validate() and invalidate() logic on action state."""
    mock_action.validate()
    assert mock_action.is_valid

    mock_action.invalidate()
    assert not mock_action.is_valid
    assert mock_action.executor is None  # type: ignore[unreachable]

    # once invalidated, validate() should no longer work
    mock_action.validate()
    assert not mock_action.is_valid


@pytest.mark.action
def test_executor_binding_and_resolution(
    mock_action: Action, dummy_executor: Callable[[State], None]
) -> None:
    """Test binding an executor and resolving an action."""
    mock_action.executor = dummy_executor
    assert mock_action.executor is dummy_executor
    assert not mock_action.is_resolved

    mock_action.validate()
    assert mock_action.is_resolved
    assert mock_action.apply is dummy_executor  # type: ignore[unreachable]


@pytest.mark.action
def test_apply_without_resolution_raises(mock_action: Action) -> None:
    """Test that apply raises NotImplementedError if unresolved."""
    with pytest.raises(NotImplementedError):
        _ = mock_action.apply


@pytest.mark.action
def test_non_callable_executor_raises(mock_action: Action) -> None:
    """Test that setting a non-callable executor raises TypeError."""
    with pytest.raises(TypeError):
        mock_action.executor = "not a function"  # type: ignore


@pytest.mark.action
def test_repr_output(mock_action: Action) -> None:
    """Test __repr__ output format includes valid and description."""
    output = repr(mock_action)
    assert "<MockAction:" in output
    assert "valid=False" in output
    assert (
        "Mock action for testing" in output
        or "desc='Mock action for testing'" in output
    )
