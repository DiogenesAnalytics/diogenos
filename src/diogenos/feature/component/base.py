"""Define the component abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Tuple

from diogenos.system.base import System

from .dependency import Dependency
from .implementation.base import ComponentImplementation


class Component(ABC):
    """Define a component that can be satisfied on a system."""

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the dependencies of this component."""
        return ()

    @abstractmethod
    def is_satisfied(self, system: System) -> bool:
        """Determine whether the component is already satisfied."""

    @abstractmethod
    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the implementations available for the component."""
