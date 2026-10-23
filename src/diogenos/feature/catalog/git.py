"""Define the Git feature."""

from diogenos.component.catalog.git.git import GitComponent
from diogenos.feature.base import Feature


class Git(Feature):
    """Represent the Git feature."""

    registry_id = "git"

    def __init__(self) -> None:
        """Initialize the Git feature."""
        super().__init__(
            components=(GitComponent(),),
        )
