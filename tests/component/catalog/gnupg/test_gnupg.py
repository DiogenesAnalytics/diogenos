"""Test the GnuPG component and its implementations."""

import subprocess

import pytest

from diogenos.component import ComponentImplementation
from diogenos.component.catalog.gnupg.gnupg import ArchGnuPG
from diogenos.component.catalog.gnupg.gnupg import DebianGnuPG
from diogenos.component.catalog.gnupg.gnupg import FedoraGnuPG
from diogenos.component.catalog.gnupg.gnupg import GnuPGPackage
from diogenos.component.catalog.gnupg.gnupg import UbuntuGnuPG
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_gnupg_package_registry_id() -> None:
    """Verify that the GnuPG package has the expected registry identifier."""
    assert GnuPGPackage.registry_id == "gnupg"


@pytest.mark.component
def test_gnupg_package_is_satisfied_when_gpg_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that GnuPG is satisfied when gpg --version succeeds."""
    component = GnuPGPackage(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["gpg", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_gnupg_package_is_not_satisfied_when_gpg_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that GnuPG is not satisfied when gpg --version fails."""
    run_stub.returncode = 127
    component = GnuPGPackage(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gnupg_package_returns_compatible_implementations(
    system: System,
) -> None:
    """Verify that GnuPG exposes implementations for supported distributions."""
    component = GnuPGPackage()

    implementations = component.implementations()

    assert len(implementations) == 4
    assert isinstance(implementations[0], UbuntuGnuPG)
    assert isinstance(implementations[1], DebianGnuPG)
    assert isinstance(implementations[2], FedoraGnuPG)
    assert isinstance(implementations[3], ArchGnuPG)
    assert all(
        isinstance(implementation, ComponentImplementation)
        for implementation in implementations
    )
    assert any(implementation.supports(system) for implementation in implementations)


@pytest.mark.component
def test_ubuntu_gnupg_installs_gnupg(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu GnuPG installation runs the expected commands."""
    implementation = UbuntuGnuPG(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "gnupg"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_gnupg_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu GnuPG reports successful verification."""
    implementation = UbuntuGnuPG(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gpg", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gnupg_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu GnuPG reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuGnuPG(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gnupg_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts GnuPG installation."""
    run_stub.returncode = 1
    implementation = UbuntuGnuPG(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_gnupg_installs_gnupg(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian GnuPG installation runs the expected commands."""
    implementation = DebianGnuPG(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "gnupg"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_gnupg_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian GnuPG reports successful verification."""
    implementation = DebianGnuPG(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gpg", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_gnupg_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian GnuPG reports failed verification."""
    run_stub.returncode = 127
    implementation = DebianGnuPG(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_gnupg_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts GnuPG installation."""
    run_stub.returncode = 1
    implementation = DebianGnuPG(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_gnupg_installs_gnupg(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora GnuPG installation runs the expected command."""
    implementation = FedoraGnuPG(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "gnupg2"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_gnupg_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora GnuPG reports successful verification."""
    implementation = FedoraGnuPG(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gpg", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_gnupg_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora GnuPG reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraGnuPG(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_fedora_gnupg_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts GnuPG installation."""
    run_stub.returncode = 1
    implementation = FedoraGnuPG(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_gnupg_installs_gnupg(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch GnuPG installation runs the expected command."""
    implementation = ArchGnuPG(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "gnupg"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_gnupg_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch GnuPG reports successful verification."""
    implementation = ArchGnuPG(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gpg", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_gnupg_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch GnuPG reports failed verification."""
    run_stub.returncode = 127
    implementation = ArchGnuPG(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_arch_gnupg_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts GnuPG installation."""
    run_stub.returncode = 1
    implementation = ArchGnuPG(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
