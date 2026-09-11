"""Shared test fixtures."""

from typing import Set

import pytest


@pytest.fixture
def solutions() -> Set[str]:
    """Return a small solution dictionary for testing."""
    return {"CRANE", "STAIN", "PLANE"}


@pytest.fixture
def available_guesses() -> Set[str]:
    """Return the complete legal Wordle guess dictionary."""
    return {"CRANE", "STAIN", "PLANE", "SLATE"}
