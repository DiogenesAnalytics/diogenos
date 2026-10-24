"""Define the Git component."""

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


class UbuntuGit(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Git."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Git implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Git on Ubuntu."""
        self._run(["apt-get", "update"], check=True)
        self._run(
            ["apt-get", "install", "-y", "git"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Git is available."""
        return validate_command(self._run, ["git", "--version"])


class DebianGit(DebianComponentImplementation):
    """Define the Debian implementation of Git."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Git implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Git on Debian."""
        self._run(["apt-get", "update"], check=True)
        self._run(
            ["apt-get", "install", "-y", "git"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Git is available."""
        return validate_command(self._run, ["git", "--version"])


class FedoraGit(FedoraComponentImplementation):
    """Define the Fedora implementation of Git."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora Git implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Git on Fedora."""
        self._run(
            ["dnf", "install", "-y", "git"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Git is available."""
        return validate_command(self._run, ["git", "--version"])


class ArchGit(ArchComponentImplementation):
    """Define the Arch Linux implementation of Git."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux Git implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Git on Arch Linux."""
        self._run(
            ["pacman", "-S", "--noconfirm", "git"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Git is available."""
        return validate_command(self._run, ["git", "--version"])


class GitComponent(Component):
    """Represent the Git component."""

    registry_id = "git"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Git component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Git is available."""
        return validate_command(self._run, ["git", "--version"])

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Git."""
        return (
            UbuntuGit(run=self._run),
            DebianGit(run=self._run),
            FedoraGit(run=self._run),
            ArchGit(run=self._run),
        )
