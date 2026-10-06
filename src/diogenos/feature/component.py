"""Define the component abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Tuple

from diogenos.system.base import System


class ComponentImplementation(ABC):
    """Define a platform-specific component implementation."""

    @abstractmethod
    def supports(self, system: System) -> bool:
        """Determine whether this implementation supports the system."""

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
    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the component."""
