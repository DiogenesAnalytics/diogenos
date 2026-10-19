"""Test the Tmux component and its implementations."""

import subprocess

import pytest

from diogenos.component.catalog.tmux.tmux import ArchTmux
from diogenos.component.catalog.tmux.tmux import DebianTmux
from diogenos.component.catalog.tmux.tmux import FedoraTmux
from diogenos.component.catalog.tmux.tmux import TmuxPackage
from diogenos.component.catalog.tmux.tmux import UbuntuTmux
from diogenos.system.base import System
from tests.feature.support import RunStub


@pytest.mark.component
@pytest.mark.feature
def test_tmux_package_is_satisfied_when_tmux_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Tmux is satisfied when tmux -V succeeds."""
    component = TmuxPackage(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["tmux", "-V"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_tmux_package_is_not_satisfied_when_tmux_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Tmux is not satisfied when tmux -V fails."""
    run_stub.returncode = 127
    component = TmuxPackage(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_tmux_package_returns_compatible_implementations(
    system: System,
) -> None:
    """Verify that the Tmux package exposes compatible implementations."""
    component = TmuxPackage()

    implementations = component.implementations()

    assert any(implementation.supports(system) for implementation in implementations)


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_tmux_installs_tmux(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Tmux installation runs the expected commands."""
    implementation = UbuntuTmux(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "tmux"],
            {"check": True},
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_tmux_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Tmux reports successful verification."""
    implementation = UbuntuTmux(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["tmux", "-V"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_tmux_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Tmux reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuTmux(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_tmux_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Tmux installation."""
    run_stub.returncode = 1
    implementation = UbuntuTmux(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
@pytest.mark.feature
def test_debian_tmux_installs_tmux(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Tmux installation runs the expected commands."""
    implementation = DebianTmux(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "tmux"],
            {"check": True},
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_debian_tmux_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Tmux reports successful verification."""
    implementation = DebianTmux(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["tmux", "-V"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_debian_tmux_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Tmux reports failed verification."""
    run_stub.returncode = 127
    implementation = DebianTmux(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_debian_tmux_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Tmux installation."""
    run_stub.returncode = 1
    implementation = DebianTmux(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
@pytest.mark.feature
def test_fedora_tmux_installs_tmux(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Tmux installation runs the expected command."""
    implementation = FedoraTmux(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "tmux"],
            {"check": True},
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_fedora_tmux_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Tmux reports successful verification."""
    implementation = FedoraTmux(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["tmux", "-V"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_fedora_tmux_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Tmux reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraTmux(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_fedora_tmux_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts Tmux installation."""
    run_stub.returncode = 1
    implementation = FedoraTmux(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
@pytest.mark.feature
def test_arch_tmux_installs_tmux(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Tmux installation runs the expected command."""
    implementation = ArchTmux(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "tmux"],
            {"check": True},
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_arch_tmux_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Tmux reports successful verification."""
    implementation = ArchTmux(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["tmux", "-V"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_arch_tmux_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Tmux reports failed verification."""
    run_stub.returncode = 127
    implementation = ArchTmux(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_arch_tmux_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts Tmux installation."""
    run_stub.returncode = 1
    implementation = ArchTmux(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
