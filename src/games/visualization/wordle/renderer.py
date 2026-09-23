"""Defines Wordle rendering."""

from games.catalog.simulation.wordle.state import WordleState
from games.visualization.wordle.board import WordleBoard
from games.visualization.wordle.board import create_wordle_board
from games.visualization.wordle.html import HtmlRenderer
from games.visualization.wordle.image import ImageRenderer
from games.visualization.wordle.text import TextRenderer


class WordleRenderer:
    """Render Wordle game states in different representations."""

    def __init__(self) -> None:
        """Initialize the renderer."""
        self._html_renderer = HtmlRenderer()
        self._image_renderer = ImageRenderer()
        self._text_renderer = TextRenderer()

    def render_html(self, state: WordleState) -> str:
        """Render a Wordle state as HTML."""
        return self._html_renderer.render(self._create_board(state))

    def render_image(
        self,
        state: WordleState,
        image_format: str = "svg",
    ) -> bytes:
        """Render a Wordle state as an image."""
        return self._image_renderer.render(
            self._create_board(state),
            image_format,
        )

    def render_text(self, state: WordleState) -> str:
        """Render a Wordle state as text."""
        return self._text_renderer.render(self._create_board(state))

    @staticmethod
    def _create_board(state: WordleState) -> WordleBoard:
        """Create a visual board from a Wordle state."""
        return create_wordle_board(
            state.guesses,
            state.feedback,
        )
