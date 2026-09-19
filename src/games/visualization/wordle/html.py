"""Defines HTML rendering for the Wordle simulation."""

from typing import List

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.state import WordleState


class HtmlWordleRenderer:
    """Render a Wordle game state as HTML."""

    _EMPTY_TILE = "#d3d6da"
    _GREEN_TILE = "#6aaa64"
    _YELLOW_TILE = "#c9b458"
    _GRAY_TILE = "#787c7e"

    def render(self, state: WordleState) -> str:
        """Render the current Wordle board.

        Args:
            state: Wordle game state to render.

        Returns:
            A string containing the current Wordle board as HTML.
        """
        rows: List[str] = []

        for guess, result in zip(
            state.guesses,
            state.feedback,
            strict=True,
        ):
            tiles = "".join(
                self._render_tile(letter, tile)
                for letter, tile in zip(guess, result, strict=True)
            )
            rows.append(self._render_row(tiles))

        while len(rows) < 6:
            rows.append(self._render_empty_row())

        return (
            '<div style="'
            "display:flex;"
            "flex-direction:column;"
            "gap:4px;"
            '">'
            f'{"".join(rows)}'
            "</div>"
        )

    def _render_tile(
        self,
        letter: str,
        tile: FeedbackTile,
    ) -> str:
        """Render a single Wordle tile.

        Args:
            letter: Letter displayed in the tile.
            tile: Feedback classification for the letter.

        Returns:
            An HTML element representing the tile.
        """
        if tile is FeedbackTile.GREEN:
            background = self._GREEN_TILE
        elif tile is FeedbackTile.YELLOW:
            background = self._YELLOW_TILE
        else:
            background = self._GRAY_TILE

        return self._render_letter_tile(letter, background)

    def _render_empty_row(self) -> str:
        """Render an empty Wordle row.

        Returns:
            An HTML row containing five empty tiles.
        """
        tiles = "".join(
            self._render_letter_tile("", self._EMPTY_TILE) for _ in range(5)
        )
        return self._render_row(tiles)

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
