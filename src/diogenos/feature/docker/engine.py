"""Define the Docker Engine component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


class UbuntuDockerEngine(ComponentImplementation):
    """Define the Ubuntu implementation of Docker Engine."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Docker Engine implementation."""
        self._run = run

    def supports(self, system: System) -> bool:
        """Determine whether this implementation supports the system."""
        return system.platform.os == "ubuntu"

    def install(self, system: System) -> None:
        """Install Docker Engine on Ubuntu."""
        raise NotImplementedError

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
