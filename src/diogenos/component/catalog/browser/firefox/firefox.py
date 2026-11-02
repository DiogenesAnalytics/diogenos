"""Define the Firefox component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.validation import validate_command
from diogenos.system.base import System


def _is_firefox_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether Firefox is available."""
    return validate_command(run, ["firefox", "--version"]) or validate_command(
        run, ["firefox-esr", "--version"]
    )


class UbuntuFirefox(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Firefox."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Firefox implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Firefox on Ubuntu."""
        self._run(
            prepare_command(["snap", "install", "firefox"], privileged=True),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Firefox is available."""
        return validate_command(self._run, ["firefox", "--version"])


class DebianFirefox(DebianComponentImplementation):
    """Define the Debian implementation of Firefox."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Firefox implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Firefox on Debian."""
        self._run(
            prepare_command(["apt-get", "update"], privileged=True),
            check=True,
        )
        self._run(
            prepare_command(
                ["apt-get", "install", "-y", "firefox-esr"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Firefox is available."""
        return validate_command(self._run, ["firefox-esr", "--version"])


class FedoraFirefox(FedoraComponentImplementation):
    """Define the Fedora implementation of Firefox."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora Firefox implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Firefox on Fedora."""
        self._run(
            prepare_command(
                ["dnf", "install", "-y", "firefox"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Firefox is available."""
        return validate_command(self._run, ["firefox", "--version"])


class ArchFirefox(ArchComponentImplementation):
    """Define the Arch Linux implementation of Firefox."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux Firefox implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Firefox on Arch Linux."""
        self._run(
            prepare_command(
                ["pacman", "-S", "--noconfirm", "firefox"],
                privileged=True,
            ),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that Firefox is available."""
        return validate_command(self._run, ["firefox", "--version"])


class Firefox(Component):
    """Represent the Firefox browser."""

    registry_id = "firefox"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Firefox component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Firefox is available."""
        return _is_firefox_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Firefox."""
        return (
            UbuntuFirefox(run=self._run),
            DebianFirefox(run=self._run),
            FedoraFirefox(run=self._run),
            ArchFirefox(run=self._run),
        )
