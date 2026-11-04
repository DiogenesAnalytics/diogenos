"""Define the GNOME Terminal component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.validation import validate_command
from diogenos.system.base import System


class UbuntuGnomeTerminal(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of GNOME Terminal."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GNOME Terminal implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GNOME Terminal on Ubuntu."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", "gnome-terminal"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GNOME Terminal is available."""
        return validate_command(self._run, ["gnome-terminal", "--version"])


class DebianGnomeTerminal(DebianComponentImplementation):
    """Define the Debian implementation of GNOME Terminal."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian GNOME Terminal implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GNOME Terminal on Debian."""
        UbuntuGnomeTerminal(run=self._run).install(system)

    def verify(self, system: System) -> bool:
        """Verify that GNOME Terminal is available."""
        return UbuntuGnomeTerminal(run=self._run).verify(system)


class FedoraGnomeTerminal(FedoraComponentImplementation):
    """Define the Fedora implementation of GNOME Terminal."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora GNOME Terminal implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GNOME Terminal on Fedora."""
        self._run(
            prepare_command(
                ["dnf", "install", "-y", "gnome-terminal"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GNOME Terminal is available."""
        return validate_command(self._run, ["gnome-terminal", "--version"])


class ArchGnomeTerminal(ArchComponentImplementation):
    """Define the Arch implementation of GNOME Terminal."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch GNOME Terminal implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GNOME Terminal on Arch."""
        self._run(
            prepare_command(
                ["pacman", "-S", "--noconfirm", "gnome-terminal"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GNOME Terminal is available."""
        return validate_command(self._run, ["gnome-terminal", "--version"])


class GnomeTerminalPackage(Component):
    """Represent the GNOME Terminal package component."""

    registry_id = "gnome_terminal"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME Terminal component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GNOME Terminal is available."""
        return validate_command(self._run, ["gnome-terminal", "--version"])

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for GNOME Terminal."""
        return (
            UbuntuGnomeTerminal(run=self._run),
            DebianGnomeTerminal(run=self._run),
            FedoraGnomeTerminal(run=self._run),
            ArchGnomeTerminal(run=self._run),
        )
