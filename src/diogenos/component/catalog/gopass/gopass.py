"""Define the GoPass component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import ArchComponentImplementation
from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.system.base import System


KEYRING_URL = "https://packages.gopass.pw/repos/gopass/" "gopass-archive-keyring.gpg"
KEYRING_PATH = "/usr/share/keyrings/gopass-archive-keyring.gpg"
SOURCE_PATH = "/etc/apt/sources.list.d/gopass.sources"
PREFERENCES_PATH = "/etc/apt/preferences.d/99gopass.pref"

SOURCE_CONTENT = (
    "Types: deb\n"
    "URIs: https://packages.gopass.pw/repos/gopass\n"
    "Suites: stable\n"
    "Architectures: all amd64 arm64 armhf\n"
    "Components: main\n"
    f"Signed-By: {KEYRING_PATH}\n"
)

PREFERENCES_CONTENT = (
    "# Never prefer packages from this repository by default.\n"
    "Package: *\n"
    "Pin: origin packages.gopass.pw\n"
    "Pin-Priority: 1\n"
    "\n"
    "# Prefer the official GoPass packages.\n"
    "Package: gopass gopass-archive-keyring\n"
    "Pin: origin packages.gopass.pw\n"
    "Pin-Priority: 900\n"
)


class UbuntuGoPass(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of GoPass."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GoPass implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GoPass on Ubuntu."""
        self._run(
            ["curl", "-L", "-q", KEYRING_URL, "-o", KEYRING_PATH],
            check=True,
        )
        self._run(
            ["tee", SOURCE_PATH],
            input=SOURCE_CONTENT,
            capture_output=True,
            check=True,
            text=True,
        )
        self._run(
            ["tee", PREFERENCES_PATH],
            input=PREFERENCES_CONTENT,
            capture_output=True,
            check=True,
            text=True,
        )
        self._run(["apt-get", "update"], check=True)
        self._run(
            [
                "apt-get",
                "install",
                "-y",
                "gopass",
                "gopass-archive-keyring",
            ],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GoPass is available."""
        result = self._run(
            ["gopass", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class DebianGoPass(DebianComponentImplementation):
    """Define the Debian implementation of GoPass."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian GoPass implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GoPass on Debian."""
        UbuntuGoPass(run=self._run).install(system)

    def verify(self, system: System) -> bool:
        """Verify that GoPass is available."""
        return UbuntuGoPass(run=self._run).verify(system)


class FedoraGoPass(FedoraComponentImplementation):
    """Define the Fedora implementation of GoPass."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Fedora GoPass implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GoPass on Fedora."""
        self._run(
            ["dnf", "install", "-y", "gopass"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GoPass is available."""
        result = self._run(
            ["gopass", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class ArchGoPass(ArchComponentImplementation):
    """Define the Arch Linux implementation of GoPass."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Arch Linux GoPass implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install GoPass on Arch Linux."""
        self._run(
            ["pacman", "-S", "--noconfirm", "gopass"],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that GoPass is available."""
        result = self._run(
            ["gopass", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0


class GoPassPackage(Component):
    """Represent the GoPass package component."""

    registry_id = "gopass"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GoPass component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GoPass is available."""
        result = self._run(
            ["gopass", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for GoPass."""
        return (
            UbuntuGoPass(run=self._run),
            DebianGoPass(run=self._run),
            FedoraGoPass(run=self._run),
            ArchGoPass(run=self._run),
        )
