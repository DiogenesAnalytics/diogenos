"""Define the component package."""

from .base import Component
from .dependency import Dependency
from .implementation.base import ComponentImplementation
from .implementation.linux import AlpineComponentImplementation
from .implementation.linux import ArchComponentImplementation
from .implementation.linux import DebianComponentImplementation
from .implementation.linux import FedoraComponentImplementation
from .implementation.linux import OpenSUSEComponentImplementation
from .implementation.linux import UbuntuComponentImplementation
from .registry import ComponentRegistry


__all__ = [
    "AlpineComponentImplementation",
    "ArchComponentImplementation",
    "Component",
    "ComponentImplementation",
    "ComponentRegistry",
    "DebianComponentImplementation",
    "Dependency",
    "FedoraComponentImplementation",
    "OpenSUSEComponentImplementation",
    "UbuntuComponentImplementation",
]
