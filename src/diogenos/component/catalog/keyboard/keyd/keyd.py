"""Define the Keyd component."""

import subprocess
import tempfile
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.validation import validate_command
from diogenos.system.base import System


KEYD_REPOSITORY = "https://github.com/rvaiya/keyd.git"
KEYD_VERSION = "v2.6.0"


def _is_keyd_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether Keyd is installed and its service is healthy."""
    return validate_command(
        run, ["systemctl", "is-enabled", "--quiet", "keyd"]
    ) and validate_command(run, ["systemctl", "is-active", "--quiet", "keyd"])


class UbuntuKeyd(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Keyd."""

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
        """Build, install, and enable Keyd on Ubuntu."""
        with tempfile.TemporaryDirectory(prefix="diogenos-keyd-") as directory:
            source_directory = Path(directory) / "keyd"

            self._run(
                [
                    "git",
                    "clone",
                    "--branch",
                    KEYD_VERSION,
                    "--depth",
                    "1",
                    KEYD_REPOSITORY,
                    str(source_directory),
                ],
                check=True,
            )

            self._run(
                ["make"],
                cwd=source_directory,
                check=True,
            )

            self._run(
                prepare_command(["make", "install"], privileged=True),
                cwd=source_directory,
                check=True,
            )

        self._run(
            prepare_command(["systemctl", "daemon-reload"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["systemctl", "enable", "--now", "keyd"],
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

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (
            Dependency("git"),
            Dependency("build_essentials"),
            Dependency("linux_kernel_headers"),
        )

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Keyd is installed and running."""
        return _is_keyd_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Keyd."""
        return (UbuntuKeyd(run=self._run),)
