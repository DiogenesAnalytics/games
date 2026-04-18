"""Tests for module games.visualization.board.renderer."""

from typing import Any
from typing import Dict
from typing import List
from typing import Protocol
from typing import Tuple

import matplotlib.axes
import numpy as np
import pytest
from pytest import MonkeyPatch

from games.visualization.board.background.base import Background
from games.visualization.board.geometry.base import Geometry
from games.visualization.board.renderer import MatplotlibBoardRenderer
from games.visualization.board.renderer import RenderSpec
from games.visualization.board.types import Grid


class RendererFactory(Protocol):
    """Callable that constructs a MatplotlibBoardRenderer."""

    def __call__(self, show_grid: bool = False) -> MatplotlibBoardRenderer:
        """Create a renderer instance."""


class DummyCell:
    """Minimal CellValue-compatible test object."""

    def render_symbol(self) -> str:
        """Return dummy symbol."""
        return "X"

    def render_color(self) -> str:
        """Return dummy color."""
        return "white"


class BackgroundSpy(Background):
    """Test double for Background that records draw calls."""

    def __init__(self) -> None:
        """Initialize empty call log."""
        self.calls: List[int] = []

    def draw(self, ax: Any, size: int) -> None:
        """Record a background draw call."""
        self.calls.append(size)


class GeometrySpy(Geometry):
    """Test double for Geometry that records coordinate lookups."""

    def __init__(self) -> None:
        """Initialize empty call log."""
        self.calls: List[Tuple[int, int]] = []

    def cell_position(self, r: int, c: int) -> Tuple[float, float]:
        """Record coordinate lookup and return centered position."""
        self.calls.append((r, c))
        return c + 0.5, r + 0.5


@pytest.fixture
def empty_grid() -> Grid:
    """Provide a small empty grid for renderer tests."""
    return np.full((3, 3), None, dtype=object)


@pytest.fixture
def grid_with_cells() -> Grid:
    """Provide a small grid with a few populated cells."""
    grid: Grid = np.full((3, 3), None, dtype=object)
    grid[0, 0] = DummyCell()
    grid[2, 2] = DummyCell()
    return grid


@pytest.fixture
def background_spy() -> BackgroundSpy:
    """Provide a BackgroundSpy instance for renderer tests."""
    return BackgroundSpy()


@pytest.fixture
def geometry_spy() -> GeometrySpy:
    """Provide a GeometrySpy instance."""
    return GeometrySpy()


@pytest.fixture
def text_spy(monkeypatch: MonkeyPatch) -> List[Tuple[Tuple[Any, ...], Dict[str, Any]]]:
    """Capture calls to matplotlib Axes.text."""
    calls: List[Tuple[Tuple[Any, ...], Dict[str, Any]]] = []

    def fake_text(self: Any, *args: Any, **kwargs: Any) -> None:
        """Record text draw call."""
        calls.append((args, kwargs))

    monkeypatch.setattr(matplotlib.axes.Axes, "text", fake_text)

    return calls


@pytest.fixture
def make_renderer(
    background_spy: BackgroundSpy,
    geometry_spy: GeometrySpy,
) -> RendererFactory:
    """Factory for constructing MatplotlibBoardRenderer instances."""

    def _make(show_grid: bool = False) -> MatplotlibBoardRenderer:
        """Create renderer with injected test doubles."""
        return MatplotlibBoardRenderer(
            background=background_spy,
            geometry=geometry_spy,
            show_grid=show_grid,
        )

    return _make


@pytest.mark.renderer
def test_renderer_renders_non_empty_cells(
    make_renderer: RendererFactory,
    grid_with_cells: Grid,
    text_spy: List[Tuple[Tuple[Any, ...], Dict[str, Any]]],
) -> None:
    """Renderer should draw one text element per non-empty cell."""
    renderer = make_renderer()

    renderer.render(grid_with_cells)

    assert len(text_spy) == 2


