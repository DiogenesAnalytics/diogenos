"""Define the software installation method abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Tuple

from diogenos.system.base import System

from .options import MethodOptions


class Method(ABC):
    """Define a software installation method."""

    def __init__(self, options: MethodOptions) -> None:
        """Initialize the method with its options."""
        self.options = options

    @abstractmethod
    def install(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Install the specified packages."""
