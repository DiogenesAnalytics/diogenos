"""Test the Docker Engine component."""

import subprocess

import pytest

from diogenos.feature.docker.engine import DockerEngine
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
