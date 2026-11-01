"""Test the Keyd component."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.keyboard.keyd import KEYD_PPA
from diogenos.component.catalog.keyboard.keyd import Keyd
from diogenos.component.catalog.keyboard.keyd import UbuntuKeyd
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_keyd_registry_id() -> None:
    """Test the Keyd registry ID."""
    assert Keyd.registry_id == "keyd"


@pytest.mark.component
def test_keyd_is_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that Keyd is satisfied when its service is enabled and active."""
    component = Keyd(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["systemctl", "is-enabled", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
        (
            ["systemctl", "is-active", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_keyd_is_not_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that Keyd is not satisfied when its service is unavailable."""
    run_stub.returncode = 1
    component = Keyd(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_keyd_implementations(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that Keyd provides an implementation for Ubuntu."""
    component = Keyd(run=run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_keyd_install(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test installing Keyd on Ubuntu."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuKeyd(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "software-properties-common"],
            {"check": True},
        ),
        (
            ["add-apt-repository", "-y", KEYD_PPA],
            {"check": True},
        ),
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "keyd"],
            {"check": True},
        ),
        (
            ["systemctl", "enable", "--now", "keyd"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_keyd_install_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that Keyd installation uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuKeyd(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "apt-get", "update"],
            {"check": True},
        ),
        (
            [
                "sudo",
                "apt-get",
                "install",
                "-y",
                "software-properties-common",
            ],
            {"check": True},
        ),
        (
            ["sudo", "add-apt-repository", "-y", KEYD_PPA],
            {"check": True},
        ),
        (
            ["sudo", "apt-get", "update"],
            {"check": True},
        ),
        (
            ["sudo", "apt-get", "install", "-y", "keyd"],
            {"check": True},
        ),
        (
            ["sudo", "systemctl", "enable", "--now", "keyd"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_keyd_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test verifying Keyd on Ubuntu."""
    implementation = UbuntuKeyd(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["systemctl", "is-enabled", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
        (
            ["systemctl", "is-active", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_keyd_verify_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test failed verification of Keyd on Ubuntu."""
    run_stub.returncode = 1
    implementation = UbuntuKeyd(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_keyd_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that a failed Keyd installation command raises an error."""
    run_stub.returncode = 1
    implementation = UbuntuKeyd(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
