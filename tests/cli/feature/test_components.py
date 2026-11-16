"""Test the feature components command."""

from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from diogenos.cli import main
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


@pytest.mark.cli
def test_feature_components(
    registry: Mock,
    detector: Mock,
    system: System,
) -> None:
    """Verify that the feature components command lists install methods."""
    apt_implementation = Mock()
    apt_implementation.supports.return_value = True
    apt_implementation.install_methods = (InstallMethodType.APT,)

    snap_implementation = Mock()
    snap_implementation.supports.return_value = True
    snap_implementation.install_methods = (InstallMethodType.SNAP,)

    config_implementation = Mock()
    config_implementation.supports.return_value = True
    config_implementation.install_methods = ()

    selected_feature = Mock()
    selected_feature.resolved_components = (
        Mock(
            registry_id="docker.engine",
            implementations=Mock(return_value=(apt_implementation,)),
        ),
        Mock(
            registry_id="firefox",
            implementations=Mock(return_value=(snap_implementation,)),
        ),
        Mock(
            registry_id="docker.config.user",
            implementations=Mock(return_value=(config_implementation,)),
        ),
    )
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(
        main,
        ["feature", "components", "desktop"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Feature 'desktop'\n"
        "\n"
        "  Component           Install methods\n"
        "  ------------------  ---------------\n"
        "  docker.engine       apt\n"
        "  firefox             snap\n"
        "  docker.config.user  Not applicable\n"
        "\n"
    )
    registry.get.assert_called_once_with("desktop")
    detector.detect.assert_called_once_with()

    apt_implementation.supports.assert_called_once_with(system)
    snap_implementation.supports.assert_called_once_with(system)
    config_implementation.supports.assert_called_once_with(system)


@pytest.mark.cli
def test_feature_components_multiple_install_methods(
    registry: Mock,
    detector: Mock,
) -> None:
    """Verify that all supported installation methods are listed."""
    implementation = Mock()
    implementation.supports.return_value = True
    implementation.install_methods = (
        InstallMethodType.APT,
        InstallMethodType.SNAP,
    )

    selected_feature = Mock()
    selected_feature.resolved_components = (
        Mock(
            registry_id="browser",
            implementations=Mock(return_value=(implementation,)),
        ),
    )
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(
        main,
        ["feature", "components", "desktop"],
    )

    assert result.exit_code == 0
    assert "  browser    apt, snap\n" in result.output


@pytest.mark.cli
def test_feature_components_unsupported(
    registry: Mock,
    detector: Mock,
) -> None:
    """Verify that unsupported components are identified."""
    implementation = Mock()
    implementation.supports.return_value = False

    selected_feature = Mock()
    selected_feature.resolved_components = (
        Mock(
            registry_id="docker.engine",
            implementations=Mock(return_value=(implementation,)),
        ),
    )
    registry.get.return_value = lambda: selected_feature

    result = CliRunner().invoke(
        main,
        ["feature", "components", "docker"],
    )

    assert result.exit_code == 0
    assert "  docker.engine  Not supported\n" in result.output
    implementation.supports.assert_called_once()


@pytest.mark.cli
def test_feature_components_multiple_features(
    registry: Mock,
    detector: Mock,
) -> None:
    """Verify that components from multiple features are listed."""
    first_implementation = Mock()
    first_implementation.supports.return_value = True
    first_implementation.install_methods = (InstallMethodType.SNAP,)

    second_implementation = Mock()
    second_implementation.supports.return_value = True
    second_implementation.install_methods = (InstallMethodType.APT,)

    first_feature = Mock()
    first_feature.resolved_components = (
        Mock(
            registry_id="firefox",
            implementations=Mock(return_value=(first_implementation,)),
        ),
    )

    second_feature = Mock()
    second_feature.resolved_components = (
        Mock(
            registry_id="docker.engine",
            implementations=Mock(return_value=(second_implementation,)),
        ),
    )

    registry.get.side_effect = [
        lambda: first_feature,
        lambda: second_feature,
    ]

    result = CliRunner().invoke(
        main,
        ["feature", "components", "desktop", "docker"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Feature 'desktop'\n"
        "\n"
        "  Component  Install methods\n"
        "  ---------  ---------------\n"
        "  firefox    snap\n"
        "\n"
        "Feature 'docker'\n"
        "\n"
        "  Component      Install methods\n"
        "  -------------  ---------------\n"
        "  docker.engine  apt\n"
        "\n"
    )
    registry.get.assert_any_call("desktop")
    registry.get.assert_any_call("docker")


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
    detector: Mock,
) -> None:
    """Verify that component listing continues after an unknown feature."""
    implementation = Mock()
    implementation.supports.return_value = True
    implementation.install_methods = (InstallMethodType.SNAP,)

    selected_feature = Mock()
    selected_feature.resolved_components = (
        Mock(
            registry_id="firefox",
            implementations=Mock(return_value=(implementation,)),
        ),
    )

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
        "Feature 'desktop'\n"
        "\n"
        "  Component  Install methods\n"
        "  ---------  ---------------\n"
        "  firefox    snap\n"
        "\n"
    )
    assert registry.get.call_count == 2


@pytest.mark.cli
def test_feature_components_requires_feature_name() -> None:
    """Verify that feature components requires a feature ID."""
    result = CliRunner().invoke(main, ["feature", "components"])

    assert result.exit_code == 2
    assert "Missing argument 'REGISTRY_IDS...'" in result.output
