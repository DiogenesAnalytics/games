"""Core board rendering engine."""

from abc import ABC
from abc import abstractmethod
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence
from typing import Tuple

import matplotlib.pyplot as plt

from .background.base import Background
from .geometry.base import Geometry
from .protocol import CellValue
from .types import Grid
from .types import Overlay


@dataclass(frozen=True)
class RenderTheme:
    """Matplotlib styling configuration for rendering."""

    style: Optional[str] = None
    facecolor: Optional[str] = None
    axes_facecolor: Optional[str] = None
    axes_edgecolor: Optional[str] = None

    def subplot_kwargs(self) -> Dict[str, Any]:
        """Return kwargs for plt.subplots()."""
        kwargs: Dict[str, Any] = {}

        if self.facecolor is not None:
            kwargs["facecolor"] = self.facecolor

        return kwargs

    def apply_axes(self, ax: Any) -> None:
        """Apply axis-level styling."""
        if self.axes_facecolor is not None:
            ax.set_facecolor(self.axes_facecolor)

        if self.axes_edgecolor is not None:
            for spine in ax.spines.values():
                spine.set_edgecolor(self.axes_edgecolor)


DEFAULT_THEME: RenderTheme = RenderTheme()
"""No-op theme that preserves existing matplotlib environment."""

DARK_PUBLICATION_THEME = RenderTheme(
    style="dark_background",
    facecolor="#181818",
    axes_facecolor="#181818",
    axes_edgecolor="#181818",
)


@dataclass(frozen=True)
class RenderSpec:
    """Configuration for matplotlib rendering output."""

    figsize: Tuple[float, float] = (6.0, 6.0)
    dpi: int = 150
    show_axes: bool = False
    subtitle: Optional[str] = None
    subtitle_y: float = 0.98
    subtitle_fontsize: int = 12


class BoardRenderer(ABC):
    """Abstract base class for board renderers."""

    @abstractmethod
    def render(
        self,
        grid: Grid,
        *,
        spec: Optional[RenderSpec] = None,
        theme: Optional[RenderTheme] = None,
        title: str = "",
        overlays: Optional[Sequence[Overlay]] = None,
        return_ax: bool = False,
    ) -> Any:
        """Render a grid state."""
        raise NotImplementedError


class MatplotlibBoardRenderer(BoardRenderer):
    """Matplotlib-based implementation of board rendering."""

    def __init__(
        self,
        background: Background,
        geometry: Geometry,
        show_grid: bool = False,
    ) -> None:
        """Initialize renderer with board background and geometry."""
        self.background = background
        self.geometry = geometry
        self.show_grid = show_grid

    def render(
        self,
        grid: Grid,
        *,
        spec: Optional[RenderSpec] = None,
        theme: Optional[RenderTheme] = None,
        title: str = "",
        overlays: Optional[Sequence[Overlay]] = None,
        return_ax: bool = False,
    ) -> Any:
        """Render a board grid using matplotlib."""
        size: int = grid.shape[0]

        spec = spec or RenderSpec()
        theme = theme or DEFAULT_THEME

        style_ctx = (
            plt.style.context(theme.style) if theme.style is not None else nullcontext()
        )

        with style_ctx:
            fig, ax = plt.subplots(
                figsize=spec.figsize,
                dpi=spec.dpi,
                **theme.subplot_kwargs(),
            )

            theme.apply_axes(ax)

            self.background.draw(ax, size)
            self._draw_cells(ax, grid)
            self._draw_grid(ax, size)

            if overlays:
                for overlay in overlays:
                    overlay(ax)

            if title:
                ax.set_title(title)

            if spec.subtitle:
                fig.suptitle(
                    spec.subtitle,
                    y=spec.subtitle_y,
                    fontsize=spec.subtitle_fontsize,
                )

            if not spec.show_axes:
                ax.axis("off")

            if return_ax:
                return ax

            plt.show()

    def _draw_cells(self, ax: Any, grid: Grid) -> None:
        """Render all non-empty grid cells."""
        size: int = grid.shape[0]

        for r in range(size):
            for c in range(size):
                value: Optional[CellValue] = grid[r, c]

                if value is None:
                    continue

                x, y = self.geometry.cell_position(r, c)

                draw_fn = getattr(value, "draw", None)

                if callable(draw_fn) and draw_fn(ax, x, y, size):
                    continue

                ax.text(
                    x,
                    y,
                    value.render_symbol(),
                    ha="center",
                    va="center",
                    color=value.render_color(),
                    fontsize=max(10, int(240 / size)),
                    zorder=3,
                )

    def _draw_grid(self, ax: Any, size: int) -> None:
        """Draw optional renderer-level grid lines."""
        if not self.show_grid:
            return

        for i in range(size):
            ax.plot([0, size - 1], [i, i], linewidth=1)
            ax.plot([i, i], [0, size - 1], linewidth=1)
