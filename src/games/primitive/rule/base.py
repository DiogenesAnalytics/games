"""Base module for defining the abstract base class (ABC) for game rules."""

from abc import ABC
from abc import abstractmethod
from typing import List

from games.primitive.action.base import Action


class Rule(ABC):
    """Base class for rules that validate and/or modify actions."""

    @abstractmethod
    def accepts(self, action: Action) -> bool:
        """Determine if this rule applies to the given action."""
        pass

    @abstractmethod
    def apply(self, action: Action) -> None:
        """Validate or modify the action in-place."""
        pass

    def process(self, action: Action) -> None:
        """Apply this rule to the given action if the rule accepts it."""
        if self.accepts(action):
            self.apply(action)


class CompoundRule(Rule, ABC):
    """Abstract base class for a rule that applies multiple rules to an action."""

    @property
    @abstractmethod
    def _rules(self) -> List[Rule]:
        """Return the list of rules that should be applied in sequence."""
        pass

    def accepts(self, action: Action) -> bool:
        """Accepts the action if all constituent rules accept it."""
        return all(rule.accepts(action) for rule in self._rules)

    def apply(self, action: Action) -> None:
        """Apply all constituent rules in sequence until one invalidates the action."""
        for rule in self._rules:
            rule.apply(action)
            if not action.is_valid:
                break
