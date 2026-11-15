"""Define the Keyd component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import APTInstallMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.validation import validate_command
from diogenos.system.base import System


KEYD_PPA = "ppa:keyd-team/ppa"


def _is_keyd_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether Keyd is installed and its service is healthy."""
    return validate_command(
        run, ["systemctl", "is-enabled", "--quiet", "keyd"]
    ) and validate_command(run, ["systemctl", "is-active", "--quiet", "keyd"])


class UbuntuKeyd(UbuntuComponentImplementation, APTInstallMixin):
    """Define the Ubuntu implementation of Keyd."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.APT

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Keyd implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install and enable Keyd on Ubuntu."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", "software-properties-common"],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(
                ["add-apt-repository", "-y", KEYD_PPA],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self.install_packages(system, ("keyd",), method)
        self._run(
            prepare_command(
                ["systemctl", "enable", "--now", "keyd"],
                privileged=True,
            ),
            check=True,
        )

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install packages using APT."""
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", *packages],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Keyd is enabled and running."""
        return _is_keyd_satisfied(self._run)


class Keyd(Component):
    """Represent the Keyd keyboard remapping daemon."""

    registry_id = "keyd"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Keyd component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Keyd is installed and running."""
        return _is_keyd_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Keyd."""
        return (UbuntuKeyd(run=self._run),)
