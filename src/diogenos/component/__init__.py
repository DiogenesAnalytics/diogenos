"""Define the component package."""

from .base import Component
from .dependency import Dependency
from .implementation.base import ComponentImplementation
from .implementation.linux import ArchComponentImplementation
from .implementation.linux import DebianComponentImplementation
from .implementation.linux import FedoraComponentImplementation
from .implementation.linux import UbuntuComponentImplementation


__all__ = [
    "ArchComponentImplementation",
    "Component",
    "ComponentImplementation",
    "DebianComponentImplementation",
    "Dependency",
    "FedoraComponentImplementation",
    "UbuntuComponentImplementation",
]
