"""Test the Docker Engine component."""

import subprocess

import pytest

from diogenos.feature.catalog.docker.engine import DockerEngine
from diogenos.feature.catalog.docker.engine import UbuntuDockerEngine
from diogenos.feature.component import UbuntuComponentImplementation
from diogenos.system.base import System


class RunStub:
    """Capture subprocess calls."""

    def __init__(self) -> None:
        """Initialize the stub."""
        self.commands: list[list[str]] = []

    def __call__(
        self,
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """Capture a subprocess call."""
        self.commands.append(command)

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
        )


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


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_docker_engine_installs_docker(
    system: System,
) -> None:
    """Test that UbuntuDockerEngine installs Docker Engine."""
    run = RunStub()
    implementation = UbuntuDockerEngine(run=run)

    implementation.install(system)

    assert run.commands == [
        ["apt-get", "update"],
        [
            "apt-get",
            "install",
            "-y",
            "ca-certificates",
            "curl",
        ],
        [
            "install",
            "-m",
            "0755",
            "-d",
            "/etc/apt/keyrings",
        ],
        [
            "curl",
            "-fsSL",
            "https://download.docker.com/linux/ubuntu/gpg",
            "-o",
            "/etc/apt/keyrings/docker.asc",
        ],
        [
            "chmod",
            "a+r",
            "/etc/apt/keyrings/docker.asc",
        ],
        [
            "sh",
            "-c",
            (
                "echo "
                "'deb [arch=amd64 "
                "signed-by=/etc/apt/keyrings/docker.asc] "
                "https://download.docker.com/linux/ubuntu "
                "noble stable' "
                "> /etc/apt/sources.list.d/docker.list"
            ),
        ],
        ["apt-get", "update"],
        [
            "apt-get",
            "install",
            "-y",
            "docker-ce",
            "docker-ce-cli",
            "containerd.io",
            "docker-buildx-plugin",
            "docker-compose-plugin",
        ],
    ]
