"""Detect and represent the hardware of a system."""

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class Hardware:
    """Represent the hardware of a system."""

    machine: str
    processor: str


class HardwareDetector:
    """Detect the hardware of the current system."""

    def detect(self) -> Hardware:
        """Detect the hardware of the current system."""
        return Hardware(
            machine=platform.machine(),
            processor=platform.processor(),
        )
