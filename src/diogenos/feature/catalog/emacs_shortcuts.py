"""Define the Emacs shortcuts feature."""

from diogenos.component.catalog.keyboard.emacs_keymap import EmacsKeymap
from diogenos.component.catalog.keyboard.gtk import GtkEmacsKeymap
from diogenos.component.catalog.keyboard.keyd import Keyd
from diogenos.feature.base import Feature


class EmacsShortcuts(Feature):
    """Represent the Emacs shortcuts feature."""

    registry_id = "emacs_shortcuts"

    def __init__(self) -> None:
        """Initialize the Emacs shortcuts feature."""
        super().__init__(
            components=(
                Keyd(),
                EmacsKeymap(),
                GtkEmacsKeymap(),
            ),
        )
