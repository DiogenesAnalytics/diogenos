"""Define the Git feature."""

from diogenos.feature.base import Feature
from diogenos.feature.catalog.git.git import GitComponent


class Git(Feature):
    """Represent the Git feature."""

    def __init__(self) -> None:
        """Initialize the Git feature."""
        super().__init__(
            components=(GitComponent(),),
        )
