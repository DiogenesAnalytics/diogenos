"""Test the GCC component and its implementations."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.build.gcc import ArchGCC
from diogenos.component.catalog.build.gcc import DebianGCC
from diogenos.component.catalog.build.gcc import FedoraGCC
from diogenos.component.catalog.build.gcc import GCC
from diogenos.component.catalog.build.gcc import UbuntuGCC
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_gcc_has_registry_id() -> None:
    """Verify that GCC has the expected registry ID."""
    assert GCC.registry_id == "gcc"


@pytest.mark.component
def test_gcc_is_satisfied_when_gcc_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that GCC is satisfied when gcc --version succeeds."""
    component = GCC(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["gcc", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_gcc_is_not_satisfied_when_gcc_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that GCC is not satisfied when gcc --version fails."""
    run_stub.returncode = 127
    component = GCC(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gcc_returns_compatible_implementations(
    system: System,
) -> None:
    """Verify that GCC exposes compatible implementations."""
    component = GCC()

    implementations = component.implementations()

    assert any(
        implementation.supports(system)
        for implementation in implementations
    )


@pytest.mark.component
def test_ubuntu_gcc_installs_gcc(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu GCC installation runs the expected commands."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuGCC(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "gcc"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_gcc_installs_gcc_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu GCC uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuGCC(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "apt-get", "update"],
            {"check": True},
        ),
        (
            ["sudo", "apt-get", "install", "-y", "gcc"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_gcc_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu GCC reports successful verification."""
    implementation = UbuntuGCC(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gcc", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gcc_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu GCC reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuGCC(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gcc_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts GCC installation."""
    run_stub.returncode = 1
    implementation = UbuntuGCC(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_gcc_installs_gcc(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Debian GCC installs its package using APT."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = DebianGCC(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "gcc"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_gcc_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian GCC reports successful verification."""
    implementation = DebianGCC(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gcc", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_gcc_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian GCC reports failed verification."""
    run_stub.returncode = 127
    implementation = DebianGCC(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_gcc_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts GCC installation on Debian."""
    run_stub.returncode = 1
    implementation = DebianGCC(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_gcc_installs_gcc(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Fedora GCC installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = FedoraGCC(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "gcc"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_gcc_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora GCC reports successful verification."""
    implementation = FedoraGCC(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gcc", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_gcc_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora GCC reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraGCC(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_fedora_gcc_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts GCC installation."""
    run_stub.returncode = 1
    implementation = FedoraGCC(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_gcc_installs_gcc(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Arch GCC installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = ArchGCC(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "gcc"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_gcc_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch GCC reports successful verification."""
    implementation = ArchGCC(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gcc", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_gcc_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch GCC reports failed verification."""
    run_stub.returncode = 127
    implementation = ArchGCC(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_arch_gcc_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts GCC installation."""
    run_stub.returncode = 1
    implementation = ArchGCC(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
