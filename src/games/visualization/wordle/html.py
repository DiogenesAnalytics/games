"""Defines HTML rendering for the Wordle board."""

from typing import List

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell


class HtmlRenderer:
    """Render a Wordle board as HTML."""

    _EMPTY_TILE = "#d3d6da"
    _GREEN_TILE = "#6aaa64"
    _YELLOW_TILE = "#c9b458"
    _GRAY_TILE = "#787c7e"

    def render(self, board: WordleBoard) -> str:
        """Render a Wordle board.

        Args:
            board: Wordle board to render.

        Returns:
            A string containing the Wordle board as HTML.
        """
        rows: List[str] = []

        for row in board.rows:
            tiles = "".join(self._render_tile(cell) for cell in row)
            rows.append(self._render_row(tiles))

        return (
            '<div style="'
            "display:flex;"
            "flex-direction:column;"
            "gap:4px;"
            '">'
            f'{"".join(rows)}'
            "</div>"
        )

    def _render_tile(self, cell: WordleCell) -> str:
        """Render a single HTML tile.

        Args:
            cell: Board cell to render.

        Returns:
            An HTML element representing the tile.
        """
        if cell.feedback is FeedbackTile.GREEN:
            background = self._GREEN_TILE
        elif cell.feedback is FeedbackTile.YELLOW:
            background = self._YELLOW_TILE
        elif cell.feedback is FeedbackTile.GRAY:
            background = self._GRAY_TILE
        else:
            background = self._EMPTY_TILE

        return self._render_letter_tile(
            cell.letter or "",
            background,
        )

    @staticmethod
    def _render_row(tiles: str) -> str:
        """Render a row containing Wordle tiles.

        Args:
            tiles: HTML for the tiles in the row.

        Returns:
            An HTML row containing the supplied tiles.
        """
        return (
            '<div style="'
            "display:flex;"
            "flex-direction:row;"
            "gap:4px;"
            '">'
            f"{tiles}"
            "</div>"
        )

    @staticmethod
    def _render_letter_tile(
        letter: str,
        background: str,
    ) -> str:
        """Render a single HTML tile.

        Args:
            letter: Letter to display in the tile.
            background: Background color for the tile.

        Returns:
            An HTML element representing the tile.
        """
        return (
            '<div style="'
            "width:40px;"
            "height:40px;"
            "display:flex;"
            "align-items:center;"
            "justify-content:center;"
            "box-sizing:border-box;"
            "color:white;"
            "font-family:monospace;"
            "font-size:18px;"
            "font-weight:bold;"
            f"background:{background};"
            '">'
            f"{letter}"
            "</div>"
        )
