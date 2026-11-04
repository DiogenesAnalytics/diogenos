"""Test the GNOME Terminal component."""

import subprocess
from typing import Callable
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from diogenos.component import ComponentImplementation
from diogenos.component.catalog.terminal.gnome_terminal import ArchGnomeTerminal
from diogenos.component.catalog.terminal.gnome_terminal import DebianGnomeTerminal
from diogenos.component.catalog.terminal.gnome_terminal import FedoraGnomeTerminal
from diogenos.component.catalog.terminal.gnome_terminal import GnomeTerminalPackage
from diogenos.component.catalog.terminal.gnome_terminal import UbuntuGnomeTerminal
from diogenos.system.base import System


@pytest.fixture
def run() -> Mock:
    """Provide a mocked subprocess runner."""
    return Mock(
        return_value=subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="GNOME Terminal version",
            stderr="",
        ),
    )


@pytest.fixture
def system() -> System:
    """Provide a mocked system."""
    return Mock(spec=System)


def ubuntu_gnome_terminal(run: Mock) -> ComponentImplementation:
    """Create the Ubuntu GNOME Terminal implementation."""
    return UbuntuGnomeTerminal(run=run)


def fedora_gnome_terminal(run: Mock) -> ComponentImplementation:
    """Create the Fedora GNOME Terminal implementation."""
    return FedoraGnomeTerminal(run=run)


def arch_gnome_terminal(run: Mock) -> ComponentImplementation:
    """Create the Arch GNOME Terminal implementation."""
    return ArchGnomeTerminal(run=run)


@pytest.mark.component
def test_gnome_terminal_package_registry_id() -> None:
    """Test the GNOME Terminal component registry identifier."""
    assert GnomeTerminalPackage.registry_id == "gnome_terminal"


@pytest.mark.component
def test_gnome_terminal_package_is_satisfied(
    run: Mock,
    system: System,
) -> None:
    """Test that GNOME Terminal is satisfied when its executable succeeds."""
    component = GnomeTerminalPackage(run=run)

    assert component.is_satisfied(system)

    run.assert_called_once_with(
        ["gnome-terminal", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )


@pytest.mark.component
def test_gnome_terminal_package_is_not_satisfied(
    run: Mock,
    system: System,
) -> None:
    """Test that GNOME Terminal is not satisfied when its executable fails."""
    run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="not found",
    )
    component = GnomeTerminalPackage(run=run)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_gnome_terminal_package_implementations(run: Mock) -> None:
    """Test the implementations exposed by the GNOME Terminal component."""
    implementations = GnomeTerminalPackage(run=run).implementations()

    assert len(implementations) == 4
    assert isinstance(implementations[0], UbuntuGnomeTerminal)
    assert isinstance(implementations[1], DebianGnomeTerminal)
    assert isinstance(implementations[2], FedoraGnomeTerminal)
    assert isinstance(implementations[3], ArchGnomeTerminal)
    assert all(
        isinstance(implementation, ComponentImplementation)
        for implementation in implementations
    )


@pytest.mark.parametrize(
    ("implementation", "expected_commands"),
    [
        (
            ubuntu_gnome_terminal,
            [
                ["apt-get", "update"],
                ["apt-get", "install", "-y", "gnome-terminal"],
            ],
        ),
        (
            fedora_gnome_terminal,
            [
                ["dnf", "install", "-y", "gnome-terminal"],
            ],
        ),
        (
            arch_gnome_terminal,
            [
                ["pacman", "-S", "--noconfirm", "gnome-terminal"],
            ],
        ),
    ],
)
@pytest.mark.parametrize("user_id", [0, 1000])
@pytest.mark.component
def test_gnome_terminal_install(
    monkeypatch: MonkeyPatch,
    run: Mock,
    system: System,
    implementation: Callable[[Mock], ComponentImplementation],
    expected_commands: list[list[str]],
    user_id: int,
) -> None:
    """Test installing GNOME Terminal with and without sudo."""
    monkeypatch.setattr("os.geteuid", lambda: user_id)

    component = implementation(run)
    component.install(system)

    prefix = ["sudo"] if user_id != 0 else []

    assert [call.args[0] for call in run.call_args_list] == [
        prefix + command for command in expected_commands
    ]

    assert all(call.kwargs == {"check": True} for call in run.call_args_list)


@pytest.mark.parametrize(
    "implementation",
    [
        ubuntu_gnome_terminal,
        fedora_gnome_terminal,
        arch_gnome_terminal,
    ],
)
@pytest.mark.component
def test_gnome_terminal_verify(
    run: Mock,
    system: System,
    implementation: Callable[[Mock], ComponentImplementation],
) -> None:
    """Test successful verification of GNOME Terminal."""
    component = implementation(run)

    assert component.verify(system)

    run.assert_called_once_with(
        ["gnome-terminal", "--version"],
        capture_output=True,
        check=False,
        text=True,
    )


@pytest.mark.parametrize(
    "implementation",
    [
        ubuntu_gnome_terminal,
        fedora_gnome_terminal,
        arch_gnome_terminal,
    ],
)
def test_gnome_terminal_verify_failure(
    run: Mock,
    system: System,
    implementation: Callable[[Mock], ComponentImplementation],
) -> None:
    """Test unsuccessful verification of GNOME Terminal."""
    run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="error",
    )
    component = implementation(run)

    assert not component.verify(system)


def test_debian_gnome_terminal_install(
    run: Mock,
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that the Debian implementation delegates installation."""
    install = Mock()
    monkeypatch.setattr(UbuntuGnomeTerminal, "install", install)

    component = DebianGnomeTerminal(run=run)
    component.install(system)

    install.assert_called_once_with(system)


def test_debian_gnome_terminal_verify(
    run: Mock,
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that the Debian implementation delegates verification."""
    verify = Mock(return_value=True)
    monkeypatch.setattr(UbuntuGnomeTerminal, "verify", verify)

    component = DebianGnomeTerminal(run=run)

    assert component.verify(system)

    verify.assert_called_once_with(system)
