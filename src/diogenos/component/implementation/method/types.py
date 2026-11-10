"""Define software installation method types."""

from enum import Enum


class MethodType(Enum):
    """Identify software installation methods."""

    APT = "apt"
    SNAP = "snap"
    DOCKER = "docker"
