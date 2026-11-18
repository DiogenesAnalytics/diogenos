"""Test the GNOME Overview keybindings component."""

import subprocess

import pytest

from diogenos.component.catalog.keyboard.gnome.overview_keybindings import (
    OVERVIEW_KEYBINDINGS,
)
from diogenos.component.catalog.keyboard.gnome.overview_keybindings import (
    GnomeOverviewKeybindings,
)
from diogenos.component.catalog.keyboard.gnome.overview_keybindings import (
    UbuntuGnomeOverviewKeybindings,
)
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gnome_overview_run_stub() -> RunStub:
    """Create a subprocess stub that reports the GNOME Overview keybindings."""
    return RunStub(
        outputs=[f"{value}\n" for _, _, value in OVERVIEW_KEYBINDINGS],
    )


@pytest.mark.component
def test_gnome_overview_keybindings_registry_id() -> None:
    """Test the GNOME Overview keybindings registry ID."""
    assert GnomeOverviewKeybindings.registry_id == "gnome_overview_keybindings"


@pytest.mark.component
def test_gnome_overview_keybindings_is_satisfied(
    system: System,
    gnome_overview_run_stub: RunStub,
) -> None:
    """Test that the GNOME Overview keybindings are satisfied when configured."""
    component = GnomeOverviewKeybindings(run=gnome_overview_run_stub)

    assert component.is_satisfied(system) is True
    assert gnome_overview_run_stub.calls == [
        (
            ["gsettings", "get", schema, key],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
        for schema, key, _ in OVERVIEW_KEYBINDINGS
    ]


@pytest.mark.component
def test_gnome_overview_keybindings_is_not_satisfied(
    system: System,
) -> None:
    """Test that the GNOME Overview keybindings are not satisfied when misconfigured."""
    run_stub = RunStub(outputs=["'incorrect'\n"])
    component = GnomeOverviewKeybindings(run=run_stub)

    assert component.is_satisfied(system) is False
    assert len(run_stub.calls) == 1


@pytest.mark.component
def test_gnome_overview_keybindings_implementations(
    system: System,
    gnome_overview_run_stub: RunStub,
) -> None:
    """Test that GNOME Overview keybindings provide an implementation for Ubuntu."""
    component = GnomeOverviewKeybindings(run=gnome_overview_run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_gnome_overview_keybindings_install(
    system: System,
    gnome_overview_run_stub: RunStub,
) -> None:
    """Test configuring GNOME Overview keybindings on Ubuntu."""
    implementation = UbuntuGnomeOverviewKeybindings(run=gnome_overview_run_stub)

    implementation.install(system)

    assert gnome_overview_run_stub.calls == [
        (
            ["gsettings", "set", schema, key, value],
            {"check": True},
        )
        for schema, key, value in OVERVIEW_KEYBINDINGS
    ]


@pytest.mark.component
def test_ubuntu_gnome_overview_keybindings_verify(
    system: System,
    gnome_overview_run_stub: RunStub,
) -> None:
    """Test verifying GNOME Overview keybindings on Ubuntu."""
    implementation = UbuntuGnomeOverviewKeybindings(run=gnome_overview_run_stub)

    assert implementation.verify(system) is True
    assert gnome_overview_run_stub.calls == [
        (
            ["gsettings", "get", schema, key],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
        for schema, key, _ in OVERVIEW_KEYBINDINGS
    ]


@pytest.mark.component
def test_ubuntu_gnome_overview_keybindings_verify_failure(
    system: System,
) -> None:
    """Test failed verification of GNOME Overview keybindings on Ubuntu."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuGnomeOverviewKeybindings(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gnome_overview_keybindings_install_failure(
    system: System,
) -> None:
    """Test that failed GNOME Overview keybindings installation raises an error."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuGnomeOverviewKeybindings(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert len(run_stub.calls) == 1
