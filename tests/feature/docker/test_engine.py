"""Test the Docker Engine component."""

import subprocess

import pytest

from diogenos.feature.component import UbuntuComponentImplementation
from diogenos.feature.docker.engine import DockerEngine
from diogenos.feature.docker.engine import UbuntuDockerEngine
from diogenos.system.base import System


@pytest.mark.component
@pytest.mark.feature
def test_docker_engine_is_satisfied(
    system: System,
) -> None:
    """Test that Docker Engine is satisfied when hello-world succeeds."""

    def run(
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
        )

    component = DockerEngine(run=run)

    assert component.is_satisfied(system) is True


@pytest.mark.component
@pytest.mark.feature
def test_docker_engine_is_not_satisfied(
    system: System,
) -> None:
    """Test that Docker Engine is not satisfied when hello-world fails."""

    def run(
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=command,
            returncode=1,
        )

    component = DockerEngine(run=run)

    assert component.is_satisfied(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_docker_engine_returns_ubuntu_implementation() -> None:
    """Test that Docker Engine provides its Ubuntu implementation."""
    component = DockerEngine()

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuDockerEngine)


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_docker_engine_is_ubuntu_implementation() -> None:
    """Test that UbuntuDockerEngine uses the Ubuntu implementation."""
    assert issubclass(
        UbuntuDockerEngine,
        UbuntuComponentImplementation,
    )
