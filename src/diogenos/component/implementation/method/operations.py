"""Define software installation method operations."""

from enum import Enum


class Operation(Enum):
    """Identify operations supported by installation methods."""


class APTOperation(Operation):
    """Define APT operations."""

    INSTALL = ("install",)


class SnapOperation(Operation):
    """Define Snap operations."""

    INSTALL = ("install",)


class DockerOperation(Operation):
    """Define Docker operations."""

    RUN = ("run",)
    COMPOSE_UP = ("compose", "up")
    COMPOSE_DOWN = ("compose", "down")
