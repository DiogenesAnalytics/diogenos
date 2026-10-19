"""Test the Docker feature."""

import pytest

from diogenos.component.catalog.docker.engine import DockerEngine
from diogenos.feature.catalog.docker import Docker


@pytest.mark.feature
def test_docker_contains_docker_engine() -> None:
    """Verify that the Docker feature contains the Docker Engine component."""
    feature = Docker()

    assert len(feature.components) == 1
    assert isinstance(feature.components[0], DockerEngine)
