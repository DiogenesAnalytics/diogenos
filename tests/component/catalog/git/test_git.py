"""Test the Git component and its implementations."""

import subprocess

import pytest

from diogenos.component.catalog.git.git import ArchGit
from diogenos.component.catalog.git.git import DebianGit
from diogenos.component.catalog.git.git import FedoraGit
from diogenos.component.catalog.git.git import GitComponent
from diogenos.component.catalog.git.git import UbuntuGit
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_git_component_is_satisfied_when_git_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Git is satisfied when git --version succeeds."""
    component = GitComponent(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_git_component_is_not_satisfied_when_git_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Git is not satisfied when git --version fails."""
    run_stub.returncode = 127
    component = GitComponent(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_git_component_returns_implementations(
    system: System,
) -> None:
    """Verify that the Git component exposes compatible implementations."""
    component = GitComponent()

    implementations = component.implementations()

    assert any(implementation.supports(system) for implementation in implementations)


@pytest.mark.component
def test_ubuntu_git_installs_git(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Git installation runs the expected commands."""
    implementation = UbuntuGit(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "git"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_git_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Git reports successful verification."""
    implementation = UbuntuGit(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_git_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Git reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuGit(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_git_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Git installation."""
    run_stub.returncode = 1
    implementation = UbuntuGit(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_git_installs_git(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Git installation runs the expected command."""
    implementation = FedoraGit(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "git"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_git_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Git reports successful verification."""
    implementation = FedoraGit(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_git_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Git reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraGit(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_fedora_git_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts Git installation."""
    run_stub.returncode = 1
    implementation = FedoraGit(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_git_installs_git(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Git installation runs the expected commands."""
    implementation = DebianGit(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "git"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_git_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Git installation succeeds when git --version succeeds."""
    implementation = DebianGit(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_git_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Git installation fails when git --version fails."""
    run_stub.returncode = 127
    implementation = DebianGit(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_git_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Git installation."""
    run_stub.returncode = 1
    implementation = DebianGit(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_git_installs_git(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Git installation runs the expected command."""
    implementation = ArchGit(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "git"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_git_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Git installation succeeds when git --version succeeds."""
    implementation = ArchGit(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_git_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Git installation fails when git --version fails."""
    run_stub.returncode = 127
    implementation = ArchGit(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_arch_git_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts Git installation."""
    run_stub.returncode = 1
    implementation = ArchGit(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
