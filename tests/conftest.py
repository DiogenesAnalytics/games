"""Configuration file for pytest."""

from typing import Any
from typing import Callable
from typing import Set

import pytest

from games.primitive.action.base import Action
from games.primitive.actor.base import Actor
from games.primitive.rule.base import Rule
from games.primitive.state.base import State


def pytest_configure(config: pytest.Config) -> None:
    """For configuring pytest with custom markers."""
    config.addinivalue_line("markers", "debug: debugging tests.")
    config.addinivalue_line("markers", "fixture: fixture tests.")
    config.addinivalue_line("markers", "abc: tests for abstract base classes")
    config.addinivalue_line("markers", "simulation: simulation tests")
    config.addinivalue_line("markers", "action: action tests")
    config.addinivalue_line("markers", "state: state tests")
    config.addinivalue_line("markers", "actor: actor tests")
    config.addinivalue_line("markers", "rule: rule tests")


class MockAction(Action):
    """Subclass for testing Action ABC."""

    def describe(self) -> str:
        """Mock a description for the action."""
        return "Mock action for testing"


class DummyState(State):
    """State subclass for testing."""

    def __init__(self) -> None:
        """Initialize the dummy state with a default None value."""
        self._value = None

    def reset(self) -> None:
        """Mock reset method that does nothing."""
        pass

    def is_valid(self) -> bool:
        """Always return True to indicate the state is valid."""
        return True

    def update(self, value: Any) -> None:
        """Set the internal value to the provided input."""
        self._value = value

    @property
    def available_values(self) -> Set[Any]:
        """Return an empty set."""
        return set()


class DummyActor(Actor):
    """A simple actor that always returns the same predefined action."""

    def __init__(self, action: Action):
        """Initialize the dummy actor."""
        self._action = action

    def decide(self, state: State) -> Action:
        """Return the predefined action regardless of state."""
        return self._action


class AcceptingRule(Rule):
    """A rule that accepts any action-state pair and resolves the action."""

    def accepts(self, action: Action, state: State) -> bool:
        """Always return True to indicate the rule accepts the action/state."""
        return True

    def apply(self, action: Action, state: State) -> None:
        """Resolve the action with a no-op executor."""
        action.executor = lambda s: None
        action.validate()


class RejectingRule(Rule):
    """A rule that rejects all action-state pairs."""

    def accepts(self, action: Action, state: State) -> bool:
        """Always return False to indicate the rule rejects the input."""
        return False

    def apply(self, action: Action, state: State) -> None:
        """Perform no operation. Included for completeness."""
        pass


@pytest.fixture
def mock_action() -> MockAction:
    """Return a mock Action subclass."""
    return MockAction()


@pytest.fixture
def dummy_executor() -> Callable[[State], None]:
    """Return a simple dummy executor that does nothing."""

    def _executor(state: State) -> None:
        """Dummy executor function for testing purposes."""
        pass

    return _executor


@pytest.fixture
def mock_state() -> State:
    """Return a dummy State instance for tests that require one."""
    return DummyState()


@pytest.fixture
def dummy_actor(mock_action: Action) -> DummyActor:
    """Fixture that returns a DummyActor using the mock_action fixture."""
    return DummyActor(mock_action)


@pytest.fixture
def accepting_rule() -> AcceptingRule:
    """Fixture that returns an AcceptingRule instance."""
    return AcceptingRule()


@pytest.fixture
def rejecting_rule() -> RejectingRule:
    """Fixture that returns a RejectingRule instance."""
    return RejectingRule()
