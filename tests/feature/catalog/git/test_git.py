"""Test the Git component and its implementations."""

import subprocess
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import pytest

from diogenos.feature.catalog.git.git import GitComponent
from diogenos.feature.catalog.git.git import UbuntuGit
from diogenos.system.base import System


class RunStub:
    """Stub subprocess.run and record its calls."""

    def __init__(self, returncode: int = 0) -> None:
        """Initialize the stub with a command return code."""
        self.returncode = returncode
        self.calls: List[Tuple[List[str], Dict[str, Any]]] = []

    def __call__(
        self,
        command: List[str],
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[str]:
        """Record a command and return a simulated result."""
        self.calls.append((command, kwargs))

        result = subprocess.CompletedProcess(
            args=command,
            returncode=self.returncode,
            stdout="",
            stderr="",
        )

        if kwargs.get("check", False) and result.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=result.returncode,
                cmd=command,
                output=result.stdout,
                stderr=result.stderr,
            )

        return result


@pytest.mark.component
@pytest.mark.feature
def test_git_component_is_satisfied_when_git_is_available(
    system: System,
) -> None:
    """Verify that Git is satisfied when git --version succeeds."""
    run = RunStub()
    component = GitComponent(run=run)

    assert component.is_satisfied(system) is True
    assert run.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_git_component_is_not_satisfied_when_git_is_unavailable(
    system: System,
) -> None:
    """Verify that Git is not satisfied when git --version fails."""
    run = RunStub(returncode=127)
    component = GitComponent(run=run)

    assert component.is_satisfied(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_git_component_returns_ubuntu_implementation(
    system: System,
) -> None:
    """Verify that the Git component exposes its Ubuntu implementation."""
    component = GitComponent()

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuGit)
    assert implementations[0].supports(system) is True


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_git_installs_git(system: System) -> None:
    """Verify that Ubuntu Git installation runs the expected commands."""
    run = RunStub()
    implementation = UbuntuGit(run=run)

    implementation.install(system)

    assert run.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "git"],
            {"check": True},
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_git_verifies_successful_installation(
    system: System,
) -> None:
    """Verify that Git installation succeeds when git --version succeeds."""
    run = RunStub()
    implementation = UbuntuGit(run=run)

    assert implementation.verify(system) is True
    assert run.calls == [
        (
            ["git", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_git_verifies_failed_installation(
    system: System,
) -> None:
    """Verify that Git installation fails when git --version fails."""
    run = RunStub(returncode=127)
    implementation = UbuntuGit(run=run)

    assert implementation.verify(system) is False


@pytest.mark.component
@pytest.mark.feature
def test_ubuntu_git_installation_propagates_command_failure(
    system: System,
) -> None:
    """Verify that an APT failure interrupts Git installation."""
    run = RunStub(returncode=1)
    implementation = UbuntuGit(run=run)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
