"""Test Keyd user configuration."""

import subprocess
from typing import List

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.keyboard.keyd.user import KeydUserConfig
from diogenos.component.catalog.keyboard.keyd.user import UbuntuKeydUserConfig
from diogenos.system.base import System
from tests.component.support import RunStub


class KeydUserRunStub(RunStub):
    """Stub subprocess.run with command-specific results."""

    def __init__(
        self,
        group_exists: bool = True,
        user_in_group: bool = True,
    ) -> None:
        """Initialize the stub."""
        super().__init__()
        self.group_exists = group_exists
        self.user_in_group = user_in_group

    def __call__(
        self,
        command: List[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """Record a command and return a simulated result."""
        if command == ["getent", "group", "keyd"]:
            returncode = 0 if self.group_exists else 2
            stdout = "keyd:x:999:\n" if self.group_exists else ""
        elif len(command) == 3 and command[:2] == ["id", "-nG"]:
            returncode = 0
            stdout = "testuser keyd\n" if self.user_in_group else "testuser\n"
        else:
            returncode = 0
            stdout = ""

        self.calls.append((command, kwargs))

        result = subprocess.CompletedProcess(
            args=command,
            returncode=returncode,
            stdout=stdout,
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
def test_keyd_user_config_registry_id() -> None:
    """Test the Keyd user configuration registry ID."""
    assert KeydUserConfig.registry_id == "keyd.config.user"


@pytest.mark.component
def test_keyd_user_config_dependencies() -> None:
    """Test the Keyd user configuration dependency."""
    component = KeydUserConfig(user="testuser")

    dependencies = component.dependencies()

    assert len(dependencies) == 1
    assert dependencies[0].name == "keyd"


@pytest.mark.component
def test_keyd_user_config_is_satisfied(
    system: System,
) -> None:
    """Test satisfaction when the user belongs to the Keyd group."""
    component = KeydUserConfig(
        run=KeydUserRunStub(),
        user="testuser",
    )

    assert component.is_satisfied(system) is True


@pytest.mark.component
def test_keyd_user_config_is_not_satisfied_when_group_is_missing(
    system: System,
) -> None:
    """Test unsatisfied state when the Keyd group does not exist."""
    component = KeydUserConfig(
        run=KeydUserRunStub(group_exists=False),
        user="testuser",
    )

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_keyd_user_config_is_not_satisfied_when_user_is_not_a_member(
    system: System,
) -> None:
    """Test unsatisfied state when the user lacks Keyd group membership."""
    component = KeydUserConfig(
        run=KeydUserRunStub(user_in_group=False),
        user="testuser",
    )

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_keyd_user_config_implementations(
    system: System,
) -> None:
    """Test that the Ubuntu implementation is available."""
    component = KeydUserConfig(user="testuser")

    implementations = component.implementations()

    assert len(implementations) == 1
    assert implementations[0].supports(system)
    assert isinstance(implementations[0], UbuntuKeydUserConfig)


@pytest.mark.component
def test_ubuntu_keyd_user_config_install(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test adding the user to the Keyd group."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    run_stub = KeydUserRunStub(user_in_group=False)
    implementation = UbuntuKeydUserConfig(
        run=run_stub,
        user="testuser",
    )

    implementation.install(system)

    commands = [command for command, _ in run_stub.calls]

    assert ["usermod", "-aG", "keyd", "testuser"] in commands
    assert commands.count(["usermod", "-aG", "keyd", "testuser"]) == 1


@pytest.mark.component
def test_ubuntu_keyd_user_config_install_with_sudo(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that adding the user to Keyd uses sudo when necessary."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    run_stub = KeydUserRunStub(user_in_group=False)
    implementation = UbuntuKeydUserConfig(
        run=run_stub,
        user="testuser",
    )

    implementation.install(system)

    commands = [command for command, _ in run_stub.calls]

    assert ["sudo", "usermod", "-aG", "keyd", "testuser"] in commands


@pytest.mark.component
def test_ubuntu_keyd_user_config_install_does_not_modify_existing_member(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that installation leaves existing group membership unchanged."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    run_stub = KeydUserRunStub()
    implementation = UbuntuKeydUserConfig(
        run=run_stub,
        user="testuser",
    )

    implementation.install(system)

    commands = [command for command, _ in run_stub.calls]

    assert ["usermod", "-aG", "keyd", "testuser"] not in commands


@pytest.mark.component
def test_ubuntu_keyd_user_config_install_fails_when_group_is_missing(
    system: System,
) -> None:
    """Test that installation fails when the Keyd group is missing."""
    implementation = UbuntuKeydUserConfig(
        run=KeydUserRunStub(group_exists=False),
        user="testuser",
    )

    with pytest.raises(RuntimeError, match="Keyd group does not exist"):
        implementation.install(system)


@pytest.mark.component
def test_ubuntu_keyd_user_config_verify(
    system: System,
) -> None:
    """Test verifying Keyd user configuration."""
    implementation = UbuntuKeydUserConfig(
        run=KeydUserRunStub(),
        user="testuser",
    )

    assert implementation.verify(system) is True


@pytest.mark.component
def test_ubuntu_keyd_user_config_verify_failure(
    system: System,
) -> None:
    """Test failed verification when the user lacks group membership."""
    implementation = UbuntuKeydUserConfig(
        run=KeydUserRunStub(user_in_group=False),
        user="testuser",
    )

    assert implementation.verify(system) is False
