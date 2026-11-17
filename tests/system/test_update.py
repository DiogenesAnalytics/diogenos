"""Test system update operations."""

from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from diogenos.component.internal.system_update import SystemUpdate
from diogenos.system.base import System
from diogenos.system.update import SystemUpdater


@pytest.mark.system
def test_system_updater_resolves_implementation(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that the system updater resolves an implementation."""
    implementation = Mock()
    resolver = Mock()
    resolver.resolve.return_value = implementation

    monkeypatch.setattr(
        "diogenos.system.update.ImplementationResolver",
        lambda: resolver,
    )

    updater = SystemUpdater()
    updater.update(system)

    component = resolver.resolve.call_args.args[0]

    assert isinstance(component, SystemUpdate)
    resolver.resolve.assert_called_once_with(component, system)


@pytest.mark.system
def test_system_updater_installs_resolved_implementation(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that the system updater installs the resolved implementation."""
    implementation = Mock()
    resolver = Mock()
    resolver.resolve.return_value = implementation

    monkeypatch.setattr(
        "diogenos.system.update.ImplementationResolver",
        lambda: resolver,
    )

    updater = SystemUpdater()
    updater.update(system)

    implementation.install.assert_called_once_with(system)


@pytest.mark.system
def test_system_updater_propagates_resolution_failure(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that the system updater propagates resolution failures."""
    resolver = Mock()
    resolver.resolve.side_effect = ValueError("No implementation found")

    monkeypatch.setattr(
        "diogenos.system.update.ImplementationResolver",
        lambda: resolver,
    )

    updater = SystemUpdater()

    with pytest.raises(ValueError, match="No implementation found"):
        updater.update(system)
