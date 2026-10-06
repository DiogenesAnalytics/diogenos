"""Define the component abstraction."""

from abc import ABC
from abc import abstractmethod
from typing import Tuple

from diogenos.system.base import System

from .implementation.base import ComponentImplementation


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
