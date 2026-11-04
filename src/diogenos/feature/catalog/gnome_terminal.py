"""Define the GNOME Terminal feature."""

from diogenos.component.catalog.terminal.gnome_terminal import GnomeTerminalPackage
from diogenos.feature import Feature


class GnomeTerminal(Feature):
    """Represent the GNOME Terminal feature."""

    registry_id = "gnome_terminal"

    def __init__(self) -> None:
        """Initialize the GNOME Terminal feature."""
        super().__init__(
            components=(GnomeTerminalPackage(),),
        )
