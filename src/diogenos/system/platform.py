"""Detect and represent the platform of a system."""

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class Platform:
    """Represent the platform of a system."""

    os: str
    version: str
    pretty_name: str


class PlatformDetector:
    """Detect the platform of the current system."""

    def detect(self) -> Platform:
        """Detect the current system platform."""
        system = platform.system()

        if system == "Linux":
            return self._detect_linux()

        return Platform(
            os=system.lower(),
            version=platform.release(),
            pretty_name=platform.platform(),
        )

    def _detect_linux(self) -> Platform:
        """Detect a Linux platform."""
        data = platform.freedesktop_os_release()

        return Platform(
            os=data["ID"],
            version=data["VERSION_ID"],
            pretty_name=data["PRETTY_NAME"],
        )
