"""Define the Snap installation method."""

from dataclasses import dataclass

from .options import MethodOptions


@dataclass
class SnapOptions(MethodOptions):
    """Define Snap installation options."""

    classic: bool = False
    channel: str = "stable"
