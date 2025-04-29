"""Tests for module games.simulation.base."""

import inspect

import pytest

from games.simulation.base import Simulation


@pytest.mark.abc
@pytest.mark.simulation
def test_simulation_abc_is_abstract() -> None:
    """Simulation should be abstract."""
    assert inspect.isabstract(Simulation)
