"""Module contains simulations of chance-based events."""

from games.primitive.rule.random import RandomChoiceRule
from games.primitive.state.discrete import ChoiceState
from games.simulation.base import Simulation


class CoinFlip(Simulation):
    """A simple simulation of a coin flip using atomic states and rules."""

    def __init__(self) -> None:
        """Set up a coin flip simulation with two possible outcomes."""
        self.state = ChoiceState(choices={"Heads", "Tails"})
        self.rule = RandomChoiceRule()

    def step(self) -> None:
        """Execute one step of the simulation: flip the coin."""
        self.rule.apply(self.state)
        print(f"Coin landed on: {self.state.value}")

    def is_done(self) -> bool:
        """Indicate if the simulation is done (in this case, never done)."""
        return False


class DiceRoll(Simulation):
    """A simulation of rolling multiple dice using atomic states and rules."""

    def __init__(self, num_dice: int = 1, num_sides: int = 6) -> None:
        """Initialize the simulation with a specified number of dice."""
        # check correct parameters
        if num_dice < 1:
            raise ValueError("Must roll at least one die.")
        if num_sides < 3:
            raise ValueError("Dice must have at least 3 sides.")

        # generate states and store rules
        self.states = [
            ChoiceState(choices=set(range(1, num_sides + 1))) for _ in range(num_dice)
        ]
        self.rule = RandomChoiceRule()

    def step(self) -> None:
        """Execute one step of the simulation: roll the dice."""
        # apply the rule to each die and update the state
        for i, state in enumerate(self.states):
            self.rule.apply(state)
            print(f"Die {i + 1} rolled: {state.value}")

    def is_done(self) -> bool:
        """Indicate if the simulation is done (in this case, never done)."""
        return False
