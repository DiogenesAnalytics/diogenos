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

    def supports(
        self,
        platform: str | None = None,
        desktop: str | None = None,
        machine: str | None = None,
    ) -> bool:
        """Determine whether the system satisfies the specified conditions."""
        if platform is None and desktop is None and machine is None:
            raise ValueError("at least one condition must be specified")

        if platform is not None and self.platform.os != platform:
            return False

        if desktop is not None and self.desktop.name != desktop:
            return False

        if machine is not None and self.hardware.machine != machine:
            return False

        return True


class SystemDetector:
    """Detect the relevant state of the current system."""

    def detect(self) -> System:
        """Detect the current system."""
        return System(
            platform=PlatformDetector().detect(),
            hardware=HardwareDetector().detect(),
            desktop=DesktopDetector().detect(),
        )
