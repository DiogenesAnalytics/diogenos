"""Test the resolver module."""

from typing import Tuple

import pytest

from diogenos.feature.catalog.docker.engine import DockerEngine
from diogenos.feature.catalog.docker.engine import UbuntuDockerEngine
from diogenos.feature.component import Component
from diogenos.feature.component import ComponentImplementation
from diogenos.resolver import Resolver
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide a minimal component implementation for testing."""

    def __init__(self, supported: bool) -> None:
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
        implementations: Tuple[ComponentImplementation, ...],
    ) -> None:
        """Initialize the component stub."""
        self._implementations = implementations

    def is_satisfied(self, system: System) -> bool:
        """Return whether the component is satisfied."""
        return False

    def implementations(
        self,
    ) -> Tuple[ComponentImplementation, ...]:
        """Return the component implementations."""
        return self._implementations


@pytest.mark.resolver
def test_resolver_returns_supported_implementation(
    system: System,
) -> None:
    """Test that the resolver returns a supported implementation."""
    unsupported = ComponentImplementationStub(supported=False)
    supported = ComponentImplementationStub(supported=True)
    component = ComponentStub((unsupported, supported))

    implementation = Resolver().resolve(component, system)

    assert implementation is supported


@pytest.mark.resolver
def test_resolver_returns_first_supported_implementation(
    system: System,
) -> None:
    """Test that the resolver returns the first supported implementation."""
    first = ComponentImplementationStub(supported=True)
    second = ComponentImplementationStub(supported=True)
    component = ComponentStub((first, second))

    implementation = Resolver().resolve(component, system)

    assert implementation is first


@pytest.mark.resolver
def test_resolver_raises_when_no_implementation_is_supported(
    system: System,
) -> None:
    """Test that the resolver raises when no implementation is supported."""
    component = ComponentStub(
        (
            ComponentImplementationStub(supported=False),
            ComponentImplementationStub(supported=False),
        ),
    )

    with pytest.raises(
        ValueError,
        match="no implementation for component ComponentStub",
    ):
        Resolver().resolve(component, system)


@pytest.mark.feature
def test_resolver_selects_ubuntu_docker_engine(
    system: System,
) -> None:
    """Test that Resolver selects the Ubuntu Docker implementation."""
    component = DockerEngine()

    implementation = Resolver().resolve(component, system)

    assert isinstance(implementation, UbuntuDockerEngine)
