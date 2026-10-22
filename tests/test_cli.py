"""Test the DiogenOS command-line interface."""

import pytest
from click.testing import CliRunner

from diogenos.cli import main


@pytest.mark.cli
def test_main_displays_help() -> None:
    """Verify that the CLI displays help."""
    runner = CliRunner()

    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Configure and manage a DiogenOS environment." in result.output
    assert "Usage:" in result.output


@pytest.mark.cli
def test_main_displays_help_for_no_arguments() -> None:
    """Verify that the CLI displays help when invoked without arguments."""
    runner = CliRunner()

    result = runner.invoke(main)

    assert result.exit_code == 0
    assert "Usage:" in result.output
