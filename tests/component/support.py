"""Provide shared support for component tests."""

from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    def supports(self, system: System) -> bool:
        """Determine whether the implementation supports the system."""
        return True

    def install(self, system: System) -> None:
        """Install the component."""
        pass

    def verify(self, system: System) -> bool:
        """Verify the component."""
        return True


class ComponentStub(Component):
    """Provide a minimal component for testing."""

    def __init__(self, satisfied: bool = False) -> None:
        """Initialize the component stub."""
        self.satisfied = satisfied
        self.implementation_stub = ComponentImplementationStub()

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        return self.satisfied

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the component implementations."""
        return (self.implementation_stub,)
