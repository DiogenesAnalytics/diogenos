"""Test the GNOME Super key component."""

import subprocess

import pytest

from diogenos.component.catalog.keyboard.gnome.super_key import MUTTER_SCHEMA
from diogenos.component.catalog.keyboard.gnome.super_key import OVERLAY_KEY
from diogenos.component.catalog.keyboard.gnome.super_key import OVERLAY_KEY_VALUE
from diogenos.component.catalog.keyboard.gnome.super_key import GnomeSuperKey
from diogenos.component.catalog.keyboard.gnome.super_key import UbuntuGnomeSuperKey
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gnome_super_key_run_stub(run_stub: RunStub) -> RunStub:
    """Create a subprocess stub that reports the standalone Super key as disabled."""
    run_stub.stdout = "''\n"
    return run_stub


@pytest.mark.component
def test_gnome_super_key_registry_id() -> None:
    """Test the GNOME Super key registry ID."""
    assert GnomeSuperKey.registry_id == "gnome_super_key"


@pytest.mark.component
def test_gnome_super_key_is_satisfied(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test that the GNOME Super key is satisfied when disabled."""
    component = GnomeSuperKey(run=gnome_super_key_run_stub)

    assert component.is_satisfied(system) is True
    assert gnome_super_key_run_stub.calls == [
        (
            ["gsettings", "get", MUTTER_SCHEMA, OVERLAY_KEY],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_gnome_super_key_is_not_satisfied(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test that the GNOME Super key is not satisfied when enabled."""
    gnome_super_key_run_stub.stdout = "'Super_L'\n"
    component = GnomeSuperKey(run=gnome_super_key_run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gnome_super_key_implementations(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test that the GNOME Super key provides an implementation for Ubuntu."""
    component = GnomeSuperKey(run=gnome_super_key_run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_gnome_super_key_install(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test disabling the standalone Super key behavior on Ubuntu."""
    implementation = UbuntuGnomeSuperKey(run=gnome_super_key_run_stub)

    implementation.install(system)

    assert gnome_super_key_run_stub.calls == [
        (
            [
                "gsettings",
                "set",
                MUTTER_SCHEMA,
                OVERLAY_KEY,
                OVERLAY_KEY_VALUE,
            ],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_gnome_super_key_verify(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test verifying the GNOME Super key configuration on Ubuntu."""
    implementation = UbuntuGnomeSuperKey(run=gnome_super_key_run_stub)

    assert implementation.verify(system) is True
    assert gnome_super_key_run_stub.calls == [
        (
            ["gsettings", "get", MUTTER_SCHEMA, OVERLAY_KEY],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gnome_super_key_verify_failure(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test failed verification of the GNOME Super key configuration."""
    gnome_super_key_run_stub.returncode = 1
    implementation = UbuntuGnomeSuperKey(run=gnome_super_key_run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gnome_super_key_install_failure(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test that a failed GNOME Super key installation raises an error."""
    gnome_super_key_run_stub.returncode = 1
    implementation = UbuntuGnomeSuperKey(run=gnome_super_key_run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
