"""Test the component implementation abstraction."""

import pytest

from diogenos.feature.component import ComponentImplementation
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    OS = "ubuntu"

    def __init__(
        self,
        verified: bool = True,
    ) -> None:
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


@pytest.mark.component
@pytest.mark.feature
def test_implementation_is_abstract() -> None:
    """Test that ComponentImplementation cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ComponentImplementation()  # type: ignore[abstract]


@pytest.mark.component
@pytest.mark.feature
def test_implementation_supports_system(
    system: System,
) -> None:
    """Test that an implementation supports its system."""
    implementation = ComponentImplementationStub()

    assert implementation.supports(system) is True


@pytest.mark.component
@pytest.mark.feature
def test_implementation_does_not_support_system(
    system: System,
) -> None:
    """Test that an implementation does not support another system."""
    implementation = ComponentImplementationStub()

    system = System(
        platform=system.platform.__class__(
            os="fedora",
            version=system.platform.version,
            codename=system.platform.codename,
            pretty_name="Fedora Linux",
        ),
        hardware=system.hardware,
        desktop=system.desktop,
    )

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
