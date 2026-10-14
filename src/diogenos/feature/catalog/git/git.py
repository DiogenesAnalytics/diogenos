"""Define the Git component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.feature.component import FedoraComponentImplementation
from diogenos.feature.component import UbuntuComponentImplementation
from diogenos.system.base import System


class UbuntuGit(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Git."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Git implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Git on Ubuntu."""
        self._run(["apt-get", "update"], check=True)
        self._run(
            ["apt-get", "install", "-y", "git"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Git is available."""
        result = self._run(
            ["git", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class FedoraGit(FedoraComponentImplementation):
    """Define the Fedora implementation of Git."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora Git implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Git on Fedora."""
        self._run(
            ["dnf", "install", "-y", "git"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Git is available."""
        result = self._run(
            ["git", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class GitComponent(Component):
    """Represent the Git component."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Git component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Git is available."""
        result = self._run(
            ["git", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Git."""
        return (
            UbuntuGit(run=self._run),
            FedoraGit(run=self._run),
        )
