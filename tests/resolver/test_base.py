"""Test the resolver facade."""

import pytest

from diogenos.component.catalog.docker.engine import DockerEngine
from diogenos.component.catalog.docker.engine import UbuntuDockerEngine
from diogenos.resolver import Resolver
from diogenos.system.base import System


@pytest.mark.resolver
def test_resolver_selects_ubuntu_docker_engine(
    system: System,
) -> None:
    """Select the Ubuntu Docker implementation."""
    component = DockerEngine()

    implementation = Resolver().resolve(component, system)

    assert isinstance(implementation, UbuntuDockerEngine)
