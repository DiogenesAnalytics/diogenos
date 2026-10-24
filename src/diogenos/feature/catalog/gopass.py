"""Define the GoPass feature."""

from diogenos.component.catalog.curl.curl import CurlPackage
from diogenos.component.catalog.gnupg.gnupg import GnuPGPackage
from diogenos.component.catalog.gopass.gopass import GoPassPackage
from diogenos.feature import Feature


class GoPass(Feature):
    """Represent the GoPass feature."""

    registry_id = "gopass"

    def __init__(self) -> None:
        """Initialize the GoPass feature."""
        super().__init__(
            components=(
                CurlPackage(),
                GnuPGPackage(),
                GoPassPackage(),
            )
        )
