"""Define the Docker Engine component."""

import subprocess
from typing import Callable

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


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

    def implementation(
        self,
        system: System,
    ) -> ComponentImplementation:
        """Return the implementation for the system."""
        raise NotImplementedError
