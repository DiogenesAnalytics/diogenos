"""Define the APT installation method."""

from dataclasses import dataclass
from typing import Tuple

from ..execution import prepare_command
from .base import Method
from .options import MethodOptions


@dataclass
class APTOptions(MethodOptions):
    """Define APT installation options."""

    assume_yes: bool = True
    no_install_recommends: bool = False


class APTMethod(Method):
    """Define the APT package installation method."""

    options: APTOptions

    def __init__(self, options: APTOptions) -> None:
        """Initialize the APT method."""
        super().__init__(options)

    def build(self, packages: Tuple[str, ...]) -> Tuple[str, ...]:
        """Build the APT installation command."""
        command = ["apt-get", "install"]

        if self.options.assume_yes:
            command.append("-y")

        if self.options.no_install_recommends:
            command.append("--no-install-recommends")

        command.extend(packages)

        return tuple(prepare_command(command, privileged=True))
