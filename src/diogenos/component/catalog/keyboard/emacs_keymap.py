"""Define the Emacs keymap component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.validation import validate_command
from diogenos.system.base import System


KEYMAP_PATH = "/etc/keyd/diogenos-emacs.conf"

KEYMAP_CONTENT = """\
[ids]
*

[main]
# Cursor movement
C-b = left
C-f = right
C-p = up
C-n = down

# Line navigation
C-a = home
C-e = end
"""


class UbuntuEmacsKeymap(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the Emacs keymap."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu Emacs keymap implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Install and activate the Emacs keymap on Ubuntu."""
        self._run(
            prepare_command(["tee", KEYMAP_PATH], privileged=True),
            input=KEYMAP_CONTENT,
            capture_output=True,
            check=True,
            text=True,
        )
        self._run(
            ["keyd", "check", KEYMAP_PATH],
            capture_output=True,
            check=True,
            text=True,
        )
        self._run(
            prepare_command(["keyd", "reload"], privileged=True),
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that the Emacs keymap configuration is valid."""
        return validate_command(
            self._run,
            ["keyd", "check", KEYMAP_PATH],
        )


class EmacsKeymap(Component):
    """Represent the system-wide Emacs keymap."""

    registry_id = "emacs_keymap"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Emacs keymap component."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("keyd"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the Emacs keymap is installed and valid."""
        return validate_command(
            self._run,
            ["keyd", "check", KEYMAP_PATH],
        )

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the Emacs keymap."""
        return (UbuntuEmacsKeymap(run=self._run),)
