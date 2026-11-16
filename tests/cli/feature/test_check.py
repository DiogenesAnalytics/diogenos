"""Test the feature check command."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from diogenos.cli import main
from diogenos.system.base import System


@pytest.mark.cli
def test_feature_check_satisfied(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that checking a satisfied feature succeeds."""
    selected_feature = Mock()
    selected_feature.is_satisfied.return_value = True
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(main, ["feature", "check", "pulsar"])

    assert result.exit_code == 0
    assert result.output == (
        "Feature  Status\n" "-------  ---------\n" "pulsar   Satisfied\n"
    )
    registry.get.assert_called_once_with("pulsar")
    detector.detect.assert_called_once_with()
    selected_feature.is_satisfied.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_check_unsatisfied(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that checking an unsatisfied feature fails."""
    selected_feature = Mock()
    selected_feature.is_satisfied.return_value = False
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(main, ["feature", "check", "pulsar"])

    assert result.exit_code == 1
    assert result.output == (
        "Feature  Status\n" "-------  -------------\n" "pulsar   Not satisfied\n"
    )
    selected_feature.is_satisfied.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_check_unknown_feature(
    registry: Mock,
    detector: Mock,
) -> None:
    """Verify that checking an unknown feature reports an error."""
    registry.get.side_effect = KeyError("unknown feature identifier: missing")

    result = CliRunner().invoke(main, ["feature", "check", "missing"])

    assert result.exit_code == 1
    assert result.output == (
        "Error: missing is not a registered feature.\n"
        "Feature  Status\n"
        "-------  ------\n"
    )
    registry.get.assert_called_once_with("missing")


@pytest.mark.cli
def test_feature_check_requires_feature_name() -> None:
    """Verify that feature check requires IDs or --all."""
    result = CliRunner().invoke(main, ["feature", "check"])

    assert result.exit_code == 2
    assert "Specify one or more feature IDs or use --all." in result.output


@pytest.mark.cli
def test_feature_check_all(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that --all checks every registered feature."""
    first_feature = Mock()
    first_feature.is_satisfied.return_value = True

    second_feature = Mock()
    second_feature.is_satisfied.return_value = True

    registry.list.return_value = ("pulsar", "tmux")
    registry.get.side_effect = [
        lambda: first_feature,
        lambda: second_feature,
    ]

    result = CliRunner().invoke(main, ["feature", "check", "--all"])

    assert result.exit_code == 0
    assert result.output == (
        "Feature  Status\n"
        "-------  ---------\n"
        "pulsar   Satisfied\n"
        "tmux     Satisfied\n"
    )
    registry.list.assert_called_once_with()
    registry.get.assert_any_call("pulsar")
    registry.get.assert_any_call("tmux")
    first_feature.is_satisfied.assert_called_once_with(system)
    second_feature.is_satisfied.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_check_multiple_features(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that multiple specified features are checked."""
    first_feature = Mock()
    first_feature.is_satisfied.return_value = True

    second_feature = Mock()
    second_feature.is_satisfied.return_value = True

    registry.get.side_effect = [
        lambda: first_feature,
        lambda: second_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "check", "pulsar", "tmux"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Feature  Status\n"
        "-------  ---------\n"
        "pulsar   Satisfied\n"
        "tmux     Satisfied\n"
    )
    registry.get.assert_any_call("pulsar")
    registry.get.assert_any_call("tmux")
    first_feature.is_satisfied.assert_called_once_with(system)
    second_feature.is_satisfied.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_check_all_rejects_feature_names() -> None:
    """Verify that --all cannot be combined with feature IDs."""
    result = CliRunner().invoke(
        main,
        ["feature", "check", "--all", "pulsar"],
    )

    assert result.exit_code == 2
    assert "Specify either --all or feature IDs, not both." in result.output


@pytest.mark.cli
def test_feature_check_unknown_feature_continues(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that checking continues after an unknown feature."""
    selected_feature = Mock()
    selected_feature.is_satisfied.return_value = True

    registry.get.side_effect = [
        KeyError("unknown feature identifier: missing"),
        lambda: selected_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "check", "missing", "pulsar"],
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: missing is not a registered feature.\n"
        "Feature  Status\n"
        "-------  ---------\n"
        "pulsar   Satisfied\n"
    )
    assert registry.get.call_count == 2
    selected_feature.is_satisfied.assert_called_once_with(system)
