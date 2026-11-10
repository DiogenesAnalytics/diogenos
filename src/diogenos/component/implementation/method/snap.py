"""Define the Snap installation method."""

from dataclasses import dataclass
from typing import Tuple

from ..execution import prepare_command
from .base import Method
from .options import MethodOptions


@dataclass
class SnapOptions(MethodOptions):
    """Define Snap installation options."""

    classic: bool = False
    channel: str = "stable"


class SnapMethod(Method):
    """Define the Snap package installation method."""

    options: SnapOptions

    def __init__(self, options: SnapOptions) -> None:
        """Initialize the Snap method."""
        super().__init__(options)

    def build(self, packages: Tuple[str, ...]) -> Tuple[str, ...]:
        """Build the Snap installation command."""
        command = ["snap", "install"]

        if self.options.classic:
            command.append("--classic")

        if self.options.channel != "stable":
            command.extend(["--channel", self.options.channel])

        command.extend(packages)

        return tuple(prepare_command(command, privileged=True))
