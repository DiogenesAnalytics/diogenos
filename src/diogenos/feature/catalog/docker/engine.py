"""Define the Docker Engine component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.feature.component import UbuntuComponentImplementation
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
            ["apt-get", "update"],
        )
        self._run(
            [
                "apt-get",
                "install",
                "-y",
                "ca-certificates",
                "curl",
            ],
        )
        self._run(
            [
                "install",
                "-m",
                "0755",
                "-d",
                "/etc/apt/keyrings",
            ],
        )
        self._run(
            [
                "curl",
                "-fsSL",
                "https://download.docker.com/linux/ubuntu/gpg",
                "-o",
                "/etc/apt/keyrings/docker.asc",
            ],
        )
        self._run(
            [
                "chmod",
                "a+r",
                "/etc/apt/keyrings/docker.asc",
            ],
        )
        self._run(
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
        )
        self._run(
            ["apt-get", "update"],
        )
        self._run(
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
        )

    def verify(self, system: System) -> bool:
        """Verify that Docker Engine is installed correctly."""
        result = self._run(
            ["docker", "run", "hello-world"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class DockerEngine(Component):
    """Represent the Docker Engine component."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Docker Engine component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Docker Engine is usable."""
        result = self._run(
            ["docker", "run", "hello-world"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Docker Engine."""
        return (UbuntuDockerEngine(run=self._run),)
