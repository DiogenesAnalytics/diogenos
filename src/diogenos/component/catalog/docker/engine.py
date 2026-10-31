"""Define the Docker Engine component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.validation import validate_command
from diogenos.system.base import System


class UbuntuDockerEngine(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Docker Engine."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Docker Engine implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Docker Engine on Ubuntu."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                [
                    "apt-get",
                    "install",
                    "-y",
                    "ca-certificates",
                    "curl",
                ],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(
                [
                    "install",
                    "-m",
                    "0755",
                    "-d",
                    "/etc/apt/keyrings",
                ],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(
                [
                    "curl",
                    "-fsSL",
                    "https://download.docker.com/linux/ubuntu/gpg",
                    "-o",
                    "/etc/apt/keyrings/docker.asc",
                ],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(
                [
                    "chmod",
                    "a+r",
                    "/etc/apt/keyrings/docker.asc",
                ],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(
                [
                    "sh",
                    "-c",
                    (
                        "echo "
                        f"'deb [arch={system.hardware.architecture} "
                        "signed-by=/etc/apt/keyrings/docker.asc] "
                        "https://download.docker.com/linux/ubuntu "
                        f"{system.platform.codename} stable' "
                        "> /etc/apt/sources.list.d/docker.list"
                    ),
                ],
                privileged=True,
            ),
            check=True,
        )
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                [
                    "apt-get",
                    "install",
                    "-y",
                    "docker-ce",
                    "docker-ce-cli",
                    "containerd.io",
                    "docker-buildx-plugin",
                    "docker-compose-plugin",
                ],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Docker Engine is operational."""
        return validate_command(
            self._run,
            prepare_command(["docker", "info"], privileged=True),
        )


class DockerEngine(Component):
    """Represent the Docker Engine component."""

    registry_id = "docker.engine"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Docker Engine component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Docker Engine is operational."""
        return validate_command(
            self._run,
            prepare_command(["docker", "info"], privileged=True),
        )

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Docker Engine."""
        return (UbuntuDockerEngine(run=self._run),)
