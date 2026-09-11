"""Defines terminal rendering for the Wordle simulation."""

from typing import List

from games.catalog.simulation.wordle.feedback import FeedbackTile
from games.catalog.simulation.wordle.state import WordleState


class TerminalWordleRenderer:
    """Render a Wordle game state for terminal display."""

    _EMPTY_TILE = "⬜"
    _GREEN_TILE = "🟩"
    _YELLOW_TILE = "🟨"
    _GRAY_TILE = "⬛"

    def render(self, state: WordleState) -> str:
        """Render the current Wordle board.

        Args:
            state: Wordle game state to render.

        Returns:
            A string containing the current Wordle board.
        """
        rows: List[str] = []

        for guess, result in zip(
            state.guesses,
            state.feedback,
            strict=True,
        ):
            rows.append(
                "".join(
                    self._render_tile(letter, tile)
                    for letter, tile in zip(guess, result, strict=True)
                )
            )

        while len(rows) < 6:
            rows.append(self._EMPTY_TILE * 5)

        return "\n".join(rows)

    def _render_tile(
        self,
        letter: str,
        tile: FeedbackTile,
    ) -> str:
        """Render a single Wordle tile."""
        if tile is FeedbackTile.GREEN:
            return f"{self._GREEN_TILE}{letter}"
        if tile is FeedbackTile.YELLOW:
            return f"{self._YELLOW_TILE}{letter}"
        return f"{self._GRAY_TILE}{letter}"
