"""Defines rules for resolving actions in a Wordle simulation."""

from typing import Callable
from typing import List

from games.primitive.action.base import Action
from games.primitive.rule.base import CompoundRule
from games.primitive.rule.base import ExecutorRule
from games.primitive.rule.base import Rule
from games.primitive.rule.base import ValidationRule
from games.primitive.state.base import State

from .action import WordleGuess
from .feedback import feedback
from .state import WordleState


class WordleGuessValidationRule(ValidationRule):
    """Validate a proposed Wordle guess against a Wordle state."""

    def accepts(self, action: Action, state: State) -> bool:
        """Return whether this rule can handle the action and state."""
        return isinstance(action, WordleGuess) and isinstance(state, WordleState)

    def validate(self, action: Action, state: State) -> bool:
        """Return whether the proposed guess is legal.

        Args:
            action: Wordle guess to validate.
            state: Current Wordle game state.

        Returns:
            ``True`` if the guess is an allowable Wordle guess;
            otherwise ``False``.

        Raises:
            TypeError: If the action or state is not a Wordle type.
        """
        if not self.accepts(action, state):
            raise TypeError("Expected WordleGuess and WordleState.")

        assert isinstance(action, WordleGuess)
        assert isinstance(state, WordleState)

        return action.word in state.available_values


class WordleGuessExecutorRule(ExecutorRule):
    """Create an executor that applies a Wordle guess to the state."""

    def accepts(self, action: Action, state: State) -> bool:
        """Return whether this rule can handle the action and state."""
        return isinstance(action, WordleGuess) and isinstance(state, WordleState)

    def bind_executor(
        self,
        action: Action,
        state: State,
    ) -> Callable[[State], None]:
        """Return an executor that applies the Wordle guess.

        Args:
            action: Wordle guess to execute.
            state: Current Wordle game state.

        Returns:
            Function that applies the guess to a Wordle state.

        Raises:
            TypeError: If the action or state is not a Wordle type.
        """
        if not self.accepts(action, state):
            raise TypeError("Expected WordleGuess and WordleState.")

        assert isinstance(action, WordleGuess)
        assert isinstance(state, WordleState)

        guess = action.word
        target = state.target

        def execute(new_state: State) -> None:
            """Apply the guess to the supplied Wordle state."""
            if not isinstance(new_state, WordleState):
                raise TypeError("Expected WordleState.")

            result = feedback(target, guess)
            new_state.update((guess, result))

        return execute


class WordleRule(CompoundRule):
    """Resolve Wordle guesses against a Wordle game state."""

    @property
    def _rules(self) -> List[Rule]:
        """Return the rules used to resolve a Wordle guess."""
        return [
            WordleGuessValidationRule(),
            WordleGuessExecutorRule(),
        ]

    def accepts(self, action: Action, state: State) -> bool:
        """Return whether this rule accepts the action and state."""
        return all(rule.accepts(action, state) for rule in self._rules)
