"""Define the Docker user configuration component."""

import getpass
import os
import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.system.base import System


def _get_invoking_user() -> str:
    """Return the user who invoked DiogenOS."""
    return os.environ.get("SUDO_USER") or getpass.getuser()


def _is_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
    user: str,
) -> bool:
    """Determine whether the invoking user belongs to the Docker group."""
    group = run(
        ["getent", "group", "docker"],
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

    return result.returncode == 0 and "docker" in result.stdout.split()


class UbuntuDockerUserConfig(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Docker user configuration."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
        user: str = "",
    ) -> None:
        """Initialize the Docker user configuration implementation."""
        self._run = run
        self._user = user or _get_invoking_user()

    def install(self, system: System) -> None:
        """Configure the invoking user for Docker access."""
        if (
            self._run(
                ["getent", "group", "docker"],
                capture_output=True,
                check=False,
                text=True,
            ).returncode
            != 0
        ):
            self._run(
                ["groupadd", "docker"],
                check=True,
            )

        if not _is_satisfied(self._run, self._user):
            self._run(
                ["usermod", "-aG", "docker", self._user],
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify that the invoking user belongs to the Docker group."""
        return _is_satisfied(self._run, self._user)


class DockerUserConfig(Component):
    """Represent Docker user configuration."""

    registry_id = "docker.config.user"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
        user: str = "",
    ) -> None:
        """Initialize Docker user configuration."""
        self._run = run
        self._user = user or _get_invoking_user()

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Docker user configuration is satisfied."""
        return _is_satisfied(self._run, self._user)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Docker user configuration."""
        return (
            UbuntuDockerUserConfig(
                run=self._run,
                user=self._user,
            ),
        )
