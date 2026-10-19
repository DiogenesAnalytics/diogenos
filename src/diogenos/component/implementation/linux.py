"""Define Linux component implementation strategies."""

from .base import ComponentImplementation


class APTComponentImplementation(ComponentImplementation):
    """Define an implementation using APT."""


class DebianComponentImplementation(APTComponentImplementation):
    """Define an implementation for Debian."""

    OS = "debian"


class UbuntuComponentImplementation(APTComponentImplementation):
    """Define an implementation for Ubuntu."""

    OS = "ubuntu"


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
