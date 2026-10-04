"""Test the component module."""

import pytest

from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    def __init__(self, verified: bool = True) -> None:
        """Initialize the component implementation stub."""
        self.verified = verified
        self.install_called = False
        self.verify_called = False

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
        verified: bool = True,
    ) -> None:
        """Initialize the component stub."""
        self.satisfied = satisfied
        self.implementation_stub = ComponentImplementationStub(
            verified=verified,
        )

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        return self.satisfied

    def implementation(
        self,
        system: System,
    ) -> ComponentImplementation:
        """Return the component implementation."""
        return self.implementation_stub


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
def test_apply_when_satisfied(
    system: System,
    satisfied_component: ComponentStub,
) -> None:
    """Test that apply does nothing when already satisfied."""
    satisfied_component.apply(system)

    assert satisfied_component.implementation_stub.install_called is False
    assert satisfied_component.implementation_stub.verify_called is False


@pytest.mark.component
@pytest.mark.feature
def test_apply_when_not_satisfied(
    system: System,
    component: ComponentStub,
) -> None:
    """Test that apply installs and verifies an unsatisfied component."""
    component.apply(system)

    assert component.implementation_stub.install_called is True
    assert component.implementation_stub.verify_called is True


@pytest.mark.component
@pytest.mark.feature
def test_apply_raises_when_verification_fails(
    system: System,
    failed_component: ComponentStub,
) -> None:
    """Test that apply raises when verification fails."""
    with pytest.raises(RuntimeError, match="failed verification"):
        failed_component.apply(system)

    assert failed_component.implementation_stub.install_called is True
    assert failed_component.implementation_stub.verify_called is True
