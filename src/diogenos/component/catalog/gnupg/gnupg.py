"""Define the GnuPG component."""

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
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import APTInstallMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.validation import validate_command
from diogenos.system.base import System


class UbuntuGnuPG(UbuntuComponentImplementation, APTInstallMixin):
    """Define the Ubuntu implementation of GnuPG."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GnuPG implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GnuPG on Ubuntu."""
        self.install_packages(system, ("gnupg",), method)

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
        """Verify that GnuPG is available."""
        return validate_command(self._run, ["gpg", "--version"])


class DebianGnuPG(DebianComponentImplementation, APTInstallMixin):
    """Define the Debian implementation of GnuPG."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian GnuPG implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GnuPG on Debian."""
        self.install_packages(system, ("gnupg",), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        UbuntuGnuPG(run=self._run).install_apt(system, packages)

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        return validate_command(self._run, ["gpg", "--version"])


class FedoraGnuPG(FedoraComponentImplementation):
    """Define the Fedora implementation of GnuPG."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora GnuPG implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GnuPG on Fedora."""
        self._run(
            prepare_command(
                ["dnf", "install", "-y", "gnupg2"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        return validate_command(self._run, ["gpg", "--version"])


class ArchGnuPG(ArchComponentImplementation):
    """Define the Arch Linux implementation of GnuPG."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux GnuPG implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install GnuPG on Arch Linux."""
        self._run(
            prepare_command(
                ["pacman", "-S", "--noconfirm", "gnupg"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GnuPG is available."""
        return validate_command(self._run, ["gpg", "--version"])


class GnuPGPackage(Component):
    """Represent the GnuPG package component."""

    registry_id = "gnupg"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GnuPG component."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("curl"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GnuPG is available."""
        return validate_command(self._run, ["gpg", "--version"])

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
