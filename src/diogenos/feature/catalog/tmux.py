"""Define the Tmux feature."""

from diogenos.component.catalog.tmux.config import TmuxConfig
from diogenos.component.catalog.tmux.tmux import TmuxPackage
from diogenos.feature.base import Feature


class Tmux(Feature):
    """Represent the Tmux feature."""

    registry_id = "tmux"

    def __init__(self) -> None:
        """Initialize the Tmux feature."""
        super().__init__(
            components=(
                TmuxPackage(),
                TmuxConfig(),
            ),
        )
