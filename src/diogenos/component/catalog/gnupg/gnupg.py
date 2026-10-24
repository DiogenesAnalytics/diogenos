"""Define the GnuPG component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.system.base import System


class UbuntuGnuPG(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of GnuPG."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GnuPG implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GnuPG on Ubuntu."""
        self._run(["apt-get", "update"], check=True)
        self._run(
            ["apt-get", "install", "-y", "gnupg"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        result = self._run(
            ["gpg", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class DebianGnuPG(DebianComponentImplementation):
    """Define the Debian implementation of GnuPG."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian GnuPG implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GnuPG on Debian."""
        self._run(["apt-get", "update"], check=True)
        self._run(
            ["apt-get", "install", "-y", "gnupg"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        result = self._run(
            ["gpg", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class FedoraGnuPG(FedoraComponentImplementation):
    """Define the Fedora implementation of GnuPG."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora GnuPG implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GnuPG on Fedora."""
        self._run(
            ["dnf", "install", "-y", "gnupg2"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        result = self._run(
            ["gpg", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class ArchGnuPG(ArchComponentImplementation):
    """Define the Arch Linux implementation of GnuPG."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux GnuPG implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GnuPG on Arch Linux."""
        self._run(
            ["pacman", "-S", "--noconfirm", "gnupg"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        result = self._run(
            ["gpg", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class GnuPGPackage(Component):
    """Represent the GnuPG package component."""

    registry_id = "gnupg"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GnuPG component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GnuPG is available."""
        result = self._run(
            ["gpg", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for GnuPG."""
        return (
            UbuntuGnuPG(run=self._run),
            DebianGnuPG(run=self._run),
            FedoraGnuPG(run=self._run),
            ArchGnuPG(run=self._run),
        )
