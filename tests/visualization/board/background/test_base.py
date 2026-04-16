"""Tests for module games.visualization.board.background.base."""

import pytest

from games.visualization.board.background.base import Background


@pytest.mark.background
def test_background_is_abstract() -> None:
    """Background should not be instantiable directly."""
    with pytest.raises(TypeError):
        Background()  # type: ignore[abstract]
