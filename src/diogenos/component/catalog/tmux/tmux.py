"""Define the Tmux component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.validation import validate_command
from diogenos.system.base import System


class UbuntuTmux(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Tmux."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Tmux implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Tmux on Ubuntu."""
        self._run(["apt-get", "update"], check=True)
        self._run(["apt-get", "install", "-y", "tmux"], check=True)

    def verify(self, system: System) -> bool:
        """Verify that Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])


class DebianTmux(DebianComponentImplementation):
    """Define the Debian implementation of Tmux."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Tmux implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Tmux on Debian."""
        self._run(["apt-get", "update"], check=True)
        self._run(["apt-get", "install", "-y", "tmux"], check=True)

    def verify(self, system: System) -> bool:
        """Verify that Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])


class FedoraTmux(FedoraComponentImplementation):
    """Define the Fedora implementation of Tmux."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora Tmux implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Tmux on Fedora."""
        self._run(["dnf", "install", "-y", "tmux"], check=True)

    def verify(self, system: System) -> bool:
        """Verify that Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])


class ArchTmux(ArchComponentImplementation):
    """Define the Arch Linux implementation of Tmux."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux Tmux implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Tmux on Arch Linux."""
        self._run(
            ["pacman", "-S", "--noconfirm", "tmux"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])


class TmuxPackage(Component):
    """Represent the Tmux package component."""

    registry_id = "tmux"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Tmux package component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Tmux."""
        return (
            UbuntuTmux(run=self._run),
            DebianTmux(run=self._run),
            FedoraTmux(run=self._run),
            ArchTmux(run=self._run),
        )
