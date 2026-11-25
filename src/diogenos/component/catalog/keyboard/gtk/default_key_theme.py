"""Define the GTK default key theme component."""

import subprocess
from typing import Callable
from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.method import InstallMethodType
from diogenos.system.base import System


GTK_SCHEMA = "org.gnome.desktop.interface"
GTK_KEY_THEME = "gtk-key-theme"
GTK_KEY_THEME_VALUE = "Default"


def _is_gtk_default_key_theme_satisfied(
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> bool:
    """Determine whether the GTK default key theme is enabled."""
    result = run(
        ["gsettings", "get", GTK_SCHEMA, GTK_KEY_THEME],
        capture_output=True,
        check=False,
        text=True,
    )

    return (
        result.returncode == 0 and result.stdout.strip() == f"{GTK_KEY_THEME_VALUE!r}"
    )


class UbuntuGtkDefaultKeyTheme(UbuntuComponentImplementation):
    """Define the Ubuntu implementation of the GTK default key theme."""

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the Ubuntu GTK default key theme implementation."""
        self._run = run

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Enable the GTK default key theme on Ubuntu."""
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
        """Verify that the GTK default key theme is enabled."""
        return _is_gtk_default_key_theme_satisfied(self._run)


class GtkDefaultKeyTheme(Component):
    """Represent the GTK default key theme."""

    registry_id = "gtk_default_key_theme"

    def __init__(
        self,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        """Initialize the GTK default key theme component."""
        self._run = run

    def is_satisfied(self, system: System) -> bool:
        """Determine whether the GTK default key theme is enabled."""
        return _is_gtk_default_key_theme_satisfied(self._run)

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the GTK default key theme."""
        return (UbuntuGtkDefaultKeyTheme(run=self._run),)
