"""Provide shared support for resolver tests."""

from typing import Optional
from typing import Tuple

from diogenos.component import Component
from diogenos.component import ComponentImplementation
from diogenos.component.dependency import Dependency
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    def __init__(self, supported: bool = True) -> None:
        """Initialize the component implementation stub."""
        self.supported = supported

    def supports(self, system: System) -> bool:
        """Determine whether the implementation supports the system."""
        return self.supported

    def install(self, system: System) -> None:
        """Provide a test implementation of installation."""

    def verify(self, system: System) -> bool:
        """Provide a test implementation of verification."""
        return True


class ComponentStub(Component):
    """Provide a minimal component for testing."""

    def __init__(
        self,
        implementations: Tuple[ComponentImplementation, ...] = (),
        registry_id: Optional[str] = "stub",
        dependencies: Tuple[Dependency, ...] = (),
    ) -> None:
        """Initialize the component stub."""
        self._implementations = implementations
        self.registry_id = registry_id
        self._dependencies = dependencies

    def dependencies(self) -> Tuple[Dependency, ...]:
        """Return the component dependencies."""
        return self._dependencies

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        return False

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the component implementations."""
        return self._implementations
