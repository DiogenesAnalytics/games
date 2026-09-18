"""Defines the Wordle command-line interface."""

import random
from typing import Set

import click

from games.catalog.simulation.wordle.actor import InteractiveWordlePlayer
from games.catalog.simulation.wordle.game import WordleGame
from games.catalog.simulation.wordle.words import load_answers
from games.catalog.simulation.wordle.words import load_words
from games.visualization.wordle.terminal import TerminalWordleRenderer


def _select_target(answers: Set[str]) -> str:
    """Select a random Wordle answer."""
    return random.choice(sorted(answers))


@click.command()
def wordle() -> None:
    """Play Wordle."""
    answers = load_answers()
    words = load_words()

    target = _select_target(answers)

    player = InteractiveWordlePlayer()
    game = WordleGame(
        solutions=answers,
        available_guesses=words,
        target=target,
        player=player,
    )
    renderer = TerminalWordleRenderer()

    while not game.is_done():
        try:
            game.step()
        except RuntimeError:
            click.echo("Invalid guess. Please try again.")
            continue

        click.echo(renderer.render(game.state))

    if game.state.target in game.state.guesses:
        click.echo(f"You got it in {len(game.state.guesses)} guesses!")
    else:
        click.echo(f"The word was {game.state.target}.")
