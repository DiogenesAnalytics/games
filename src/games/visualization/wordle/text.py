"""Defines text rendering for the Wordle board."""

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import WordleCell


class TextRenderer:
    """Render a Wordle board as text."""

    _EMPTY_TILE = "⬜"
    _GREEN_TILE = "🟩"
    _YELLOW_TILE = "🟨"
    _GRAY_TILE = "⬛"

    def render(self, board: WordleBoard) -> str:
        """Render a Wordle board as text."""
        rows = []

        for row in board.rows:
            rows.append("".join(self._render_tile(cell) for cell in row))

        return "\n".join(rows)

    def _render_tile(self, cell: WordleCell) -> str:
        """Render a single text tile."""
        if cell.feedback is FeedbackTile.GREEN:
            tile = self._GREEN_TILE
        elif cell.feedback is FeedbackTile.YELLOW:
            tile = self._YELLOW_TILE
        elif cell.feedback is FeedbackTile.GRAY:
            tile = self._GRAY_TILE
        else:
            tile = self._EMPTY_TILE

        return f"{tile}{cell.letter or ''}"
