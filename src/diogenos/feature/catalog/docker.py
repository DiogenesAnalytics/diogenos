"""Define the Docker feature."""

from diogenos.component.catalog.docker.engine import DockerEngine
from diogenos.feature.base import Feature


class Docker(Feature):
    """Represent the Docker feature."""

    def __init__(self) -> None:
        """Initialize the Docker feature."""
        super().__init__(
            components=(DockerEngine(),),
        )
