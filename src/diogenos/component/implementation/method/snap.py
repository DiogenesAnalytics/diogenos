"""Define the Snap installation method."""

from dataclasses import dataclass
from typing import Tuple

from diogenos.component.implementation.command import Command
from diogenos.component.implementation.execution import prepare_command

from .base import Method
from .operations import Operation
from .operations import SnapOperation
from .options import MethodOptions


@dataclass
class SnapOptions(MethodOptions):
    """Define Snap installation options."""

    classic: bool = False
    channel: str = "stable"


class SnapMethod(Method):
    """Define the Snap package installation method."""

    OPERATIONS = (SnapOperation.INSTALL,)

    options: SnapOptions

    def __init__(self, options: SnapOptions) -> None:
        """Initialize the Snap method."""
        super().__init__(options)

    def build(
        self,
        operation: Operation,
        arguments: Tuple[str, ...] = (),
    ) -> Command:
        """Build a command for the specified operation."""
        if not self.supports(operation):
            raise ValueError(f"unsupported Snap operation: {operation}")

        match operation:
            case SnapOperation.INSTALL:
                command = ["snap", "install"]

                if self.options.classic:
                    command.append("--classic")

                if self.options.channel != "stable":
                    command.extend(["--channel", self.options.channel])

                command.extend(arguments)

                return Command.from_arguments(
                    tuple(prepare_command(command, privileged=True)),
                )

        raise ValueError(f"unsupported Snap operation: {operation}")
