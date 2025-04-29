"""Test suite for 'games.catalog.simulation.stochastic' module."""

import pytest

from games.catalog.simulation.stochastic import CoinFlip
from games.catalog.simulation.stochastic import DiceRoll


@pytest.mark.simulation
def test_coinflip_runs() -> None:
    """Test that CoinFlip simulation runs and returns a valid result."""
    sim = CoinFlip()
    sim.step()
    assert sim.state.value in {"Heads", "Tails"}


@pytest.mark.simulation
def test_coinflip_runs_multiple_times() -> None:
    """Test CoinFlip simulation runs multiple times."""
    sim = CoinFlip()
    for _ in range(10):  # simulate 10 flips
        sim.step()
        assert sim.state.value in {"Heads", "Tails"}


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
    # verify the states object is not changed unexpectedly
    assert len(sim.states) == len(initial_states)
