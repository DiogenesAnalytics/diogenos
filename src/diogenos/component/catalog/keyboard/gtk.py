"""Define the GTK Emacs keymap component."""

import subprocess
from typing import Callable
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.system.base import System


GTK_SCHEMA = "org.gnome.desktop.interface"
GTK_KEY_THEME = "gtk-key-theme"
GTK_KEY_THEME_VALUE = "Emacs"


def _is_gtk_emacs_keymap_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the GTK Emacs key theme is enabled."""
    result = run(
        ["gsettings", "get", GTK_SCHEMA, GTK_KEY_THEME],
        capture_output=True,
        check=False,
        text=True,
    )

    return (
        result.returncode == 0 and result.stdout.strip() == f"{GTK_KEY_THEME_VALUE!r}"
    )


class UbuntuGtkEmacsKeymap(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the GTK Emacs keymap."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GTK Emacs keymap implementation."""
        self._run = run

    def install(self, system: System) -> None:
        """Enable the GTK Emacs key theme on Ubuntu."""
        self._run(
            [
                "gsettings",
                "set",
                GTK_SCHEMA,
                GTK_KEY_THEME,
                GTK_KEY_THEME_VALUE,
            ],
            check=True,
        )

    def verify(self, system: System) -> bool:
        """Verify that the GTK Emacs key theme is enabled."""
        return _is_gtk_emacs_keymap_satisfied(self._run)


class GtkEmacsKeymap(Component):
    """Represent the GTK Emacs keymap."""

    registry_id = "gtk_emacs_keymap"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GTK Emacs keymap component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the GTK Emacs key theme is enabled."""
        return _is_gtk_emacs_keymap_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the GTK Emacs keymap."""
        return (UbuntuGtkEmacsKeymap(run=self._run),)
