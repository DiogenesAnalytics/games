"""Tests for module games.primitive.rule.base."""

import inspect

import pytest

from games.primitive.rule.base import Rule


@pytest.mark.abc
@pytest.mark.rule
def test_rule_abc_is_abstract() -> None:
    """Rule should be abstract."""
    assert inspect.isabstract(Rule)
