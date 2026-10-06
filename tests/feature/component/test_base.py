"""Test the component abstraction."""

from typing import Tuple

import pytest

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


class ComponentStub(Component):
    """Provide a minimal component for testing."""

    def __init__(
        self,
        satisfied: bool = False,
    ) -> None:
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


@pytest.fixture
def component() -> ComponentStub:
    """Create an unsatisfied component stub."""
    return ComponentStub()


@pytest.fixture
def satisfied_component() -> ComponentStub:
    """Create a satisfied component stub."""
    return ComponentStub(satisfied=True)


@pytest.mark.component
@pytest.mark.feature
def test_component_is_abstract() -> None:
    """Test that Component cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Component()  # type: ignore[abstract]


@pytest.mark.component
@pytest.mark.feature
def test_component_is_satisfied(
    system: System,
    satisfied_component: ComponentStub,
) -> None:
    """Test that a component reports when it is satisfied."""
    assert satisfied_component.is_satisfied(system) is True


@pytest.mark.component
@pytest.mark.feature
def test_component_is_not_satisfied(
    system: System,
    component: ComponentStub,
) -> None:
    """Test that a component reports when it is not satisfied."""
    assert component.is_satisfied(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_component_returns_implementation(
    component: ComponentStub,
) -> None:
    """Test that a component returns its implementation."""
    implementations = component.implementations()

    assert implementations == (component.implementation_stub,)
