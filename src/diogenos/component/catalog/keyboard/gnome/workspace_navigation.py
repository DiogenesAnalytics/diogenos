"""Define the GNOME workspace navigation component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


WINDOW_MANAGER_SCHEMA = "org.gnome.desktop.wm.keybindings"

WORKSPACE_LEFT = "switch-to-workspace-left"
WORKSPACE_RIGHT = "switch-to-workspace-right"

WORKSPACE_LEFT_VALUE = "['<Control><Alt>Left']"
WORKSPACE_RIGHT_VALUE = "['<Control><Alt>Right']"

WORKSPACE_KEYBINDINGS = (
    (WINDOW_MANAGER_SCHEMA, WORKSPACE_LEFT, WORKSPACE_LEFT_VALUE),
    (WINDOW_MANAGER_SCHEMA, WORKSPACE_RIGHT, WORKSPACE_RIGHT_VALUE),
)


def _is_gnome_workspace_navigation_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether GNOME workspace navigation is configured."""
    for schema, key, expected_value in WORKSPACE_KEYBINDINGS:
        result = run(
            ["gsettings", "get", schema, key],
            capture_output=True,
            check=False,
            text=True,
        )

        if result.returncode != 0 or result.stdout.strip() != expected_value:
            return False

    return True


class UbuntuGnomeWorkspaceNavigation(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of GNOME workspace navigation."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GNOME workspace navigation implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Configure GNOME workspace navigation on Ubuntu."""
        for schema, key, value in WORKSPACE_KEYBINDINGS:
            self._run(
                ["gsettings", "set", schema, key, value],
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify GNOME workspace navigation on Ubuntu."""
        return _is_gnome_workspace_navigation_satisfied(self._run)


class GnomeWorkspaceNavigation(Component):
    """Represent the GNOME workspace navigation configuration."""

    registry_id = "gnome_workspace_navigation"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME workspace navigation component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GNOME workspace navigation is configured."""
        return _is_gnome_workspace_navigation_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for GNOME workspace navigation."""
        return (UbuntuGnomeWorkspaceNavigation(run=self._run),)
