"""Define the Make component."""

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


class UbuntuMake(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Make."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Make implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Make on Ubuntu."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", "make"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Make is available."""
        return validate_command(self._run, ["make", "--version"])


class DebianMake(DebianComponentImplementation):
    """Define the Debian implementation of Make."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Make implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Make on Debian."""
        UbuntuMake(run=self._run).install(system)

    def verify(self, system: System) -> bool:
        """Verify that Make is available."""
        return UbuntuMake(run=self._run).verify(system)


class FedoraMake(FedoraComponentImplementation):
    """Define the Fedora implementation of Make."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora Make implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Make on Fedora."""
        self._run(
            prepare_command(
                ["dnf", "install", "-y", "make"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Make is available."""
        return validate_command(self._run, ["make", "--version"])


class ArchMake(ArchComponentImplementation):
    """Define the Arch Linux implementation of Make."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux Make implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Make on Arch Linux."""
        self._run(
            prepare_command(
                ["pacman", "-S", "--noconfirm", "make"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Make is available."""
        return validate_command(self._run, ["make", "--version"])


class MakePackage(Component):
    """Represent the Make package component."""

    registry_id = "make"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Make component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Make is available."""
        return validate_command(self._run, ["make", "--version"])

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Make."""
        return (
            UbuntuMake(run=self._run),
            DebianMake(run=self._run),
            FedoraMake(run=self._run),
            ArchMake(run=self._run),
        )
