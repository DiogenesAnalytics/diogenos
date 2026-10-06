"""Test the component module."""

from typing import Tuple

import pytest

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    def __init__(
        self,
        supported: bool = True,
        verified: bool = True,
    ) -> None:
        """Initialize the component implementation stub."""
        self.supported = supported
        self.verified = verified
        self.install_called = False
        self.verify_called = False

    def supports(self, system: System) -> bool:
        """Determine whether the implementation supports the system."""
        return self.supported

    def install(self, system: System) -> None:
        """Record that installation was called."""
        self.install_called = True

    def verify(self, system: System) -> bool:
        """Record that verification was called."""
        self.verify_called = True
        return self.verified


class ComponentStub(Component):
    """Provide a minimal component for testing."""

    def __init__(
        self,
        satisfied: bool = False,
        supported: bool = True,
        verified: bool = True,
    ) -> None:
        """Initialize the component stub."""
        self.satisfied = satisfied
        self.implementation_stub = ComponentImplementationStub(
            supported=supported,
            verified=verified,
        )

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        return self.satisfied

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the component implementations."""
        return (self.implementation_stub,)


@pytest.fixture
def component() -> ComponentStub:
    """Create an unsatisfied component stub."""
    return ComponentStub()


@pytest.fixture
def satisfied_component() -> ComponentStub:
    """Create a satisfied component stub."""
    return ComponentStub(satisfied=True)


@pytest.fixture
def failed_component() -> ComponentStub:
    """Create a component stub that fails verification."""
    return ComponentStub(verified=False)


@pytest.mark.component
@pytest.mark.feature
def test_component_is_abstract() -> None:
    """Test that Component cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Component()  # type: ignore[abstract]


@pytest.mark.component
@pytest.mark.feature
def test_implementation_is_abstract() -> None:
    """Test that ComponentImplementation cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ComponentImplementation()  # type: ignore[abstract]


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


@pytest.mark.component
@pytest.mark.feature
def test_implementation_supports_system(
    system: System,
) -> None:
    """Test that an implementation reports support for a system."""
    implementation = ComponentImplementationStub(supported=True)

    assert implementation.supports(system) is True


@pytest.mark.component
@pytest.mark.feature
def test_implementation_does_not_support_system(
    system: System,
) -> None:
    """Test that an implementation reports when it does not support a system."""
    implementation = ComponentImplementationStub(supported=False)

    assert implementation.supports(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_implementation_install(
    system: System,
) -> None:
    """Test that installation is called."""
    implementation = ComponentImplementationStub()

    implementation.install(system)

    assert implementation.install_called is True


@pytest.mark.component
@pytest.mark.feature
def test_implementation_verify(
    system: System,
) -> None:
    """Test that verification is called."""
    implementation = ComponentImplementationStub()

    assert implementation.verify(system) is True
    assert implementation.verify_called is True
