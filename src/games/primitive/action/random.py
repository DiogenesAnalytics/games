"""Defines an action that selects randomly from available state choices."""

from games.primitive.action.base import Action


class RandomChoiceAction(Action):
    """Action representing a random selection from a ChoiceState's options."""

    def describe(self) -> str:
        """Description of the random choice action."""
        return "Randomly select one of the available choices from the state."
