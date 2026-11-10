"""Define Linux component implementation strategies."""

from .base import ComponentImplementation
from .method.apt import APTMethod
from .method.apt import APTOptions
from .method.snap import SnapMethod
from .method.snap import SnapOptions
from .method.types import MethodType


class APTComponentImplementation(ComponentImplementation):
    """Define an implementation using APT."""

    METHODS = {
        MethodType.APT: (
            APTMethod,
            APTOptions(),
        ),
    }


class SnapComponentImplementation(ComponentImplementation):
    """Define an implementation using Snap."""

    METHODS = {
        MethodType.SNAP: (
            SnapMethod,
            SnapOptions(),
        ),
    }


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
