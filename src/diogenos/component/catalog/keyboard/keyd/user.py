"""Define the Keyd user configuration component."""

import getpass
import os
import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


def _get_invoking_user() -> str:
    """Return the user who invoked DiogenOS."""
    return os.environ.get("SUDO_USER") or getpass.getuser()


def _is_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
    user: str,
) -> bool:
    """Determine whether the invoking user belongs to the Keyd group."""
    group = run(
        ["getent", "group", "keyd"],
        capture_output=True,
        check=False,
        text=True,
    )

    if group.returncode != 0:
        return False

    result = run(
        ["id", "-nG", user],
        capture_output=True,
        check=False,
        text=True,
    )

    return result.returncode == 0 and "keyd" in result.stdout.split()


class UbuntuKeydUserConfig(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Keyd user configuration."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
        user: str = "",
    ) -> None:
        """Initialize the Ubuntu Keyd user configuration."""
        self._run = run
        self._user = user or _get_invoking_user()

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Add the invoking user to the Keyd group."""
        group = self._run(
            ["getent", "group", "keyd"],
            capture_output=True,
            check=False,
            text=True,
        )

        if group.returncode != 0:
            raise RuntimeError("The Keyd group does not exist.")

        if not _is_satisfied(self._run, self._user):
            self._run(
                prepare_command(
                    ["usermod", "-aG", "keyd", self._user],
                    privileged=True,
                ),
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify that the invoking user belongs to the Keyd group."""
        return _is_satisfied(self._run, self._user)


class KeydUserConfig(Component):
    """Represent Keyd user configuration."""

    registry_id = "keyd.config.user"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
        user: str = "",
    ) -> None:
        """Initialize Keyd user configuration."""
        self._run = run
        self._user = user or _get_invoking_user()

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("keyd"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the invoking user belongs to the Keyd group."""
        return _is_satisfied(self._run, self._user)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Keyd user configuration."""
        return (
            UbuntuKeydUserConfig(
                run=self._run,
                user=self._user,
            ),
        )
