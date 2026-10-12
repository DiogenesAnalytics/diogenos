"""Define the Docker feature."""

from diogenos.feature.base import Feature
from diogenos.feature.catalog.docker.engine import DockerEngine


class Docker(Feature):
    """Represent the Docker feature."""

    def __init__(self) -> None:
        """Initialize the Docker feature."""
        super().__init__(
            components=(DockerEngine(),),
        )
