"""Tests for module games.catalog.simulation.wordle.rule."""

from typing import Set

import pytest

from games.catalog.simulation.wordle.action import WordleGuess
from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.rule import WordleGuessExecutorRule
from games.catalog.simulation.wordle.rule import WordleGuessValidationRule
from games.catalog.simulation.wordle.rule import WordleRule
from games.catalog.simulation.wordle.state import WordleState
from games.primitive.action.base import Action
from games.primitive.state.base import State


class ConcreteAction(Action):
    """Concrete action for testing rule type rejection."""

    def describe(self) -> str:
        """Return a description of the test action."""
        return "test action"


class ConcreteState(State):
    """Concrete state for testing rule type rejection."""

    def __init__(self) -> None:
        """Initialize the test state."""
        super().__init__()

    def reset(self) -> None:
        """Reset the test state."""
        pass

    def is_valid(self) -> bool:
        """Return whether the test state is valid."""
        return True

    def update(self, value: object) -> None:
        """Update the test state."""
        pass

    @property
    def available_values(self) -> Set[object]:
        """Return the available test values."""
        return set()


@pytest.fixture
def state(
    solutions: Set[str],
    available_guesses: Set[str],
) -> WordleState:
    """Return a Wordle state for testing."""
    return WordleState(
        solutions=solutions,
        available_guesses=available_guesses,
        target="CRANE",
    )


@pytest.mark.wordle
def test_validation_rule_accepts_wordle_action_and_state(
    state: WordleState,
) -> None:
    """The validation rule should accept Wordle actions and states."""
    rule = WordleGuessValidationRule()

    assert rule.accepts(WordleGuess("PLANE"), state)


@pytest.mark.wordle
def test_validation_rule_rejects_wrong_types(
    state: WordleState,
) -> None:
    """The validation rule should reject incompatible action or state types."""
    rule = WordleGuessValidationRule()

    assert not rule.accepts(ConcreteAction(), state)
    assert not rule.accepts(
        WordleGuess("PLANE"),
        ConcreteState(),
    )


@pytest.mark.wordle
def test_validation_rule_accepts_available_guess(
    state: WordleState,
) -> None:
    """The validation rule should accept any legal Wordle guess."""
    rule = WordleGuessValidationRule()

    assert rule.validate(WordleGuess("SLATE"), state)


@pytest.mark.wordle
def test_validation_rule_rejects_unavailable_guess(
    state: WordleState,
) -> None:
    """The validation rule should reject guesses outside the dictionary."""
    rule = WordleGuessValidationRule()

    assert not rule.validate(WordleGuess("XXXXX"), state)


@pytest.mark.wordle
def test_validation_rule_rejects_wrong_types_in_validate(
    state: WordleState,
) -> None:
    """Validation should raise TypeError for incompatible types."""
    rule = WordleGuessValidationRule()

    with pytest.raises(
        TypeError,
        match="Expected WordleGuess and WordleState",
    ):
        rule.validate(ConcreteAction(), state)


@pytest.mark.wordle
def test_executor_rule_accepts_wordle_action_and_state(
    state: WordleState,
) -> None:
    """The executor rule should accept Wordle actions and states."""
    rule = WordleGuessExecutorRule()

    assert rule.accepts(WordleGuess("PLANE"), state)


@pytest.mark.wordle
def test_executor_rule_rejects_wrong_types(
    state: WordleState,
) -> None:
    """The executor rule should reject incompatible action or state types."""
    rule = WordleGuessExecutorRule()

    assert not rule.accepts(ConcreteAction(), state)
    assert not rule.accepts(
        WordleGuess("PLANE"),
        ConcreteState(),
    )


@pytest.mark.wordle
def test_executor_rule_rejects_wrong_types_in_bind_executor(
    state: WordleState,
) -> None:
    """Binding should raise TypeError for incompatible types."""
    rule = WordleGuessExecutorRule()

    with pytest.raises(
        TypeError,
        match="Expected WordleGuess and WordleState",
    ):
        rule.bind_executor(ConcreteAction(), state)


@pytest.mark.wordle
def test_executor_applies_guess(
    state: WordleState,
) -> None:
    """The bound executor should update the state with feedback."""
    rule = WordleGuessExecutorRule()
    action = WordleGuess("PLANE")

    executor = rule.bind_executor(action, state)
    executor(state)

    assert state.guesses == ["PLANE"]
    assert state.feedback == [
        (
            FeedbackTile.GRAY,
            FeedbackTile.GRAY,
            FeedbackTile.GREEN,
            FeedbackTile.GREEN,
            FeedbackTile.GREEN,
        )
    ]


@pytest.mark.wordle
def test_executor_rejects_non_wordle_state(
    state: WordleState,
) -> None:
    """The bound executor should reject a non-Wordle state."""
    rule = WordleGuessExecutorRule()
    action = WordleGuess("PLANE")

    executor = rule.bind_executor(action, state)

    with pytest.raises(TypeError, match="Expected WordleState"):
        executor(ConcreteState())


@pytest.mark.wordle
def test_wordle_rule_contains_validation_and_executor_rules() -> None:
    """The compound Wordle rule should contain both component rules."""
    rule = WordleRule()

    assert len(rule._rules) == 2
    assert isinstance(rule._rules[0], WordleGuessValidationRule)
    assert isinstance(rule._rules[1], WordleGuessExecutorRule)


@pytest.mark.wordle
def test_wordle_rule_accepts_wordle_action_and_state(
    state: WordleState,
) -> None:
    """The compound rule should accept Wordle actions and states."""
    rule = WordleRule()

    assert rule.accepts(WordleGuess("PLANE"), state)
