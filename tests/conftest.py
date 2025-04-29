"""Configuration file for pytest."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """For configuring pytest with custom markers."""
    config.addinivalue_line("markers", "debug: debugging tests.")
    config.addinivalue_line("markers", "fixture: fixture tests.")
    config.addinivalue_line("markers", "abc: tests for abstract base classes")
    config.addinivalue_line("markers", "simulation: simulation tests")
    config.addinivalue_line("markers", "state: state tests")
    config.addinivalue_line("markers", "rule: rule tests")
