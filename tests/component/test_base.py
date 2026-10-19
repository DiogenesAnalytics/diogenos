"""Test the component abstraction."""

from typing import Tuple

import pytest

from diogenos.component import Component
from diogenos.component import Dependency
from diogenos.system.base import System
from tests.component.support import ComponentStub


@pytest.mark.component
def test_component_is_abstract() -> None:
    """Test that Component cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Component()  # type: ignore[abstract]


@pytest.mark.component
def test_component_is_satisfied(
    system: System,
    satisfied_component: ComponentStub,
) -> None:
    """Test that a component reports when it is satisfied."""
    assert satisfied_component.is_satisfied(system) is True


@pytest.mark.component
def test_component_is_not_satisfied(
    system: System,
    component: ComponentStub,
) -> None:
    """Test that a component reports when it is not satisfied."""
    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_component_returns_implementation(
    component: ComponentStub,
) -> None:
    """Test that a component returns its implementation."""
    implementations = component.implementations()

    assert implementations == (component.implementation_stub,)


@pytest.mark.component
def test_component_has_no_dependencies_by_default(
    component: ComponentStub,
) -> None:
    """Test that a component has no dependencies by default."""
    assert component.dependencies() == ()


@pytest.mark.component
def test_component_returns_declared_dependencies() -> None:
    """Test that a component returns its declared dependencies."""
    dependency = Dependency("GitComponent")

    class DependentComponent(ComponentStub):
        """Provide a component with a declared dependency."""

        def dependencies(self) -> Tuple[Dependency, ...]:
            """Return the component dependencies."""
            return (dependency,)

    component = DependentComponent()

    assert component.dependencies() == (dependency,)
    assert component.dependencies()[0].name == "GitComponent"
