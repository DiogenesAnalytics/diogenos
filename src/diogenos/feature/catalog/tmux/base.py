"""Define the Tmux feature."""

from diogenos.feature.base import Feature
from diogenos.feature.catalog.tmux.tmux import TmuxPackage


class Tmux(Feature):
    """Represent the Tmux feature."""

    def __init__(self) -> None:
        """Initialize the Tmux feature."""
        super().__init__(
            components=(TmuxPackage(),),
        )
