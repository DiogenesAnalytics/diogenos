"""Detect and represent the hardware of a system."""

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class Hardware:
    """Represent the hardware of a system."""

    machine: str
    processor: str
    architecture: str


class HardwareDetector:
    """Detect the hardware of the current system."""

    def detect(self) -> Hardware:
        """Detect the current system hardware."""
        machine = platform.machine()

        architecture = {
            "x86_64": "amd64",
            "amd64": "amd64",
            "aarch64": "arm64",
            "arm64": "arm64",
        }.get(machine, machine)

        return Hardware(
            machine=machine,
            processor=platform.processor(),
            architecture=architecture,
        )
