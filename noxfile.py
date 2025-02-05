"""Nox sessions."""

import re
import subprocess
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

import nox
from packaging import version


def parse_requires_python(requirement: str) -> Dict[str, Optional[version.Version]]:
    """Parses a `requires-python` string (e.g., ">=3.9,<3.13")."""
    # get regex
    pattern = r"([<>]=?)\s*(\d+\.\d+)"
    constraints = re.findall(pattern, requirement)
    parsed_versions: Dict[str, Optional[version.Version]] = {
        ">=": None,
        "<=": None,
        ">": None,
        "<": None,
    }

    # populate dict
    for op, ver in constraints:
        parsed_versions[op] = version.parse(ver)

    return parsed_versions


def generate_python_versions(
    min_version: version.Version, max_version: version.Version
) -> List[str]:
    """Generates a list of Python versions incrementing by minor versions."""
    # setup versions
    python_versions = []
    current_version = min_version

    # loop
    while current_version < max_version:
        # add current minor version
        python_versions.append(str(current_version))

        # increment minor digit
        next_minor = current_version.minor + 1

        # update
        current_version = version.parse(f"{current_version.major}.{next_minor}")

    return python_versions


def get_python_versions_from_toml() -> List[str]:
    """Load Python version range from pyproject.toml."""
    # load the entire configuration from the pyproject.toml
    root_dir = Path(__file__).resolve().parent
    project_toml = nox.project.load_toml(str(root_dir / "pyproject.toml"))

    # extract the 'requires-python' field
    python_version_str = project_toml["project"]["requires-python"]

    # parse version constraints dynamically
    parsed_versions = parse_requires_python(python_version_str)

    # eetermine min and max versions (handling both `>=` and `>`, `<` and `<=`)
    min_version = parsed_versions.get(">=") or parsed_versions.get(">")
    max_version = parsed_versions.get("<=") or parsed_versions.get("<")

    # check for weirdness
    if min_version is None or max_version is None:
        raise ValueError(f"Invalid requires-python format: {python_version_str}")

    return generate_python_versions(min_version, max_version)


# generate Python versions dynamically from the pyproject.toml
PROJECT_PYTHON_VERSIONS = get_python_versions_from_toml()


def install_python_version(version: str) -> None:
    """Installs the given Python version using pyenv."""
    try:
        subprocess.run(["pyenv", "install", version], check=True)
    except subprocess.CalledProcessError as e:
        # Raise the error again with a custom message
        raise RuntimeError(
            f"Could not install Python version {version} using pyenv."
        ) from e


def install_lint_deps(session: nox.Session, deps: Optional[List[str]] = None) -> None:
    """Install specified linting dependencies (or all if not provided)."""
    # defaults
    all_deps = ["flake8", "black", "isort", "mypy", "deptry"]

    # Use provided dependencies or default to all
    deps_to_install = deps or all_deps

    # Install Nox if not already installed
    session.install("nox", "pytest")

    # Install the specified dependencies
    session.install(*deps_to_install)


@nox.session()
def setup(session: nox.Session) -> None:
    """Install required Python versions using pyenv."""
    for vers in PROJECT_PYTHON_VERSIONS:
        install_python_version(vers)


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run tests using pytest."""
    # Install Nox if not already installed
    session.install("nox")

    # Install test dependencies
    session.install("pytest")

    # Run the tests (assuming pytest is used)
    session.run("pytest")


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """Run all linting tools."""
    install_lint_deps(session)

    # Run all linting tools
    session.run("flake8")
    session.run("black", ".")
    session.run("isort", ".")
    session.run("mypy", ".")
    session.run("deptry", "src/")


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def isort(session: nox.Session) -> None:
    """Run isort."""
    install_lint_deps(session, deps=["isort"])
    session.run("isort", ".")


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def black(session: nox.Session) -> None:
    """Run black."""
    install_lint_deps(session, deps=["black"])
    session.run("black", ".")


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def flake8(session: nox.Session) -> None:
    """Run flake8."""
    install_lint_deps(session, deps=["flake8"])
    session.run("flake8")


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def mypy(session: nox.Session) -> None:
    """Run mypy."""
    install_lint_deps(session, deps=["mypy"])
    session.run("mypy", ".")


@nox.session(python=PROJECT_PYTHON_VERSIONS)
def deptry(session: nox.Session) -> None:
    """Run deptry."""
    install_lint_deps(session, deps=["deptry"])
    session.run("deptry", "src/")
