"""Define the shared Keyd configuration component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.validation import validate_command
from diogenos.system.base import System


CONFIGURATION_PATH = "/etc/keyd/diogenos.conf"

EMACS_KEYMAP_PATH = "/etc/keyd/diogenos-emacs"
MACOS_KEYMAP_PATH = "/etc/keyd/diogenos-macos"

CONFIGURATION_CONTENT = """\
[ids]
*

include diogenos-emacs
include diogenos-macos
"""


class UbuntuKeydConfiguration(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the shared Keyd configuration."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Keyd configuration implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install and activate the shared Keyd configuration."""
        for path in (EMACS_KEYMAP_PATH, MACOS_KEYMAP_PATH):
            self._run(
                prepare_command(["touch", path], privileged=True),
                check=True,
            )

        self._run(
            prepare_command(["tee", CONFIGURATION_PATH], privileged=True),
            input=CONFIGURATION_CONTENT,
            capture_output=True,
            check=True,
            text=True,
        )

        self._run(
            ["keyd", "check", CONFIGURATION_PATH],
            capture_output=True,
            check=True,
            text=True,
        )

        self._run(
            prepare_command(["keyd", "reload"], privileged=True),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that the shared Keyd configuration is valid."""
        return validate_command(
            self._run,
            ["keyd", "check", CONFIGURATION_PATH],
        )


class KeydConfiguration(Component):
    """Represent the shared Keyd configuration."""

    registry_id = "keyd.config"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the shared Keyd configuration component."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("keyd"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the shared configuration is valid."""
        return validate_command(
            self._run,
            ["keyd", "check", CONFIGURATION_PATH],
        )

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for this component."""
        return (UbuntuKeydConfiguration(run=self._run),)
