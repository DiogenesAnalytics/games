"""Base module for defining the abstract base class (ABC) for game rules."""

from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import List

from games.primitive.action.base import Action
from games.primitive.state.base import State


class Rule(ABC):
    """Abstract base class for rules that resolve actions."""

    @abstractmethod
    def accepts(self, action: Action, state: State) -> bool:
        """Check whether this rule can handle the given action and states."""
        pass

    @abstractmethod
    def apply(self, action: Action, state: State) -> None:
        """Apply rule to action, by validating it and/or binding an executor."""
        pass


class ValidationRule(Rule, ABC):
    """Abstract base class for rules that only validate an action."""

    @abstractmethod
    def validate(self, action: Action, state: State) -> bool:
        """Return True if the action is valid, False otherwise."""
        pass

    def apply(self, action: Action, state: State) -> None:
        """Apply the validation rule to the given action."""
        if self.validate(action, state):
            action.validate()
        else:
            action.invalidate()


class ExecutorRule(Rule, ABC):
    """Abstract base class for rules that only assigns an executor to an action."""

    @abstractmethod
    def bind_executor(self, action: Action, state: State) -> Callable[[State], None]:
        """Return the executor function to apply to the action."""
        pass

    def apply(self, action: Action, state: State) -> None:
        """Apply the executor rule to the given action."""
        action.executor = self.bind_executor(action, state)
        action.validate()


class CompoundRule(Rule, ABC):
    """Abstract base class for rule that applies multiple rules to an action."""

    @property
    @abstractmethod
    def _rules(self) -> List[Rule]:
        """Return the list of rules that should be applied in sequence."""
        pass

    def accepts(self, action: Action, state: State) -> bool:
        """Check whether all rules accept action."""
        return all(rule.accepts(action, state) for rule in self._rules)

    def apply(self, action: Action, state: State) -> None:
        """Apply all the constituent rules to the action."""
        for rule in self._rules:
            rule.apply(action, state)
            if not action.is_valid:
                break
