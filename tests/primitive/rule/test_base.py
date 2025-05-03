"""Tests for module games.primitive.rule.base."""

import inspect
from typing import Callable
from typing import List

import pytest

from games.primitive.action.base import Action
from games.primitive.rule.base import CompoundRule
from games.primitive.rule.base import ExecutorRule
from games.primitive.rule.base import Rule
from games.primitive.rule.base import ValidationRule
from games.primitive.state.base import State


@pytest.mark.abc
@pytest.mark.rule
def test_rule_abc_is_abstract() -> None:
    """Rule should be abstract."""
    assert inspect.isabstract(Rule)


@pytest.mark.rule
def test_validation_rule_invalidates_action(
    mock_action: Action, mock_state: State
) -> None:
    """Test should invalidate action when validate() returns False."""

    class MyValidationRule(ValidationRule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def validate(self, action: Action, state: State) -> bool:
            return False

    rule = MyValidationRule()
    rule.apply(mock_action, mock_state)
    assert not mock_action.is_valid


@pytest.mark.rule
def test_validation_rule_keeps_action_valid(
    mock_action: Action, mock_state: State
) -> None:
    """Test should leave action valid when validate() returns True."""

    class MyValidationRule(ValidationRule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def validate(self, action: Action, state: State) -> bool:
            return True

    rule = MyValidationRule()
    rule.apply(mock_action, mock_state)
    assert mock_action.is_valid


@pytest.mark.rule
def test_executor_rule_sets_executor_and_validates(
    mock_action: Action, mock_state: State, dummy_executor: Callable[[State], None]
) -> None:
    """Test should bind executor and mark action as valid."""

    class MyExecutorRule(ExecutorRule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def bind_executor(
            self, action: Action, state: State
        ) -> Callable[[State], None]:
            return dummy_executor

    rule = MyExecutorRule()
    rule.apply(mock_action, mock_state)
    assert mock_action.executor == dummy_executor
    assert mock_action.is_valid


@pytest.mark.rule
def test_compound_rule_applies_all_rules(
    mock_action: Action, mock_state: State
) -> None:
    """Test apply multiple rules in order."""

    class Rule1(Rule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def apply(self, action: Action, state: State) -> None:
            action.value = "R1"  # type: ignore
            action.validate()

    class Rule2(Rule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def apply(self, action: Action, state: State) -> None:
            action.value = "R2"  # type: ignore
            action.validate()

    class MyCompoundRule(CompoundRule):
        @property
        def _rules(self) -> List[Rule]:
            return [Rule1(), Rule2()]

    rule = MyCompoundRule()
    rule.apply(mock_action, mock_state)
    assert getattr(mock_action, "value", None) == "R2"


@pytest.mark.rule
def test_compound_rule_stops_on_invalidation(
    mock_action: Action, mock_state: State
) -> None:
    """Test stop applying further rules after invalidation."""

    class Rule1(Rule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def apply(self, action: Action, state: State) -> None:
            action.invalidate()

    class Rule2(Rule):
        def accepts(self, action: Action, state: State) -> bool:
            return True

        def apply(self, action: Action, state: State) -> None:
            action.validate()

    class MyCompoundRule(CompoundRule):
        @property
        def _rules(self) -> List[Rule]:
            return [Rule1(), Rule2()]

    rule = MyCompoundRule()
    rule.apply(mock_action, mock_state)
    assert not mock_action.is_valid
    assert getattr(mock_action, "value", None) is None
