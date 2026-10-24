"""Define the Curl component."""

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


class UbuntuCurl(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Curl."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Curl implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Curl on Ubuntu."""
        self._run(["apt-get", "update"], check=True)
        self._run(
            ["apt-get", "install", "-y", "curl"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Curl is available."""
        result = self._run(
            ["curl", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class DebianCurl(DebianComponentImplementation):
    """Define the Debian implementation of Curl."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Curl implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Curl on Debian."""
        UbuntuCurl(run=self._run).install(system)

    def verify(self, system: System) -> bool:
        """Verify that Curl is available."""
        return UbuntuCurl(run=self._run).verify(system)


class FedoraCurl(FedoraComponentImplementation):
    """Define the Fedora implementation of Curl."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora Curl implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Curl on Fedora."""
        self._run(
            ["dnf", "install", "-y", "curl"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Curl is available."""
        result = self._run(
            ["curl", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class ArchCurl(ArchComponentImplementation):
    """Define the Arch Linux implementation of Curl."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux Curl implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Curl on Arch Linux."""
        self._run(
            ["pacman", "-S", "--noconfirm", "curl"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Curl is available."""
        result = self._run(
            ["curl", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class CurlPackage(Component):
    """Represent the Curl package component."""

    registry_id = "curl"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Curl component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Curl is available."""
        result = self._run(
            ["curl", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Curl."""
        return (
            UbuntuCurl(run=self._run),
            DebianCurl(run=self._run),
            FedoraCurl(run=self._run),
            ArchCurl(run=self._run),
        )
