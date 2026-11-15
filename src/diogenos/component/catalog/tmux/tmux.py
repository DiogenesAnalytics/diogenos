"""Define the Tmux component."""

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


class UbuntuTmux(UbuntuComponentImplementation, APTInstallMixin):
    """Define the Ubuntu implementation of Tmux."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Tmux implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install Tmux on Ubuntu."""
        self.install_packages(system, ("tmux",), method)

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
        """Verify that Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])


class DebianTmux(DebianComponentImplementation, APTInstallMixin):
    """Define the Debian implementation of Tmux."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Tmux implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install Tmux on Debian."""
        self.install_packages(system, ("tmux",), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        UbuntuTmux(run=self._run).install_apt(system, packages)

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

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install Tmux on Fedora."""
        self._run(
            prepare_command(
                ["dnf", "install", "-y", "tmux"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Tmux is available."""
        return validate_command(self._run, ["tmux", "-V"])


class ArchTmux(ArchComponentImplementation):
    """Define the Arch Linux implementation of Tmux."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Tmux implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install Tmux on Arch Linux."""
        self._run(
            prepare_command(
                ["pacman", "-S", "--noconfirm", "tmux"],
                privileged=True,
            ),
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
