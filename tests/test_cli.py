"""Test the DiogenOS command-line interface."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch

from diogenos.cli import main
from diogenos.system.base import System


@pytest.fixture
def registry(monkeypatch: MonkeyPatch) -> Mock:
    """Provide a mocked feature registry."""
    registry = Mock()
    monkeypatch.setattr("diogenos.cli.FeatureRegistry", lambda: registry)

    return registry


@pytest.fixture
def detector(monkeypatch: MonkeyPatch, system: System) -> Mock:
    """Provide a mocked system detector."""
    detector = Mock()
    detector.detect.return_value = system

    monkeypatch.setattr("diogenos.cli.SystemDetector", lambda: detector)

    return detector


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
def test_feature_list(registry: Mock) -> None:
    """Verify that the feature list command prints registered identifiers."""
    registry.list.return_value = ("pulsar", "tmux")

    result = CliRunner().invoke(main, ["feature", "list"])

    assert result.exit_code == 0
    assert result.output == "pulsar\ntmux\n"
    registry.list.assert_called_once_with()


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
    assert result.output == "Feature 'pulsar' is satisfied.\n"
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
    assert result.output == "Feature 'pulsar' is not satisfied.\n"
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
    assert result.output == "Error: missing is not a registered feature.\n"
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
        "Feature 'pulsar' is satisfied.\n" "Feature 'tmux' is satisfied.\n"
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
        "Feature 'pulsar' is satisfied.\n" "Feature 'tmux' is satisfied.\n"
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
        "Feature 'pulsar' is satisfied.\n"
    )
    assert registry.get.call_count == 2
    selected_feature.is_satisfied.assert_called_once_with(system)


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


@pytest.mark.cli
def test_feature_components(registry: Mock) -> None:
    """Verify that the feature components command lists components."""
    selected_feature = Mock()
    selected_feature.resolved_components = (
        Mock(registry_id="firefox"),
        Mock(registry_id="docker"),
    )
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(
        main,
        ["feature", "components", "desktop"],
    )

    assert result.exit_code == 0
    assert result.output == ("Feature 'desktop':\n" "  firefox\n" "  docker\n")
    registry.get.assert_called_once_with("desktop")


@pytest.mark.cli
def test_feature_components_multiple_features(registry: Mock) -> None:
    """Verify that components from multiple features are listed."""
    first_feature = Mock()
    first_feature.resolved_components = (Mock(registry_id="firefox"),)

    second_feature = Mock()
    second_feature.resolved_components = (Mock(registry_id="docker"),)

    registry.get.side_effect = [
        lambda: first_feature,
        lambda: second_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "components", "desktop", "server"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Feature 'desktop':\n" "  firefox\n" "Feature 'server':\n" "  docker\n"
    )
    registry.get.assert_any_call("desktop")
    registry.get.assert_any_call("server")


@pytest.mark.cli
def test_feature_components_unknown_feature(registry: Mock) -> None:
    """Verify that an unknown feature reports an error."""
    registry.get.side_effect = KeyError("unknown feature identifier: missing")

    result = CliRunner().invoke(
        main,
        ["feature", "components", "missing"],
    )

    assert result.exit_code == 1
    assert result.output == "Error: missing is not a registered feature.\n"
    registry.get.assert_called_once_with("missing")


@pytest.mark.cli
def test_feature_components_continues_after_unknown_feature(
    registry: Mock,
) -> None:
    """Verify that component listing continues after an unknown feature."""
    selected_feature = Mock()
    selected_feature.resolved_components = (Mock(registry_id="firefox"),)

    registry.get.side_effect = [
        KeyError("unknown feature identifier: missing"),
        lambda: selected_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "components", "missing", "desktop"],
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: missing is not a registered feature.\n"
        "Feature 'desktop':\n"
        "  firefox\n"
    )
    assert registry.get.call_count == 2


@pytest.mark.cli
def test_feature_components_requires_feature_name() -> None:
    """Verify that feature components requires a feature ID."""
    result = CliRunner().invoke(main, ["feature", "components"])

    assert result.exit_code == 2
    assert "Missing argument 'REGISTRY_IDS...'" in result.output
