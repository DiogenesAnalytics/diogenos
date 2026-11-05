"""Define the Zed component."""

import subprocess
from pathlib import Path
from typing import Callable
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.validation import validate_command
from diogenos.system.base import System


ZED_EXECUTABLE = Path.home() / ".local/bin/zed"


class ZedImplementation:
    """Define the shared Zed implementation."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Zed implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Zed using its official Linux installer."""
        installer = self._run(
            ["curl", "-fL", "https://zed.dev/install.sh"],
            capture_output=True,
            check=True,
            text=True,
        )

        self._run(
            ["sh"],
            input=installer.stdout,
            check=True,
            text=True,
        )

    def verify(self, system: System) -> bool:
        """Verify the Zed installation."""
        return validate_command(
            self._run,
            [str(ZED_EXECUTABLE), "--version"],
        )


class UbuntuZed(ZedImplementation, UbuntuComponentImplementation):
    """Represent the Ubuntu Zed implementation."""


class DebianZed(ZedImplementation, DebianComponentImplementation):
    """Represent the Debian Zed implementation."""


class FedoraZed(ZedImplementation, FedoraComponentImplementation):
    """Represent the Fedora Zed implementation."""


class ArchZed(ZedImplementation, ArchComponentImplementation):
    """Represent the Arch Zed implementation."""


class ZedPackage(Component):
    """Represent the Zed package."""

    registry_id = "zed"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Zed package."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("curl"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Zed is installed."""
        return validate_command(
            self._run,
            [str(ZED_EXECUTABLE), "--version"],
        )

    def implementations(self) -> Tuple[ComponentImplementation, ...]:
        """Return the available implementations."""
        return (
            UbuntuZed(run=self._run),
            DebianZed(run=self._run),
            FedoraZed(run=self._run),
            ArchZed(run=self._run),
        )
