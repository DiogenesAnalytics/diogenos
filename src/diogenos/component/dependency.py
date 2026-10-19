"""Define component dependencies."""


class Dependency:
    """Reference a component dependency by name."""

    def __init__(self, name: str) -> None:
        """Initialize the dependency reference."""
        self.name = name
