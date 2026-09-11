"""Provides Wordle word lists."""

from pathlib import Path
from typing import Set


_DATA_DIR = Path(__file__).parent / "data"


def _load_words(path: Path) -> Set[str]:
    """Load newline-delimited words from a data file."""
    with path.open(encoding="utf-8") as file:
        return {line.strip().upper() for line in file if line.strip()}


def load_answers() -> Set[str]:
    """Load the Wordle answer words."""
    return _load_words(_DATA_DIR / "answers.txt")


def load_guesses() -> Set[str]:
    """Load the additional Wordle guess words."""
    return _load_words(_DATA_DIR / "guesses.txt")


def load_words() -> Set[str]:
    """Load all legal Wordle guesses."""
    return load_answers() | load_guesses()
