"""Define the Zed feature."""

from diogenos.component.catalog.zed.zed import ZedPackage
from diogenos.feature import Feature


class Zed(Feature):
    """Represent the Zed feature."""

    registry_id = "zed"

    def __init__(self) -> None:
        """Initialize the Zed feature."""
        super().__init__(
            components=(ZedPackage(),),
        )
