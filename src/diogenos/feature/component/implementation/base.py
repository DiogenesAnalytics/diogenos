"""Define the component implementation abstraction."""

from abc import ABC
from abc import abstractmethod

from diogenos.system.base import System


class ComponentImplementation(ABC):
    """Define a component implementation."""

    OS: str

    def supports(self, system: System) -> bool:
        """Determine whether this implementation supports the system."""
        return system.platform.os == self.OS

    @abstractmethod
    def install(self, system: System) -> None:
        """Install the component."""

    @abstractmethod
    def verify(self, system: System) -> bool:
        """Verify that the component was installed correctly."""
