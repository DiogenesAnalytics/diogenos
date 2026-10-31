"""Test the Docker Engine component."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component import UbuntuComponentImplementation
from diogenos.component.catalog.docker.engine import DockerEngine
from diogenos.component.catalog.docker.engine import UbuntuDockerEngine
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_docker_engine_is_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Docker Engine is satisfied when hello-world succeeds."""
    component = DockerEngine(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["docker", "info"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_docker_engine_is_not_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Docker Engine is not satisfied when hello-world fails."""
    run_stub.returncode = 1
    component = DockerEngine(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_docker_engine_returns_ubuntu_implementation() -> None:
    """Verify that Docker Engine provides its Ubuntu implementation."""
    component = DockerEngine()

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuDockerEngine)


@pytest.mark.component
def test_ubuntu_docker_engine_is_ubuntu_implementation() -> None:
    """Verify that UbuntuDockerEngine uses the Ubuntu implementation."""
    assert issubclass(
        UbuntuDockerEngine,
        UbuntuComponentImplementation,
    )


@pytest.mark.component
def test_ubuntu_docker_engine_installs_docker(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that UbuntuDockerEngine installs Docker Engine."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuDockerEngine(run=run_stub)

    implementation.install(system)

    assert [command for command, _ in run_stub.calls] == [
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


@pytest.mark.component
def test_ubuntu_docker_engine_installs_docker_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Docker Engine installation uses sudo when not root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuDockerEngine(run=run_stub)

    implementation.install(system)

    assert [command for command, _ in run_stub.calls] == [
        ["sudo", "apt-get", "update"],
        [
            "sudo",
            "apt-get",
            "install",
            "-y",
            "ca-certificates",
            "curl",
        ],
        [
            "sudo",
            "install",
            "-m",
            "0755",
            "-d",
            "/etc/apt/keyrings",
        ],
        [
            "sudo",
            "curl",
            "-fsSL",
            "https://download.docker.com/linux/ubuntu/gpg",
            "-o",
            "/etc/apt/keyrings/docker.asc",
        ],
        [
            "sudo",
            "chmod",
            "a+r",
            "/etc/apt/keyrings/docker.asc",
        ],
        [
            "sudo",
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
        ["sudo", "apt-get", "update"],
        [
            "sudo",
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


@pytest.mark.component
def test_ubuntu_docker_engine_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Docker Engine installation."""
    run_stub.returncode = 1
    implementation = UbuntuDockerEngine(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
