"""Define the macOS keyboard feature."""

from diogenos.component.catalog.keyboard.gnome import GnomeOverviewKeybindings
from diogenos.component.catalog.keyboard.gnome import GnomeSuperKey
from diogenos.component.catalog.keyboard.gnome import GnomeWorkspaceNavigation
from diogenos.component.catalog.keyboard.keyd import EmacsKeymap
from diogenos.component.catalog.keyboard.keyd import MacOSKeymap
from diogenos.feature.base import Feature


class MacOSKeyboard(Feature):
    """Represent macOS-style keyboard behavior."""

    registry_id = "macos_keyboard"

    def __init__(self) -> None:
        """Initialize the macOS keyboard feature."""
        super().__init__(
            components=(
                GnomeSuperKey(),
                GnomeOverviewKeybindings(),
                GnomeWorkspaceNavigation(),
                EmacsKeymap(),
                MacOSKeymap(),
            ),
        )
