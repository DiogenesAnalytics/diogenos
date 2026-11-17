"""Define the system update component."""

import os
import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component.base import Component
from diogenos.component.implementation.base import ComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.linux import AlpineComponentImplementation
from diogenos.component.implementation.linux import ArchComponentImplementation
from diogenos.component.implementation.linux import DebianComponentImplementation
from diogenos.component.implementation.linux import FedoraComponentImplementation
from diogenos.component.implementation.linux import OpenSUSEComponentImplementation
from diogenos.component.implementation.linux import UbuntuComponentImplementation
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


class _SystemUpdateMixin:
    """Provide shared system update behavior."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the implementation."""
        self._run = run

    def _run_commands(self, commands: Tuple[Tuple[str, ...], ...]) -> None:
        """Authenticate and execute system update commands."""
        if os.geteuid() != 0:
            self._run(["sudo", "-v"], check=True)

        for command in commands:
            self._run(
                prepare_command(command, privileged=True),
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify the system update implementation."""
        return True


class DebianSystemUpdate(
    _SystemUpdateMixin,
    DebianComponentImplementation,
):
    """Define the Debian system update implementation."""

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Update Debian packages."""
        self._run_commands(
            (
                ("apt-get", "update"),
                ("apt-get", "upgrade", "-y"),
            )
        )


class UbuntuSystemUpdate(
    _SystemUpdateMixin,
    UbuntuComponentImplementation,
):
    """Define the Ubuntu system update implementation."""

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Update Ubuntu packages."""
        self._run_commands(
            (
                ("apt-get", "update"),
                ("apt-get", "upgrade", "-y"),
                ("snap", "refresh"),
            )
        )


class FedoraSystemUpdate(
    _SystemUpdateMixin,
    FedoraComponentImplementation,
):
    """Define the Fedora system update implementation."""

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Update Fedora packages."""
        self._run_commands((("dnf", "upgrade", "--refresh", "-y"),))


class ArchSystemUpdate(
    _SystemUpdateMixin,
    ArchComponentImplementation,
):
    """Define the Arch Linux system update implementation."""

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Update Arch Linux packages."""
        self._run_commands((("pacman", "-Syu", "--noconfirm"),))


class OpenSUSESystemUpdate(
    _SystemUpdateMixin,
    OpenSUSEComponentImplementation,
):
    """Define the openSUSE system update implementation."""

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Update openSUSE packages."""
        self._run_commands(
            (
                ("zypper", "refresh"),
                ("zypper", "update", "-y"),
            )
        )


class AlpineSystemUpdate(
    _SystemUpdateMixin,
    AlpineComponentImplementation,
):
    """Define the Alpine Linux system update implementation."""

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Update Alpine Linux packages."""
        self._run_commands(
            (
                ("apk", "update"),
                ("apk", "upgrade"),
            )
        )


class SystemUpdate(Component):
    """Represent an operating system update."""

    def is_satisfied(self, system: System) -> bool:
        """Return whether the update is satisfied."""
        return False

    def implementations(self) -> Tuple[ComponentImplementation, ...]:
        """Return supported operating system implementations."""
        return (
            DebianSystemUpdate(),
            UbuntuSystemUpdate(),
            FedoraSystemUpdate(),
            ArchSystemUpdate(),
            OpenSUSESystemUpdate(),
            AlpineSystemUpdate(),
        )
