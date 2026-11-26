"""Define the Keyd application configuration component."""

import subprocess
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


APPLICATION_CONFIG_PATH = Path.home() / ".config/keyd/app.conf"

APPLICATION_CONFIG_CONTENT = """\
[gnome-terminal-server]
meta.c = C-S-c
meta.v = C-S-v
"""


def _is_configuration_valid() -> bool:
    """Determine whether the application configuration is valid."""
    try:
        return (
            APPLICATION_CONFIG_PATH.read_text(encoding="utf-8")
            == APPLICATION_CONFIG_CONTENT
        )
    except OSError:
        return False


class UbuntuKeydApplicationConfig(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the Keyd application configuration."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu application configuration implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install the per-application Keyd configuration."""
        self._run(
            ["mkdir", "-p", str(APPLICATION_CONFIG_PATH.parent)],
            check=True,
        )

        self._run(
            ["tee", str(APPLICATION_CONFIG_PATH)],
            input=APPLICATION_CONFIG_CONTENT,
            capture_output=True,
            check=True,
            text=True,
        )

    def verify(self, system: System) -> bool:
        """Verify the per-application Keyd configuration."""
        return _is_configuration_valid()


class KeydApplicationConfig(Component):
    """Represent the per-application Keyd configuration."""

    registry_id = "keyd.config.application"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Keyd application configuration component."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("keyd"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the application configuration is installed."""
        return _is_configuration_valid()

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for this component."""
        return (UbuntuKeydApplicationConfig(run=self._run),)
