"""Test the GNOME Super key component."""

import subprocess

import pytest

from diogenos.component.catalog.keyboard.gnome.super_key import SUPER_KEY_SETTINGS
from diogenos.component.catalog.keyboard.gnome.super_key import GnomeSuperKey
from diogenos.component.catalog.keyboard.gnome.super_key import UbuntuGnomeSuperKey
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gnome_super_key_run_stub() -> RunStub:
    """Create a subprocess stub that reports the GNOME Super key configuration."""
    return RunStub(
        outputs=[
            (value if value else "''") + "\n" for _, _, value in SUPER_KEY_SETTINGS
        ],
    )


@pytest.mark.component
def test_gnome_super_key_registry_id() -> None:
    """Test the GNOME Super key registry ID."""
    assert GnomeSuperKey.registry_id == "gnome_super_key"


@pytest.mark.component
def test_gnome_super_key_is_satisfied(
    system: System,
    gnome_super_key_run_stub: RunStub,
) -> None:
    """Test that the GNOME Super key configuration is satisfied."""
    component = GnomeSuperKey(run=gnome_super_key_run_stub)

    assert component.is_satisfied(system) is True
    assert gnome_super_key_run_stub.calls == [
        (
            ["gsettings", "get", schema, key],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
        for schema, key, _ in SUPER_KEY_SETTINGS
    ]


@pytest.mark.component
def test_gnome_super_key_is_not_satisfied(
    system: System,
) -> None:
    """Test that the GNOME Super key configuration is not satisfied."""
    run_stub = RunStub(outputs=["'Super_L'\n"])
    component = GnomeSuperKey(run=run_stub)

    assert component.is_satisfied(system) is False
    assert len(run_stub.calls) == 1


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
    """Test configuring the GNOME Super key behavior on Ubuntu."""
    implementation = UbuntuGnomeSuperKey(run=gnome_super_key_run_stub)

    implementation.install(system)

    assert gnome_super_key_run_stub.calls == [
        (
            ["gsettings", "set", schema, key, value],
            {"check": True},
        )
        for schema, key, value in SUPER_KEY_SETTINGS
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
            ["gsettings", "get", schema, key],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
        for schema, key, _ in SUPER_KEY_SETTINGS
    ]


@pytest.mark.component
def test_ubuntu_gnome_super_key_verify_failure(
    system: System,
) -> None:
    """Test failed verification of the GNOME Super key configuration."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuGnomeSuperKey(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gnome_super_key_install_failure(
    system: System,
) -> None:
    """Test that failed GNOME Super key installation raises an error."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuGnomeSuperKey(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert len(run_stub.calls) == 1
