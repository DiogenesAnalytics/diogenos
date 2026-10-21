"""Test the resolver facade."""

import pytest

from diogenos.component.catalog.docker.engine import DockerEngine
from diogenos.component.catalog.docker.engine import UbuntuDockerEngine
from diogenos.resolver import Resolver
from diogenos.system.base import System


@pytest.mark.resolver
def test_resolve_dependencies_returns_requested_component() -> None:
    """Include the requested component in the resolved dependencies."""
    resolver = Resolver()
    component = DockerEngine()

    components = resolver.resolve_dependencies((component,))

    assert component in components
    assert components[-1] is component


@pytest.mark.resolver
def test_resolve_implementation_selects_ubuntu_docker_engine(
    system: System,
) -> None:
    """Select the Ubuntu Docker implementation."""
    resolver = Resolver()
    component = DockerEngine()

    resolved_component = resolver.resolve_implementation(
        component,
        system,
    )

    assert resolved_component.component is component
    assert isinstance(
        resolved_component.implementation,
        UbuntuDockerEngine,
    )
