"""Define the Build Essentials component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import APTInstallMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


PACKAGE = "build-essential"


def _is_build_essentials_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the Build Essentials package is installed."""
    result = run(
        ["dpkg-query", "-W", "-f=${db:Status-Status}", PACKAGE],
        capture_output=True,
        check=False,
        text=True,
    )

    return result.returncode == 0 and result.stdout.strip() == "installed"


class UbuntuBuildEssentials(UbuntuComponentImplementation, APTInstallMixin):
    """Define the Ubuntu implementation of Build Essentials."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Build Essentials implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install Build Essentials on Ubuntu."""
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
        """Verify that Build Essentials is installed."""
        return _is_build_essentials_satisfied(self._run)


class DebianBuildEssentials(DebianComponentImplementation, APTInstallMixin):
    """Define the Debian implementation of Build Essentials."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Build Essentials implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install Build Essentials on Debian."""
        self.install_packages(system, (PACKAGE,), method)

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        UbuntuBuildEssentials(run=self._run).install_apt(system, packages)

    def verify(self, system: System) -> bool:
        """Verify that Build Essentials is installed."""
        return UbuntuBuildEssentials(run=self._run).verify(system)


class BuildEssentials(Component):
    """Represent the Build Essentials package component."""

    registry_id = "build_essentials"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Build Essentials component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Build Essentials is installed."""
        return _is_build_essentials_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Build Essentials."""
        return (
            UbuntuBuildEssentials(run=self._run),
            DebianBuildEssentials(run=self._run),
        )
