"""Test the system update component and its implementations."""

import subprocess
from typing import Tuple
from typing import Type
from typing import Union

import pytest
from pytest import MonkeyPatch

from diogenos.component.internal.system_update import AlpineSystemUpdate
from diogenos.component.internal.system_update import ArchSystemUpdate
from diogenos.component.internal.system_update import DebianSystemUpdate
from diogenos.component.internal.system_update import FedoraSystemUpdate
from diogenos.component.internal.system_update import OpenSUSESystemUpdate
from diogenos.component.internal.system_update import SystemUpdate
from diogenos.component.internal.system_update import UbuntuSystemUpdate
from diogenos.system.base import System
from tests.component.support import RunStub


SystemUpdateImplementation = Union[
    DebianSystemUpdate,
    UbuntuSystemUpdate,
    FedoraSystemUpdate,
    ArchSystemUpdate,
]


@pytest.mark.component
def test_system_update_is_not_satisfied(system: System) -> None:
    """Verify that a system update is never considered satisfied."""
    component = SystemUpdate()

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_system_update_returns_implementations() -> None:
    """Verify that the system update exposes all supported implementations."""
    component = SystemUpdate()

    implementations = component.implementations()

    assert tuple(type(implementation) for implementation in implementations) == (
        DebianSystemUpdate,
        UbuntuSystemUpdate,
        FedoraSystemUpdate,
        ArchSystemUpdate,
        OpenSUSESystemUpdate,
        AlpineSystemUpdate,
    )


@pytest.mark.component
@pytest.mark.parametrize(
    ("implementation_class", "commands"),
    (
        (
            DebianSystemUpdate,
            (
                ("apt-get", "update"),
                ("apt-get", "upgrade", "-y"),
            ),
        ),
        (
            UbuntuSystemUpdate,
            (
                ("apt-get", "update"),
                ("apt-get", "upgrade", "-y"),
                ("snap", "refresh"),
            ),
        ),
        (
            FedoraSystemUpdate,
            (("dnf", "upgrade", "--refresh", "-y"),),
        ),
        (
            ArchSystemUpdate,
            (("pacman", "-Syu", "--noconfirm"),),
        ),
        (
            OpenSUSESystemUpdate,
            (
                ("zypper", "refresh"),
                ("zypper", "update", "-y"),
            ),
        ),
        (
            AlpineSystemUpdate,
            (
                ("apk", "update"),
                ("apk", "upgrade"),
            ),
        ),
    ),
)
def test_system_update_runs_commands(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
    implementation_class: Type[SystemUpdateImplementation],
    commands: Tuple[Tuple[str, ...], ...],
) -> None:
    """Verify that each implementation runs its expected update commands."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = implementation_class(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [(list(command), {"check": True}) for command in commands]


@pytest.mark.component
@pytest.mark.parametrize(
    ("implementation_class", "commands"),
    (
        (
            DebianSystemUpdate,
            (
                ("apt-get", "update"),
                ("apt-get", "upgrade", "-y"),
            ),
        ),
        (
            UbuntuSystemUpdate,
            (
                ("apt-get", "update"),
                ("apt-get", "upgrade", "-y"),
                ("snap", "refresh"),
            ),
        ),
        (
            FedoraSystemUpdate,
            (("dnf", "upgrade", "--refresh", "-y"),),
        ),
        (
            ArchSystemUpdate,
            (("pacman", "-Syu", "--noconfirm"),),
        ),
        (
            OpenSUSESystemUpdate,
            (
                ("zypper", "refresh"),
                ("zypper", "update", "-y"),
            ),
        ),
        (
            AlpineSystemUpdate,
            (
                ("apk", "update"),
                ("apk", "upgrade"),
            ),
        ),
    ),
)
def test_system_update_authenticates_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
    implementation_class: Type[SystemUpdateImplementation],
    commands: Tuple[Tuple[str, ...], ...],
) -> None:
    """Verify that each implementation authenticates once before updating."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = implementation_class(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (["sudo", "-v"], {"check": True}),
        *[(["sudo", *command], {"check": True}) for command in commands],
    ]


@pytest.mark.component
@pytest.mark.parametrize(
    "implementation_class",
    (
        DebianSystemUpdate,
        UbuntuSystemUpdate,
        FedoraSystemUpdate,
        ArchSystemUpdate,
        OpenSUSESystemUpdate,
        AlpineSystemUpdate,
    ),
)
def test_system_update_propagates_command_failure(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
    implementation_class: Type[SystemUpdateImplementation],
) -> None:
    """Verify that a failed update command interrupts the update sequence."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    run_stub.returncode = 1
    implementation = implementation_class(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert len(run_stub.calls) == 1


@pytest.mark.component
def test_system_update_propagates_sudo_authentication_failure(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that a sudo authentication failure interrupts the update."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    run_stub.returncode = 1
    implementation = UbuntuSystemUpdate(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "-v"],
            {"check": True},
        ),
    ]


@pytest.mark.component
@pytest.mark.parametrize(
    "implementation_class",
    (
        DebianSystemUpdate,
        UbuntuSystemUpdate,
        FedoraSystemUpdate,
        ArchSystemUpdate,
        OpenSUSESystemUpdate,
        AlpineSystemUpdate,
    ),
)
def test_system_update_verifies_successful_execution(
    system: System,
    run_stub: RunStub,
    implementation_class: Type[SystemUpdateImplementation],
) -> None:
    """Verify that the update implementation reports successful verification."""
    implementation = implementation_class(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == []
