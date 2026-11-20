"""Define the GCC component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import APTInstallMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.validation import validate_command
from diogenos.system.base import System


PACKAGE = "gcc"


class UbuntuGCC(UbuntuComponentImplementation, APTInstallMixin):
    """Define the Ubuntu implementation of GCC."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GCC implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GCC on Ubuntu."""
        self.install_packages(system, (PACKAGE,), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", *packages],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GCC is available."""
        return validate_command(self._run, ["gcc", "--version"])


class DebianGCC(DebianComponentImplementation, APTInstallMixin):
    """Define the Debian implementation of GCC."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian GCC implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GCC on Debian."""
        self.install_packages(system, (PACKAGE,), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        UbuntuGCC(run=self._run).install_apt(system, packages)

    def verify(self, system: System) -> bool:
        """Verify that GCC is available."""
        return UbuntuGCC(run=self._run).verify(system)


class FedoraGCC(FedoraComponentImplementation):
    """Define the Fedora implementation of GCC."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora GCC implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GCC on Fedora."""
        self._run(
            prepare_command(
                ["dnf", "install", "-y", PACKAGE],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GCC is available."""
        return validate_command(self._run, ["gcc", "--version"])


class ArchGCC(ArchComponentImplementation):
    """Define the Arch Linux implementation of GCC."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux GCC implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GCC on Arch Linux."""
        self._run(
            prepare_command(
                ["pacman", "-S", "--noconfirm", PACKAGE],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GCC is available."""
        return validate_command(self._run, ["gcc", "--version"])


class GCC(Component):
    """Represent the GCC compiler component."""

    registry_id = "gcc"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GCC component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GCC is available."""
        return validate_command(self._run, ["gcc", "--version"])

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for GCC."""
        return (
            UbuntuGCC(run=self._run),
            DebianGCC(run=self._run),
            FedoraGCC(run=self._run),
            ArchGCC(run=self._run),
        )
