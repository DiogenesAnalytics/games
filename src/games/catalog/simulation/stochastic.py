"""Module contains simulations of chance-based events."""

from games.catalog.simulation.base import Simulation
from games.primitive.action.random import RandomChoiceAction
from games.primitive.actor.base import SimpleNonPlayer
from games.primitive.rule.random import RandomChoiceRule
from games.primitive.state.discrete import ChoiceState


class CoinFlip(Simulation):
    """A simple simulation of a coin flip using atomic states and rules."""

    def _register_components(self) -> None:
        """Set up the coin flip simulation with state, rule, and actor."""
        self.states = {"coin": ChoiceState({"Heads", "Tails"})}
        self.rules = [RandomChoiceRule()]
        self.actors = [SimpleNonPlayer(RandomChoiceAction)]

    def is_done(self) -> bool:
        """Coin flip simulation never ends automatically."""
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

        # store
        self.num_dice = num_dice
        self.num_sides = num_sides

        # register
        super().__init__()

    def _register_components(self) -> None:
        """Setup the dice roll states, rules, and actors."""
        self.states = {
            f"die_{i}": ChoiceState(set(range(1, self.num_sides + 1)))
            for i in range(self.num_dice)
        }
        self.rules = [RandomChoiceRule()]
        self.actors = [SimpleNonPlayer(RandomChoiceAction)]

    def is_done(self) -> bool:
        """Indicate if the simulation is done (in this case, never done)."""
        return False


class CardDraw(Simulation):
    """A simple simulation of a card draw using atomic states and rules."""

    def _register_components(self) -> None:
        """Set up the card draw simulation with state, rule, and actor."""
        self.states = {
            "deck": ChoiceState(
                {f"{rank}{suit}" for rank in "A23456789TJQK" for suit in "♠♥♦♣"}
            )
        }
        self.rules = [RandomChoiceRule()]
        self.actors = [SimpleNonPlayer(RandomChoiceAction)]

    def is_done(self) -> bool:
        """Card draw simulation never ends automatically."""
        return False
