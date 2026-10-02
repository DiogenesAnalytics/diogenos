"""Detect and represent the environment of a system."""

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class Environment:
    """Represent the environment of a system."""

    os: str
    version: str
    pretty_name: str


class EnvironmentDetector:
    """Detect the environment of the current system."""

    def detect(self) -> Environment:
        """Detect the current system environment."""
        system = platform.system()

        if system == "Linux":
            return self._detect_linux()

        return Environment(
            os=system.lower(),
            version=platform.release(),
            pretty_name=platform.platform(),
        )

    def _detect_linux(self) -> Environment:
        """Detect a Linux environment."""
        data = platform.freedesktop_os_release()

        return Environment(
            os=data["ID"],
            version=data["VERSION_ID"],
            pretty_name=data["PRETTY_NAME"],
        )
