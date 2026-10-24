"""Test Docker user configuration."""

import subprocess
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

import pytest

from diogenos.component.catalog.docker.config.user import DockerUserConfig
from diogenos.component.catalog.docker.config.user import UbuntuDockerUserConfig
from diogenos.system.base import System


class DockerUserRunStub:
    """Stub subprocess.run with command-specific results."""

    def __init__(
        self,
        group_exists: bool = True,
        user_in_group: bool = True,
    ) -> None:
        """Initialize the stub."""
        self.group_exists = group_exists
        self.user_in_group = user_in_group
        self.calls: List[Tuple[List[str], Dict[str, Any]]] = []

    def __call__(
        self,
        command: List[str],
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[str]:
        """Record a command and return a simulated result."""
        self.calls.append((command, kwargs))

        if command == ["getent", "group", "docker"]:
            return subprocess.CompletedProcess(
                args=command,
                returncode=0 if self.group_exists else 2,
                stdout="docker:x:999:\n" if self.group_exists else "",
                stderr="",
            )

        if len(command) == 3 and command[:2] == ["id", "-nG"]:
            return subprocess.CompletedProcess(
                args=command,
                returncode=0,
                stdout=("testuser docker\n" if self.user_in_group else "testuser\n"),
                stderr="",
            )

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="",
            stderr="",
        )


@pytest.fixture
def run_stub_factory() -> Callable[..., DockerUserRunStub]:
    """Provide a factory for Docker command stubs."""
    return DockerUserRunStub


@pytest.mark.component
def test_is_satisfied_when_user_belongs_to_docker_group(
    system: System,
    run_stub_factory: Callable[..., DockerUserRunStub],
) -> None:
    """Test satisfaction when the Docker group contains the user."""
    run_stub = run_stub_factory()
    component = DockerUserConfig(run=run_stub, user="testuser")

    assert component.is_satisfied(system)


@pytest.mark.component
def test_is_not_satisfied_when_docker_group_does_not_exist(
    system: System,
    run_stub_factory: Callable[..., DockerUserRunStub],
) -> None:
    """Test unsatisfied state when the Docker group does not exist."""
    run_stub = run_stub_factory(group_exists=False)
    component = DockerUserConfig(run=run_stub, user="testuser")

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_is_not_satisfied_when_user_is_not_in_docker_group(
    system: System,
    run_stub_factory: Callable[..., DockerUserRunStub],
) -> None:
    """Test unsatisfied state when the user lacks Docker group membership."""
    run_stub = run_stub_factory(user_in_group=False)
    component = DockerUserConfig(run=run_stub, user="testuser")

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_implementations_returns_ubuntu_implementation() -> None:
    """Test that the Ubuntu implementation is available."""
    component = DockerUserConfig(user="testuser")

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuDockerUserConfig)


@pytest.mark.component
def test_install_creates_group_and_adds_user(
    system: System,
    run_stub_factory: Callable[..., DockerUserRunStub],
) -> None:
    """Test installation creates the group and adds the user."""
    run_stub = run_stub_factory(
        group_exists=False,
        user_in_group=False,
    )
    implementation = UbuntuDockerUserConfig(
        run=run_stub,
        user="testuser",
    )

    implementation.install(system)

    commands = [command for command, _ in run_stub.calls]

    assert ["groupadd", "docker"] in commands
    assert ["usermod", "-aG", "docker", "testuser"] in commands


@pytest.mark.component
def test_install_does_not_create_existing_group(
    system: System,
    run_stub_factory: Callable[..., DockerUserRunStub],
) -> None:
    """Test installation does not recreate the Docker group."""
    run_stub = run_stub_factory(user_in_group=False)
    implementation = UbuntuDockerUserConfig(
        run=run_stub,
        user="testuser",
    )

    implementation.install(system)

    commands = [command for command, _ in run_stub.calls]

    assert ["groupadd", "docker"] not in commands
    assert ["usermod", "-aG", "docker", "testuser"] in commands


@pytest.mark.component
def test_install_does_not_add_existing_member(
    system: System,
    run_stub_factory: Callable[..., DockerUserRunStub],
) -> None:
    """Test installation does not modify existing group membership."""
    run_stub = run_stub_factory()
    implementation = UbuntuDockerUserConfig(
        run=run_stub,
        user="testuser",
    )

    implementation.install(system)

    commands = [command for command, _ in run_stub.calls]

    assert ["groupadd", "docker"] not in commands
    assert ["usermod", "-aG", "docker", "testuser"] not in commands