@pytest.mark.renderer
def test_renderer_skips_empty_cells(
    make_renderer: RendererFactory,
    empty_grid: Grid,
    text_spy: List[Tuple[Tuple[Any, ...], Dict[str, Any]]],
) -> None:
    """Renderer should not draw text for empty cells."""
    renderer = make_renderer()

    renderer.render(empty_grid)

    assert text_spy == []


@pytest.mark.renderer
def test_renderer_calls_background_once(
    make_renderer: RendererFactory,
    empty_grid: Grid,
    background_spy: BackgroundSpy,
) -> None:
    """Renderer should draw background exactly once."""
    renderer = make_renderer()

    renderer.render(empty_grid)

    assert len(background_spy.calls) == 1


@pytest.mark.renderer
def test_renderer_cell_coordinates(
    make_renderer: RendererFactory,
    grid_with_cells: Grid,
    geometry_spy: GeometrySpy,
) -> None:
    """Renderer should delegate coordinate mapping to Geometry."""
    renderer = make_renderer()
    renderer.render(grid_with_cells)

    assert (0, 0) in geometry_spy.calls
    assert (2, 2) in geometry_spy.calls


@pytest.mark.renderer
def test_renderer_uses_cell_symbol_and_color(
    make_renderer: RendererFactory,
    grid_with_cells: Grid,
    text_spy: List[Tuple[Tuple[Any, ...], Dict[str, Any]]],
) -> None:
    """Renderer should use CellValue symbol and color."""
    renderer = make_renderer()

    renderer.render(grid_with_cells)

    for args, kwargs in text_spy:
        assert args[2] == "X"
        assert kwargs["color"] == "white"


@pytest.mark.renderer
def test_renderer_applies_render_spec_figure_settings(
    make_renderer: RendererFactory,
    empty_grid: Grid,
) -> None:
    """Renderer should apply RenderSpec figsize and dpi."""
    renderer: MatplotlibBoardRenderer = make_renderer()

    spec: RenderSpec = RenderSpec(
        figsize=(8.0, 8.0),
        dpi=220,
    )

    ax: Any = renderer.render(
        empty_grid,
        spec=spec,
        return_ax=True,
    )

    fig = ax.figure

    assert tuple(fig.get_size_inches()) == spec.figsize
    assert fig.dpi == spec.dpi


@pytest.mark.renderer
def test_renderer_applies_subtitle(
    make_renderer: RendererFactory,
    empty_grid: Grid,
    monkeypatch: MonkeyPatch,
) -> None:
    """Renderer should apply subtitle from RenderSpec."""
    renderer: MatplotlibBoardRenderer = make_renderer()

    calls: List[Dict[str, Any]] = []

    def fake_suptitle(self: Any, text: str, **kwargs: Any) -> None:
        """Record suptitle call."""
        calls.append(
            {
                "text": text,
                "kwargs": kwargs,
            }
        )

    monkeypatch.setattr("matplotlib.figure.Figure.suptitle", fake_suptitle)

    spec: RenderSpec = RenderSpec(
        subtitle="Example subtitle",
        subtitle_y=0.02,
        subtitle_fontsize=14,
    )

    renderer.render(
        empty_grid,
        spec=spec,
    )

    assert len(calls) == 1
    assert calls[0]["text"] == "Example subtitle"
    assert calls[0]["kwargs"]["y"] == 0.02
    assert calls[0]["kwargs"]["fontsize"] == 14


@pytest.mark.renderer
def test_renderer_hides_axes_when_configured(
    make_renderer: RendererFactory,
    empty_grid: Grid,
) -> None:
    """Renderer should hide axes when show_axes is False."""
    renderer: MatplotlibBoardRenderer = make_renderer()

    spec: RenderSpec = RenderSpec(show_axes=False)

    ax: Any = renderer.render(
        empty_grid,
        spec=spec,
        return_ax=True,
    )

    assert ax.axison is False
