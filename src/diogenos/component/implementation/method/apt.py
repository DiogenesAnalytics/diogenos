"""Define the APT installation method."""

from dataclasses import dataclass

from .options import MethodOptions


@dataclass
class APTOptions(MethodOptions):
    """Define APT installation options."""

    assume_yes: bool = True
    no_install_recommends: bool = False
