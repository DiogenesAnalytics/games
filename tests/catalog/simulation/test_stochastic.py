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
    assert sim.states["coin"].value in {"Heads", "Tails"}


@pytest.mark.simulation
def test_coinflip_runs_multiple_times() -> None:
    """Test CoinFlip simulation runs multiple times."""
    sim = CoinFlip()
    for _ in range(10):  # simulate 10 flips
        sim.step()
        assert sim.states["coin"].value in {"Heads", "Tails"}


@pytest.mark.simulation
def test_diceroll_runs() -> None:
    """Test that DiceRoll simulation runs and each die has a valid result."""
    sim = DiceRoll(num_dice=3, num_sides=6)
    sim.step()
    for state in sim.states.values():
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
    assert sim.states["deck"].value in sim.states["deck"].available_values


@pytest.mark.simulation
def test_carddraw_runs_multiple_times() -> None:
    """Test that all drawn cards are valid members of the deck."""
    sim = CardDraw()
    drawn_cards = set()

    for _ in range(20):
        sim.step()
        drawn_cards.add(sim.states["deck"].value)

    assert drawn_cards.issubset(sim.states["deck"].available_values)


@pytest.mark.simulation
def test_carddraw_deck_completeness() -> None:
    """Ensure that the full deck contains exactly 52 unique cards."""
    sim = CardDraw()
    assert len(sim.states["deck"].available_values) == 52
    assert len(set(sim.states["deck"].available_values)) == 52
