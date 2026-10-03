"""Represent the system on which DiogenOS operates."""

from dataclasses import dataclass

from .desktop import Desktop
from .desktop import DesktopDetector
from .hardware import Hardware
from .hardware import HardwareDetector
from .platform import Platform
from .platform import PlatformDetector


@dataclass(frozen=True)
class System:
    """Represent the relevant state of a system."""

    platform: Platform
    hardware: Hardware
    desktop: Desktop


class SystemDetector:
    """Detect the relevant state of the current system."""

    def detect(self) -> System:
        """Detect the current system."""
        return System(
            platform=PlatformDetector().detect(),
            hardware=HardwareDetector().detect(),
            desktop=DesktopDetector().detect(),
        )
