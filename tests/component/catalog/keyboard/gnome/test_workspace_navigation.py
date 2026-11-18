"""Test the GNOME workspace navigation component."""

import subprocess

import pytest

from diogenos.component.catalog.keyboard.gnome.workspace_navigation import (
    WORKSPACE_KEYBINDINGS,
)
from diogenos.component.catalog.keyboard.gnome.workspace_navigation import (
    GnomeWorkspaceNavigation,
)
from diogenos.component.catalog.keyboard.gnome.workspace_navigation import (
    UbuntuGnomeWorkspaceNavigation,
)
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gnome_workspace_run_stub() -> RunStub:
    """Create a subprocess stub that reports the GNOME workspace keybindings."""
    return RunStub(
        outputs=[f"{value}\n" for _, _, value in WORKSPACE_KEYBINDINGS],
    )


@pytest.mark.component
def test_gnome_workspace_navigation_registry_id() -> None:
    """Test the GNOME workspace navigation registry ID."""
    assert GnomeWorkspaceNavigation.registry_id == "gnome_workspace_navigation"


@pytest.mark.component
def test_gnome_workspace_navigation_is_satisfied(
    system: System,
    gnome_workspace_run_stub: RunStub,
) -> None:
    """Test that GNOME workspace navigation is satisfied when configured."""
    component = GnomeWorkspaceNavigation(run=gnome_workspace_run_stub)

    assert component.is_satisfied(system) is True
    assert gnome_workspace_run_stub.calls == [
        (
            ["gsettings", "get", schema, key],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
        for schema, key, _ in WORKSPACE_KEYBINDINGS
    ]


@pytest.mark.component
def test_gnome_workspace_navigation_is_not_satisfied(
    system: System,
) -> None:
    """Test that GNOME workspace navigation is not satisfied when misconfigured."""
    run_stub = RunStub(outputs=["'incorrect'\n"])
    component = GnomeWorkspaceNavigation(run=run_stub)

    assert component.is_satisfied(system) is False
    assert len(run_stub.calls) == 1


@pytest.mark.component
def test_gnome_workspace_navigation_implementations(
    system: System,
    gnome_workspace_run_stub: RunStub,
) -> None:
    """Test that GNOME workspace navigation provides an implementation for Ubuntu."""
    component = GnomeWorkspaceNavigation(run=gnome_workspace_run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_gnome_workspace_navigation_install(
    system: System,
    gnome_workspace_run_stub: RunStub,
) -> None:
    """Test configuring GNOME workspace navigation on Ubuntu."""
    implementation = UbuntuGnomeWorkspaceNavigation(run=gnome_workspace_run_stub)

    implementation.install(system)

    assert gnome_workspace_run_stub.calls == [
        (
            ["gsettings", "set", schema, key, value],
            {"check": True},
        )
        for schema, key, value in WORKSPACE_KEYBINDINGS
    ]


@pytest.mark.component
def test_ubuntu_gnome_workspace_navigation_verify(
    system: System,
    gnome_workspace_run_stub: RunStub,
) -> None:
    """Test verifying GNOME workspace navigation on Ubuntu."""
    implementation = UbuntuGnomeWorkspaceNavigation(run=gnome_workspace_run_stub)

    assert implementation.verify(system) is True
    assert gnome_workspace_run_stub.calls == [
        (
            ["gsettings", "get", schema, key],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
        for schema, key, _ in WORKSPACE_KEYBINDINGS
    ]


@pytest.mark.component
def test_ubuntu_gnome_workspace_navigation_verify_failure(
    system: System,
) -> None:
    """Test failed verification of GNOME workspace navigation on Ubuntu."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuGnomeWorkspaceNavigation(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gnome_workspace_navigation_install_failure(
    system: System,
) -> None:
    """Test that failed GNOME workspace navigation installation raises an error."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuGnomeWorkspaceNavigation(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert len(run_stub.calls) == 1
