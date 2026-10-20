"""Provide fixtures for resolver tests."""

from typing import Callable
from typing import Tuple
from unittest.mock import Mock

import pytest

from diogenos.component.dependency import Dependency
from diogenos.component.registry import ComponentRegistry
from diogenos.resolver.dependencies import DependencyResolver
from tests.resolver.support import ComponentImplementationStub
from tests.resolver.support import ComponentStub


@pytest.fixture
def implementation() -> ComponentImplementationStub:
    """Provide a supported implementation."""
    return ComponentImplementationStub()


@pytest.fixture
def component(
    implementation: ComponentImplementationStub,
) -> ComponentStub:
    """Provide a component with one supported implementation."""
    return ComponentStub((implementation,))


@pytest.fixture
def component_factory() -> Callable[..., ComponentStub]:
    """Provide a factory for creating component stubs."""

    def create_component(
        registry_id: str = "stub",
        dependencies: Tuple[Dependency, ...] = (),
    ) -> ComponentStub:
        """Create a component stub with the given dependencies."""
        return ComponentStub(
            registry_id=registry_id,
            dependencies=dependencies,
        )

    return create_component


@pytest.fixture
def component_registry() -> Mock:
    """Provide a mocked component registry."""
    return Mock(spec=ComponentRegistry)


@pytest.fixture
def dependency_resolver(
    component_registry: Mock,
) -> DependencyResolver:
    """Provide a dependency resolver with a mocked registry."""
    return DependencyResolver(component_registry)
