"""Define the APT installation method."""

from dataclasses import dataclass
from typing import Tuple

from diogenos.component.implementation.command import Command

from .base import Method
from .operations import APTOperation
from .operations import Operation
from .options import MethodOptions


@dataclass
class APTOptions(MethodOptions):
    """Define APT installation options."""

    assume_yes: bool = True
    no_install_recommends: bool = False


class APTMethod(Method):
    """Define the APT package installation method."""

    OPERATIONS = (APTOperation.INSTALL,)

    options: APTOptions

    def __init__(self, options: APTOptions) -> None:
        """Initialize the APT method."""
        super().__init__(options)

    def build(
        self,
        operation: Operation,
        arguments: Tuple[str, ...] = (),
    ) -> Command:
        """Build a command for the specified operation."""
        if not self.supports(operation):
            raise ValueError(f"unsupported APT operation: {operation}")

        match operation:
            case APTOperation.INSTALL:
                command = ["apt-get", "install"]

                if self.options.assume_yes:
                    command.append("-y")

                if self.options.no_install_recommends:
                    command.append("--no-install-recommends")

                command.extend(arguments)

                return Command.from_arguments(
                    tuple(command),
                    privileged=True,
                )

        raise ValueError(f"unsupported APT operation: {operation}")
