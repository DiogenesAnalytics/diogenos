"""Define the Pulsar feature."""

from diogenos.component.catalog.pulsar.pulsar import PulsarPackage
from diogenos.feature import Feature


class Pulsar(Feature):
    """Represent the Pulsar feature."""

    registry_id = "pulsar"

    def __init__(self) -> None:
        """Initialize the Pulsar feature."""
        super().__init__(
            components=(PulsarPackage(),),
        )
