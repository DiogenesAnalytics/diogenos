"""Define the Pulsar component."""

import json
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Callable
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.system.base import System


PULSAR_RELEASE_URL = "https://api.github.com/repos/pulsar-edit/pulsar/releases/latest"


class UbuntuPulsar(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of Pulsar."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Pulsar implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install the latest official Pulsar release."""
        package_architecture = system.hardware.architecture

        if package_architecture not in ("amd64", "arm64"):
            raise RuntimeError(
                f"unsupported Pulsar architecture: {package_architecture}",
            )

        request = urllib.request.Request(
            PULSAR_RELEASE_URL,
            headers={"Accept": "application/vnd.github+json"},
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            release = json.load(response)

        package_suffix = f"_{package_architecture}.deb"

        package_url = next(
            (
                asset["browser_download_url"]
                for asset in release["assets"]
                if (
                    asset["name"].startswith(
                        ("Linux.pulsar_", "ARM.Linux.pulsar_"),
                    )
                    and asset["name"].endswith(package_suffix)
                )
            ),
            None,
        )

        if package_url is None:
            raise RuntimeError(
                f"no Pulsar .deb package found for {package_architecture}",
            )

        with tempfile.TemporaryDirectory() as directory:
            package_path = Path(directory) / "pulsar.deb"

            urllib.request.urlretrieve(package_url, package_path)

            self._run(
                [
                    "apt-get",
                    "install",
                    "-y",
                    str(package_path),
                ],
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify that Pulsar is available."""
        result = self._run(
            ["pulsar", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )

        return result.returncode == 0


class DebianPulsar(DebianComponentImplementation):
    """Define the Debian implementation of Pulsar."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Debian Pulsar implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install Pulsar on Debian."""
        UbuntuPulsar(run=self._run).install(system)

    def verify(self, system: System) -> bool:
        """Verify that Pulsar is available."""
        return UbuntuPulsar(run=self._run).verify(system)


class PulsarPackage(Component):
    """Represent the Pulsar package component."""

    registry_id = "pulsar"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Pulsar component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether Pulsar is available."""
        result = self._run(
            ["pulsar", "--version"],
            capture_output=True,
            check=False,
            text=True,
        )

        return result.returncode == 0

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for Pulsar."""
        return (
            UbuntuPulsar(run=self._run),
            DebianPulsar(run=self._run),
        )
