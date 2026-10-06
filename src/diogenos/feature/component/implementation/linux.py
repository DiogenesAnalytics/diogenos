"""Define Linux component implementation strategies."""

from .base import ComponentImplementation


class UbuntuComponentImplementation(ComponentImplementation):
    """Define an implementation for Ubuntu."""

    OS = "ubuntu"


class FedoraComponentImplementation(ComponentImplementation):
    """Define an implementation for Fedora."""

    OS = "fedora"
