"""Define the GNOME Super key component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


MUTTER_SCHEMA = "org.gnome.mutter"
SHELL_SCHEMA = "org.gnome.shell.keybindings"
WINDOW_MANAGER_SCHEMA = "org.gnome.desktop.wm.keybindings"

OVERLAY_KEY = "overlay-key"
OVERLAY_KEY_VALUE = ""

EMPTY_KEYBINDING_VALUE = "@as []"

SUPER_KEY_SETTINGS = (
    (
        (MUTTER_SCHEMA, OVERLAY_KEY, OVERLAY_KEY_VALUE),
        (SHELL_SCHEMA, "focus-active-notification", EMPTY_KEYBINDING_VALUE),
        (SHELL_SCHEMA, "toggle-application-view", EMPTY_KEYBINDING_VALUE),
        (SHELL_SCHEMA, "toggle-message-tray", EMPTY_KEYBINDING_VALUE),
        (SHELL_SCHEMA, "toggle-quick-settings", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "maximize", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "minimize", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "unmaximize", "['<Alt>F5']"),
        (WINDOW_MANAGER_SCHEMA, "move-to-monitor-down", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "move-to-monitor-left", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "move-to-monitor-right", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "move-to-monitor-up", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "move-to-workspace-1", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "move-to-workspace-last", EMPTY_KEYBINDING_VALUE),
        (
            WINDOW_MANAGER_SCHEMA,
            "move-to-workspace-left",
            "['<Control><Shift><Alt>Left']",
        ),
        (
            WINDOW_MANAGER_SCHEMA,
            "move-to-workspace-right",
            "['<Control><Shift><Alt>Right']",
        ),
        (WINDOW_MANAGER_SCHEMA, "switch-applications", "['<Alt>Tab']"),
        (
            WINDOW_MANAGER_SCHEMA,
            "switch-applications-backward",
            "['<Shift><Alt>Tab']",
        ),
        (WINDOW_MANAGER_SCHEMA, "switch-group", "['<Alt>Above_Tab']"),
        (
            WINDOW_MANAGER_SCHEMA,
            "switch-group-backward",
            "['<Shift><Alt>Above_Tab']",
        ),
        (WINDOW_MANAGER_SCHEMA, "switch-input-source", "['XF86Keyboard']"),
        (
            WINDOW_MANAGER_SCHEMA,
            "switch-input-source-backward",
            "['<Shift>XF86Keyboard']",
        ),
        (WINDOW_MANAGER_SCHEMA, "switch-to-workspace-1", EMPTY_KEYBINDING_VALUE),
        (WINDOW_MANAGER_SCHEMA, "switch-to-workspace-last", EMPTY_KEYBINDING_VALUE),
    )
    + tuple(
        (SHELL_SCHEMA, f"open-new-window-application-{number}", EMPTY_KEYBINDING_VALUE)
        for number in range(1, 10)
    )
    + tuple(
        (SHELL_SCHEMA, f"switch-to-application-{number}", EMPTY_KEYBINDING_VALUE)
        for number in range(1, 10)
    )
)


def _is_gnome_super_key_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether GNOME Super key behavior is configured."""
    for schema, key, expected_value in SUPER_KEY_SETTINGS:
        result = run(
            ["gsettings", "get", schema, key],
            capture_output=True,
            check=False,
            text=True,
        )

        if result.returncode != 0:
            return False

        if schema == MUTTER_SCHEMA and key == OVERLAY_KEY:
            expected_value = "''"

        if result.stdout.strip() != expected_value:
            return False

    return True


class UbuntuGnomeSuperKey(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the GNOME Super key."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GNOME Super key implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Configure GNOME Super key behavior on Ubuntu."""
        for schema, key, value in SUPER_KEY_SETTINGS:
            self._run(
                ["gsettings", "set", schema, key, value],
                check=True,
            )

    def verify(self, system: System) -> bool:
        """Verify GNOME Super key configuration on Ubuntu."""
        return _is_gnome_super_key_satisfied(self._run)


class GnomeSuperKey(Component):
    """Represent the GNOME Super key configuration."""

    registry_id = "gnome_super_key"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GNOME Super key component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether GNOME Super key behavior is configured."""
        return _is_gnome_super_key_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the GNOME Super key."""
        return (UbuntuGnomeSuperKey(run=self._run),)
