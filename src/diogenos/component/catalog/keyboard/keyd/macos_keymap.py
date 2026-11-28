"""Define the macOS keymap component."""

import subprocess
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.catalog.keyboard.keyd.configuration import CONFIGURATION_PATH
from diogenos.component.catalog.keyboard.keyd.configuration import MACOS_KEYMAP_PATH
from diogenos.component.dependency import Dependency
from diogenos.component.implementation.execution import prepare_command
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.validation import validate_command
from diogenos.system.base import System


KEYMAP_PATH = MACOS_KEYMAP_PATH

KEYMAP_CONTENT = """\
[meta]
a = C-a
c = C-c
v = C-v
x = C-x
z = C-z
s = C-s
q = C-q
w = C-w
"""


def _is_keymap_installed(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the macOS keymap is installed and valid."""
    try:
        content = Path(KEYMAP_PATH).read_text(encoding="utf-8")
    except OSError:
        return False

    return content == KEYMAP_CONTENT and validate_command(
        run,
        ["keyd", "check", CONFIGURATION_PATH],
    )


class UbuntuMacOSKeymap(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the macOS keymap."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu macOS keymap implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Install and activate the macOS keymap on Ubuntu."""
        self._run(
            prepare_command(["tee", KEYMAP_PATH], privileged=True),
            input=KEYMAP_CONTENT,
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
        """Verify that the macOS keymap is installed and valid."""
        return _is_keymap_installed(self._run)


class MacOSKeymap(Component):
    """Represent macOS-style application keyboard shortcuts."""

    registry_id = "keyd.keymap.macos"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the macOS keymap component."""
        self._run = run

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return (Dependency("keyd.config"),)

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the macOS keymap is installed and valid."""
        return _is_keymap_installed(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the macOS keymap."""
        return (UbuntuMacOSKeymap(run=self._run),)
