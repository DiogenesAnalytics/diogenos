"""Test the Make component and its implementations."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.make.make import ArchMake
from diogenos.component.catalog.make.make import DebianMake
from diogenos.component.catalog.make.make import FedoraMake
from diogenos.component.catalog.make.make import MakePackage
from diogenos.component.catalog.make.make import UbuntuMake
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_make_package_has_registry_id() -> None:
    """Verify that the Make package has the expected registry ID."""
    assert MakePackage.registry_id == "make"


@pytest.mark.component
def test_make_package_is_satisfied_when_make_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Make is satisfied when make --version succeeds."""
    component = MakePackage(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["make", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_make_package_is_not_satisfied_when_make_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Make is not satisfied when make --version fails."""
    run_stub.returncode = 127
    component = MakePackage(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_make_package_returns_compatible_implementations(
    system: System,
) -> None:
    """Verify that the Make package exposes compatible implementations."""
    component = MakePackage()

    implementations = component.implementations()

    assert any(implementation.supports(system) for implementation in implementations)


@pytest.mark.component
def test_ubuntu_make_installs_make(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu Make installation runs the expected commands."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuMake(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "make"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_make_installs_make_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu Make installation uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuMake(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "apt-get", "update"],
            {"check": True},
        ),
        (
            ["sudo", "apt-get", "install", "-y", "make"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_make_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Make reports successful verification."""
    implementation = UbuntuMake(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["make", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_make_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Make reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuMake(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_make_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Make installation."""
    run_stub.returncode = 1
    implementation = UbuntuMake(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_make_installs_make(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Debian Make installation delegates to Ubuntu Make."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = DebianMake(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "make"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_make_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Make reports successful verification."""
    implementation = DebianMake(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["make", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_make_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Make reports failed verification."""
    run_stub.returncode = 127
    implementation = DebianMake(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_make_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Make installation on Debian."""
    run_stub.returncode = 1
    implementation = DebianMake(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_make_installs_make(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Fedora Make installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = FedoraMake(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "make"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_make_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Make reports successful verification."""
    implementation = FedoraMake(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["make", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_make_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Make reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraMake(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_fedora_make_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts Make installation."""
    run_stub.returncode = 1
    implementation = FedoraMake(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_make_installs_make(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Arch Make installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = ArchMake(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "make"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_make_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Make reports successful verification."""
    implementation = ArchMake(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["make", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_make_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Make reports failed verification."""
    run_stub.returncode = 127
    implementation = ArchMake(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_arch_make_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts Make installation."""
    run_stub.returncode = 1
    implementation = ArchMake(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
