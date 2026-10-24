"""Test the DiogenOS command-line interface."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch

from diogenos.cli import main
from diogenos.system.base import System


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
def test_feature_list(monkeypatch: MonkeyPatch) -> None:
    """Verify that the feature list command prints registered identifiers."""
    registry = Mock()
    registry.list.return_value = ("pulsar", "tmux")

    monkeypatch.setattr("diogenos.cli.FeatureRegistry", lambda: registry)

    result = CliRunner().invoke(main, ["feature", "list"])

    assert result.exit_code == 0
    assert result.output == "pulsar\ntmux\n"
    registry.list.assert_called_once_with()


@pytest.mark.cli
def test_feature_check_satisfied(
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that checking a satisfied feature succeeds."""
    selected_feature = Mock()
    selected_feature.is_satisfied.return_value = True

    registry = Mock()
    registry.get.return_value = lambda: selected_feature

    system = Mock(spec=System)
    detector = Mock()
    detector.detect.return_value = system

    monkeypatch.setattr("diogenos.cli.FeatureRegistry", lambda: registry)
    monkeypatch.setattr("diogenos.cli.SystemDetector", lambda: detector)

    result = CliRunner().invoke(main, ["feature", "check", "pulsar"])

    assert result.exit_code == 0
    assert result.output == "Feature 'pulsar' is satisfied.\n"
    registry.get.assert_called_once_with("pulsar")
    detector.detect.assert_called_once_with()
    selected_feature.is_satisfied.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_check_unsatisfied(
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that checking an unsatisfied feature fails."""
    selected_feature = Mock()
    selected_feature.is_satisfied.return_value = False

    registry = Mock()
    registry.get.return_value = lambda: selected_feature

    system = Mock(spec=System)
    detector = Mock()
    detector.detect.return_value = system

    monkeypatch.setattr("diogenos.cli.FeatureRegistry", lambda: registry)
    monkeypatch.setattr("diogenos.cli.SystemDetector", lambda: detector)

    result = CliRunner().invoke(main, ["feature", "check", "pulsar"])

    assert result.exit_code == 1
    assert result.output == "Feature 'pulsar' is not satisfied.\n"
    selected_feature.is_satisfied.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_check_unknown_feature(
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that checking an unknown feature reports an error."""
    registry = Mock()
    registry.get.side_effect = KeyError("unknown feature identifier: missing")

    monkeypatch.setattr("diogenos.cli.FeatureRegistry", lambda: registry)

    result = CliRunner().invoke(main, ["feature", "check", "missing"])

    assert result.exit_code == 1
    assert result.output == ("Error: missing is not a registered feature.\n")
    registry.get.assert_called_once_with("missing")


@pytest.mark.cli
def test_feature_check_requires_feature_name() -> None:
    """Verify that feature check requires a feature identifier."""
    result = CliRunner().invoke(main, ["feature", "check"])

    assert result.exit_code == 2
    assert "Missing argument" in result.output
