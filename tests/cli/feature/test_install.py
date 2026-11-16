"""Test the feature install command."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from diogenos.cli import main
from diogenos.system.base import System


@pytest.mark.cli
def test_feature_install_succeeds(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that installing a feature succeeds."""
    selected_feature = Mock()
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(
        main,
        ["feature", "install", "pulsar"],
    )

    assert result.exit_code == 0
    assert result.output == "Feature 'pulsar' installed successfully.\n"
    registry.get.assert_called_once_with("pulsar")
    detector.detect.assert_called_once_with()
    selected_feature.apply.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_install_multiple_features(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that multiple features are installed."""
    first_feature = Mock()
    second_feature = Mock()

    registry.get.side_effect = [
        lambda: first_feature,
        lambda: second_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "install", "pulsar", "tmux"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Feature 'pulsar' installed successfully.\n"
        "Feature 'tmux' installed successfully.\n"
    )
    registry.get.assert_any_call("pulsar")
    registry.get.assert_any_call("tmux")
    first_feature.apply.assert_called_once_with(system)
    second_feature.apply.assert_called_once_with(system)
    detector.detect.assert_called_once_with()


@pytest.mark.cli
def test_feature_install_all(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that --all installs every registered feature."""
    first_feature = Mock()
    second_feature = Mock()

    registry.list.return_value = ("pulsar", "tmux")
    registry.get.side_effect = [
        lambda: first_feature,
        lambda: second_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "install", "--all"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Feature 'pulsar' installed successfully.\n"
        "Feature 'tmux' installed successfully.\n"
    )
    registry.list.assert_called_once_with()
    registry.get.assert_any_call("pulsar")
    registry.get.assert_any_call("tmux")
    first_feature.apply.assert_called_once_with(system)
    second_feature.apply.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_install_unknown_feature(
    registry: Mock,
    detector: Mock,
) -> None:
    """Verify that installing an unknown feature reports an error."""
    registry.get.side_effect = KeyError("unknown feature identifier: missing")

    result = CliRunner().invoke(
        main,
        ["feature", "install", "missing"],
    )

    assert result.exit_code == 1
    assert result.output == "Error: missing is not a registered feature.\n"
    registry.get.assert_called_once_with("missing")


@pytest.mark.cli
def test_feature_install_continues_after_unknown_feature(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that installation continues after an unknown feature."""
    selected_feature = Mock()

    registry.get.side_effect = [
        KeyError("unknown feature identifier: missing"),
        lambda: selected_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "install", "missing", "pulsar"],
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: missing is not a registered feature.\n"
        "Feature 'pulsar' installed successfully.\n"
    )
    assert registry.get.call_count == 2
    selected_feature.apply.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_install_continues_after_installation_failure(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that installation continues after a feature fails."""
    failed_feature = Mock()
    failed_feature.apply.side_effect = RuntimeError("component installation failed")

    successful_feature = Mock()

    registry.get.side_effect = [
        lambda: failed_feature,
        lambda: successful_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "install", "docker", "tmux"],
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: installation of feature 'docker' failed: "
        "component installation failed\n"
        "Feature 'tmux' installed successfully.\n"
    )
    failed_feature.apply.assert_called_once_with(system)
    successful_feature.apply.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_install_requires_feature_name() -> None:
    """Verify that feature install requires IDs or --all."""
    result = CliRunner().invoke(main, ["feature", "install"])

    assert result.exit_code == 2
    assert "Specify one or more feature IDs or use --all." in result.output


@pytest.mark.cli
def test_feature_install_all_rejects_feature_names() -> None:
    """Verify that --all cannot be combined with feature IDs."""
    result = CliRunner().invoke(
        main,
        ["feature", "install", "--all", "pulsar"],
    )

    assert result.exit_code == 2
    assert "Specify either --all or feature IDs, not both." in result.output
