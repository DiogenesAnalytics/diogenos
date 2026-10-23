"""Test the DiogenOS command-line interface."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from diogenos.cli import main


@pytest.mark.cli
def test_main_displays_help() -> None:
    """Verify that the CLI displays help."""
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Configure and manage a DiogenOS environment." in result.output
    assert "Usage:" in result.output
    assert "feature" in result.output


@pytest.mark.cli
def test_main_displays_help_for_no_arguments() -> None:
    """Verify that the CLI displays help when invoked without arguments."""
    result = CliRunner().invoke(main)

    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_feature_displays_help() -> None:
    """Verify that the feature command displays help."""
    result = CliRunner().invoke(main, ["feature", "--help"])

    assert result.exit_code == 0
    assert "Discover and manage features." in result.output
    assert "Usage:" in result.output
    assert "list" in result.output


@pytest.mark.cli
def test_feature_displays_help_for_no_arguments() -> None:
    """Verify that the feature command displays help without a subcommand."""
    result = CliRunner().invoke(main, ["feature"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_feature_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that the feature list command prints registered identifiers."""
    registry = Mock()
    registry.list.return_value = ("pulsar", "tmux")

    monkeypatch.setattr("diogenos.cli.FeatureRegistry", lambda: registry)

    result = CliRunner().invoke(main, ["feature", "list"])

    assert result.exit_code == 0
    assert result.output == "pulsar\ntmux\n"
    registry.list.assert_called_once_with()
