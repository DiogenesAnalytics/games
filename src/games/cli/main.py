"""Command-line interface for games."""

import click

from games.cli.wordle import wordle


@click.group()
def main() -> None:
    """Play and interact with games."""


main.add_command(wordle)
