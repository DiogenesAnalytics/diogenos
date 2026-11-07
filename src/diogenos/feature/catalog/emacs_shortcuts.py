"""Define the GTK Emacs shortcuts feature."""

from diogenos.component.catalog.keyboard.gtk import GtkEmacsKeymap
from diogenos.feature.base import Feature


class GtkEmacsShortcuts(Feature):
    """Represent the GTK Emacs shortcuts feature."""

    registry_id = "gtk_emacs_shortcuts"

    def __init__(self) -> None:
        """Initialize the GTK Emacs shortcuts feature."""
        super().__init__(
            components=(GtkEmacsKeymap(),),
        )
