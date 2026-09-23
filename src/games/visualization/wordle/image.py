"""Defines image rendering for the Wordle board."""

from typing import Optional

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell


class ImageRenderer:
    """Render a Wordle board as an image."""

    _EMPTY_TILE = "#d3d6da"
    _GREEN_TILE = "#6aaa64"
    _YELLOW_TILE = "#c9b458"
    _GRAY_TILE = "#787c7e"

    def render(
        self,
        board: WordleBoard,
        image_format: str = "svg",
    ) -> bytes:
        """Render a Wordle board as an image.

        Args:
            board: Wordle board to render.
            image_format: Image format to render.

        Raises:
            ValueError: If the image format is unsupported.

        Returns:
            The rendered image as bytes.
        """
        if image_format != "svg":
            raise ValueError(f"Unsupported image format: {image_format}")

        return self._render_svg(board)

    def _render_svg(self, board: WordleBoard) -> bytes:
        """Render a Wordle board as SVG."""
        tile_size = 40
        gap = 4
        rows = len(board.rows)
        columns = max((len(row) for row in board.rows), default=0)

        width = columns * tile_size + (columns - 1) * gap
        height = rows * tile_size + (rows - 1) * gap

        elements = []

        for row_index, row in enumerate(board.rows):
            for column_index, cell in enumerate(row):
                x = column_index * (tile_size + gap)
                y = row_index * (tile_size + gap)

                elements.append(
                    self._render_cell(
                        cell,
                        x,
                        y,
                        tile_size,
                    )
                )

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f"width={str(width)!r} height={str(height)!r} "
            f'viewBox="0 0 {width} {height}">'
            f"{''.join(elements)}"
            "</svg>"
        )

        return svg.encode("utf-8")

    def _render_cell(
        self,
        cell: WordleCell,
        x: int,
        y: int,
        size: int,
    ) -> str:
        """Render a single Wordle cell as SVG."""
        background = self._background(cell.feedback)

        letter = cell.letter or ""

        return (
            f"<rect x={str(x)!r} y={str(y)!r} "
            f"width={str(size)!r} height={str(size)!r} "
            f"fill={background!r}/>"
            f"<text x={str(x + size / 2)!r} "
            f"y={str(y + size / 2)!r} "
            'text-anchor="middle" dominant-baseline="central" '
            'fill="white" font-family="monospace" '
            'font-size="18" font-weight="bold">'
            f"{letter}"
            "</text>"
        )

    def _background(
        self,
        feedback: Optional[FeedbackTile],
    ) -> str:
        """Return the background color for a feedback value."""
        if feedback is FeedbackTile.GREEN:
            return self._GREEN_TILE
        if feedback is FeedbackTile.YELLOW:
            return self._YELLOW_TILE
        if feedback is FeedbackTile.GRAY:
            return self._GRAY_TILE
        return self._EMPTY_TILE
