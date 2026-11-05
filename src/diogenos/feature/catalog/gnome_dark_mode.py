"""Define the GNOME dark mode feature."""

from diogenos.component.catalog.gnome.color_scheme import GnomeColorScheme
from diogenos.feature import Feature


class GnomeDarkMode(Feature):
    """Represent the GNOME dark mode feature."""

    registry_id = "gnome_dark_mode"

    def __init__(self) -> None:
        """Initialize the GNOME dark mode feature."""
        super().__init__(
            components=(GnomeColorScheme(color_scheme="prefer-dark"),),
        )
