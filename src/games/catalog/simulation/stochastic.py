"""Module contains simulations of chance-based events."""

from games.catalog.simulation.base import Simulation
from games.primitive.action.random import RandomChoiceAction
from games.primitive.actor.base import SimpleNonPlayer
from games.primitive.rule.random import RandomChoiceRule
from games.primitive.state.discrete import ChoiceState


class CoinFlip(Simulation):
    """A simple simulation of a coin flip using atomic states and rules."""

    def __init__(self) -> None:
        """Initialize the coin flip simulation."""
        super().__init__()

        state = ChoiceState({"Heads", "Tails"})
        rule = RandomChoiceRule()
        actor = SimpleNonPlayer(RandomChoiceAction)

        self._register_state(state)
        self._register_rule(rule)
        self._register_actor(actor)
        self.authorize(actor, state)

    def is_done(self) -> bool:
        """Coin flip simulation never ends automatically."""
        return False


class DiceRoll(Simulation):
    """A simulation of rolling multiple dice using atomic states and rules."""

    def __init__(self, num_dice: int = 1, num_sides: int = 6) -> None:
        """Initialize the dice roll simulation."""
        if num_dice < 1:
            raise ValueError("Must roll at least one die.")
        if num_sides < 3:
            raise ValueError("Dice must have at least 3 sides.")

        super().__init__()

        states = [ChoiceState(set(range(1, num_sides + 1))) for _ in range(num_dice)]
        rule = RandomChoiceRule()
        actor = SimpleNonPlayer(RandomChoiceAction)

        for state in states:
            self._register_state(state)

        self._register_rule(rule)
        self._register_actor(actor)

        for state in states:
            self.authorize(actor, state)

        self.num_dice = num_dice
        self.num_sides = num_sides

    def is_done(self) -> bool:
        """Indicate if the simulation is done."""
        return False


class CardDraw(Simulation):
    """A simple simulation of a card draw using atomic states and rules."""

    def __init__(self) -> None:
        """Initialize the card draw simulation."""
        super().__init__()

        state = ChoiceState(
            set(f"{rank}{suit}" for rank in "A23456789TJQK" for suit in "♠♥♦♣")
        )
        rule = RandomChoiceRule()
        actor = SimpleNonPlayer(RandomChoiceAction)

        self._register_state(state)
        self._register_rule(rule)
        self._register_actor(actor)
        self.authorize(actor, state)

    def is_done(self) -> bool:
        """Card draw simulation never ends automatically."""
        return False
