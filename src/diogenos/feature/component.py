"""Define the component abstraction."""

from abc import ABC
from abc import abstractmethod

from diogenos.system.base import System


class ComponentImplementation(ABC):
    """Define a platform-specific component implementation."""

    @abstractmethod
    def install(self, system: System) -> None:
        """Install the component on the system."""

    @abstractmethod
    def verify(self, system: System) -> bool:
        """Verify that the component was installed correctly."""


class Component(ABC):
    """Define a component that can be satisfied on a system."""

    @abstractmethod
    def is_satisfied(self, system: System) -> bool:
        """Determine whether the component is already satisfied."""

    @abstractmethod
    def implementation(self, system: System) -> ComponentImplementation:
        """Return the implementation appropriate for the system."""

    def apply(self, system: System) -> None:
        """Satisfy the component on the system."""
        if self.is_satisfied(system):
            return

        implementation = self.implementation(system)
        implementation.install(system)

        if not implementation.verify(system):
            raise RuntimeError(f"component {type(self).__name__} failed verification")
