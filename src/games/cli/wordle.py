"""Defines the Wordle command-line interface."""

import os
import random
from typing import List
from typing import Set
from typing import Tuple

import click
import pyfiglet
from rich.console import Console
from rich.text import Text

from games.catalog.simulation.wordle.actor import InteractiveWordlePlayer
from games.catalog.simulation.wordle.game import WordleGame
from games.catalog.simulation.wordle.words import load_answers
from games.catalog.simulation.wordle.words import load_words
from games.visualization.wordle.renderer import WordleRenderer


def _configure_terminal() -> None:
    """Configure terminal color support."""
    os.environ.setdefault("COLORTERM", "truecolor")


def _random_colors(colors: List[str]) -> List[str]:
    """Return colors in random order."""
    colors = colors.copy()
    random.shuffle(colors)
    return colors


def _select_target(answers: Set[str]) -> str:
    """Select a random Wordle answer."""
    return random.choice(sorted(answers))


def _print_banner() -> None:
    """Print the Wordle banner."""
    _configure_terminal()
    console = Console()

    colors = _random_colors(
        [
            "#6CA965",
            "#6CA965",
            "#C8B653",
            "#C8B653",
            "#787C7F",
            "#787C7F",
        ]
    )

    letters: Tuple[Tuple[str, str], ...] = tuple(
        zip(
            "WORDLE",
            colors,
            strict=True,
        )
    )

    banner = pyfiglet.figlet_format(
        "WORDLE",
        font="ansi_shadow",
    )

    lines = banner.rstrip("\n").splitlines()

    glyph_widths: List[int] = [
        len(
            pyfiglet.figlet_format(
                letter,
                font="ansi_shadow",
            ).splitlines()[0]
        )
        for letter, _ in letters
    ]

    for line in lines:
        text = Text()
        position = 0

        for (_, color), width in zip(
            letters,
            glyph_widths,
            strict=True,
        ):
            text.append(
                line[position : position + width],
                style=color,
            )
            position += width

        text.append(line[position:])
        console.print(text)


@click.command()
def wordle() -> None:
    """Play Wordle."""
    answers = load_answers()
    words = load_words()

    _print_banner()

    target = _select_target(answers)

    player = InteractiveWordlePlayer()
    game = WordleGame(
        solutions=answers,
        available_guesses=words,
        target=target,
        player=player,
    )
    renderer = WordleRenderer()

    while not game.is_done():
        try:
            game.step()
        except RuntimeError:
            click.echo("Invalid guess. Please try again.")
            continue

        click.echo(renderer.render_text(game.state))

    if game.state.target in game.state.guesses:
        click.echo(f"You got it in {len(game.state.guesses)} guesses!")
    else:
        click.echo(f"The word was {game.state.target}.")
