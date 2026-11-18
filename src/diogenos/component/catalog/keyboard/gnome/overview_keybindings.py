"""Define the GNOME Overview keybindings component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


SHELL_SCHEMA = "org.gnome.shell.keybindings"
WINDOW_MANAGER_SCHEMA = "org.gnome.desktop.wm.keybindings"

OVERVIEW_UP = "shift-overview-up"
OVERVIEW_DOWN = "shift-overview-down"
WORKSPACE_UP = "switch-to-workspace-up"
WORKSPACE_DOWN = "switch-to-workspace-down"

OVERVIEW_UP_VALUE = "['<Control><Alt>Up']"
OVERVIEW_DOWN_VALUE = "['<Control><Alt>Down']"
EMPTY_KEYBINDING_VALUE = "@as []"

OVERVIEW_KEYBINDINGS = (
    (SHELL_SCHEMA, OVERVIEW_UP, OVERVIEW_UP_VALUE),
    (SHELL_SCHEMA, OVERVIEW_DOWN, OVERVIEW_DOWN_VALUE),
    (WINDOW_MANAGER_SCHEMA, WORKSPACE_UP, EMPTY_KEYBINDING_VALUE),
    (WINDOW_MANAGER_SCHEMA, WORKSPACE_DOWN, EMPTY_KEYBINDING_VALUE),
)


def _is_gnome_overview_keybindings_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the GNOME Overview keybindings are configured."""
    for schema, key, expected_value in OVERVIEW_KEYBINDINGS:
        result = run(
            ["gsettings", "get", schema, key],
            capture_output=True,
            check=False,
            text=True,
        )

        if result.returncode != 0 or result.stdout.strip() != expected_value:
            return False

    return True


class UbuntuGnomeOverviewKeybindings(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of GNOME Overview keybindings."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GNOME Overview keybindings implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Configure the GNOME Overview keybindings on Ubuntu."""
        for schema, key, value in OVERVIEW_KEYBINDINGS:
            self._run(
                ["gsettings", "set", schema, key, value],
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify the GNOME Overview keybindings on Ubuntu."""
        return _is_gnome_overview_keybindings_satisfied(self._run)


class GnomeOverviewKeybindings(Component):
    """Represent the GNOME Overview keybindings configuration."""

    registry_id = "gnome_overview_keybindings"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME Overview keybindings component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the GNOME Overview keybindings are configured."""
        return _is_gnome_overview_keybindings_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for GNOME Overview keybindings."""
        return (UbuntuGnomeOverviewKeybindings(run=self._run),)
