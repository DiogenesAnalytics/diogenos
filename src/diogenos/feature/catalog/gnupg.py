"""Define the GnuPG feature."""

from diogenos.component.catalog.gnupg.gnupg import GnuPGPackage
from diogenos.feature import Feature


class GnuPG(Feature):
    """Represent the GnuPG feature."""

    registry_id = "gnupg"

    def __init__(self) -> None:
        """Initialize the GnuPG feature."""
        super().__init__(
            components=(GnuPGPackage(),),
        )
