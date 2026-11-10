"""Define Linux component implementation strategies."""

from .base import ComponentImplementation
from .method.types import MethodType


class APTComponentImplementation(ComponentImplementation):
    """Define an implementation using APT."""


class SnapComponentImplementation(ComponentImplementation):
    """Define an implementation using Snap."""


class DebianComponentImplementation(APTComponentImplementation):
    """Define an implementation for Debian."""

    OS = "debian"
    DEFAULT_METHOD = MethodType.APT


class UbuntuComponentImplementation(
    APTComponentImplementation,
    SnapComponentImplementation,
):
    """Define an implementation for Ubuntu."""

    OS = "ubuntu"
    DEFAULT_METHOD = MethodType.SNAP


class FedoraComponentImplementation(ComponentImplementation):
    """Define an implementation for Fedora."""

    OS = "fedora"


class ArchComponentImplementation(ComponentImplementation):
    """Define an implementation for Arch Linux."""

    OS = "arch"


class OpenSUSEComponentImplementation(ComponentImplementation):
    """Define an implementation for openSUSE."""

    OS = "opensuse"


class AlpineComponentImplementation(ComponentImplementation):
    """Define an implementation for Alpine Linux."""

    OS = "alpine"
