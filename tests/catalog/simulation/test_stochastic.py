"""Test suite for 'games.catalog.simulation.stochastic' module."""

import pytest

from games.catalog.simulation.stochastic import CardDraw
from games.catalog.simulation.stochastic import CoinFlip
from games.catalog.simulation.stochastic import DiceRoll


@pytest.mark.simulation
def test_coinflip_runs() -> None:
    """Test that CoinFlip simulation runs and returns a valid result."""
    sim = CoinFlip()
    sim.step()
    assert sim.states[0].value in {"Heads", "Tails"}


@pytest.mark.simulation
def test_coinflip_runs_multiple_times() -> None:
    """Test CoinFlip simulation runs multiple times."""
    sim = CoinFlip()
    for _ in range(10):  # simulate 10 flips
        sim.step()
        assert sim.states[0].value in {"Heads", "Tails"}


@pytest.mark.simulation
def test_diceroll_runs() -> None:
    """Test that DiceRoll simulation runs and each die has a valid result."""
    sim = DiceRoll(num_dice=3, num_sides=6)
    sim.step()
    for state in sim.states:
        assert 1 <= state.value <= 6


@pytest.mark.simulation
def test_diceroll_states_integrity() -> None:
    """Test that DiceRoll simulation maintains state integrity."""
    sim = DiceRoll(num_dice=3, num_sides=6)
    initial_states = sim.states
    sim.step()
    assert len(sim.states) == len(initial_states)


@pytest.mark.simulation
def test_carddraw_runs() -> None:
    """Test that CardDraw simulation runs and returns a valid card."""
    sim = CardDraw()
    sim.step()
    assert sim.states[0].value in sim.states[0].available_values


@pytest.mark.simulation
def test_carddraw_runs_multiple_times() -> None:
    """Test that all drawn cards are valid members of the deck."""
    sim = CardDraw()
    drawn_cards = set()

    for _ in range(20):
        sim.step()
        drawn_cards.add(sim.states[0].value)

    assert drawn_cards.issubset(sim.states[0].available_values)


@pytest.mark.simulation
def test_carddraw_deck_completeness() -> None:
    """Ensure that the full deck contains exactly 52 unique cards."""
    sim = CardDraw()
    assert len(sim.states[0].available_values) == 52
    assert len(set(sim.states[0].available_values)) == 52


@pytest.mark.simulation
def test_coinflip_is_not_done() -> None:
    """Test that a coin flip simulation is not terminal."""
    sim = CoinFlip()

    assert not sim.is_done()


@pytest.mark.simulation
def test_diceroll_is_not_done() -> None:
    """Test that a dice roll simulation is not terminal."""
    sim = DiceRoll()

    assert not sim.is_done()


@pytest.mark.simulation
def test_carddraw_is_not_done() -> None:
    """Test that a card draw simulation is not terminal."""
    sim = CardDraw()

    assert not sim.is_done()


@pytest.mark.simulation
def test_diceroll_requires_at_least_one_die() -> None:
    """Test that a dice roll requires at least one die."""
    with pytest.raises(ValueError, match="at least one die"):
        DiceRoll(num_dice=0)


@pytest.mark.simulation
def test_diceroll_requires_at_least_three_sides() -> None:
    """Test that a die requires at least three sides."""
    with pytest.raises(ValueError, match="at least 3 sides"):
        DiceRoll(num_sides=2)
