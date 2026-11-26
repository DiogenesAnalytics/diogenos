"""Test the Keyd configuration component."""

import subprocess
from typing import Any
from typing import Sequence

import pytest

from diogenos.component.catalog.keyboard.keyd.configuration import CONFIGURATION_CONTENT
from diogenos.component.catalog.keyboard.keyd.configuration import CONFIGURATION_PATH
from diogenos.component.catalog.keyboard.keyd.configuration import EMACS_KEYMAP_PATH
from diogenos.component.catalog.keyboard.keyd.configuration import MACOS_KEYMAP_PATH
from diogenos.component.catalog.keyboard.keyd.configuration import KeydConfiguration
from diogenos.component.catalog.keyboard.keyd.configuration import (
    UbuntuKeydConfiguration,
)
from diogenos.component.implementation.execution import prepare_command
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def configuration_run_stub() -> RunStub:
    """Return a stub for Keyd configuration commands."""
    return RunStub()


def test_registry_id() -> None:
    """Test the component registry ID."""
    assert KeydConfiguration.registry_id == "keyd.config"


def test_dependencies(
    configuration_run_stub: RunStub,
) -> None:
    """Test the component dependencies."""
    component = KeydConfiguration(run=configuration_run_stub)

    assert tuple(dependency.name for dependency in component.dependencies()) == (
        "keyd",
    )


def test_is_satisfied(
    configuration_run_stub: RunStub,
    system: System,
) -> None:
    """Test that a valid configuration is satisfied."""
    component = KeydConfiguration(run=configuration_run_stub)

    assert component.is_satisfied(system)
    assert configuration_run_stub.calls == [
        (
            ["keyd", "check", CONFIGURATION_PATH],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        )
    ]


def test_is_not_satisfied(
    configuration_run_stub: RunStub,
    system: System,
) -> None:
    """Test that an invalid configuration is not satisfied."""
    configuration_run_stub.returncode = 1
    component = KeydConfiguration(run=configuration_run_stub)

    assert not component.is_satisfied(system)


def test_implementations(
    configuration_run_stub: RunStub,
    system: System,
) -> None:
    """Test the available component implementations."""
    component = KeydConfiguration(run=configuration_run_stub)

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuKeydConfiguration)
    assert implementations[0].supports(system)


def test_install(
    configuration_run_stub: RunStub,
    system: System,
) -> None:
    """Test installation of the shared Keyd configuration."""
    implementation = UbuntuKeydConfiguration(
        run=configuration_run_stub,
    )

    implementation.install(system)

    assert configuration_run_stub.calls == [
        (
            prepare_command(["touch", EMACS_KEYMAP_PATH], privileged=True),
            {"check": True},
        ),
        (
            prepare_command(["touch", MACOS_KEYMAP_PATH], privileged=True),
            {"check": True},
        ),
        (
            prepare_command(["tee", CONFIGURATION_PATH], privileged=True),
            {
                "input": CONFIGURATION_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (
            ["keyd", "check", CONFIGURATION_PATH],
            {
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (
            prepare_command(["keyd", "reload"], privileged=True),
            {"check": True},
        ),
    ]


def test_install_invalid_configuration(
    system: System,
) -> None:
    """Test that an invalid configuration is not reloaded."""
    calls = []

    def run(
        command: Sequence[str],
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[str]:
        calls.append((list(command), kwargs))

        returncode = int(command == ["keyd", "check", CONFIGURATION_PATH])
        result = subprocess.CompletedProcess(
            args=list(command),
            returncode=returncode,
            stdout="",
            stderr="",
        )

        if kwargs.get("check") and returncode:
            raise subprocess.CalledProcessError(returncode, command)

        return result

    implementation = UbuntuKeydConfiguration(run=run)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert calls[-1][0] == ["keyd", "check", CONFIGURATION_PATH]
    assert not any(call[0][-2:] == ["keyd", "reload"] for call in calls)


def test_verify(
    configuration_run_stub: RunStub,
    system: System,
) -> None:
    """Test verification of the shared Keyd configuration."""
    implementation = UbuntuKeydConfiguration(
        run=configuration_run_stub,
    )

    assert implementation.verify(system)


def test_verify_invalid_configuration(
    configuration_run_stub: RunStub,
    system: System,
) -> None:
    """Test verification of an invalid Keyd configuration."""
    configuration_run_stub.returncode = 1
    implementation = UbuntuKeydConfiguration(
        run=configuration_run_stub,
    )

    assert not implementation.verify(system)


def test_install_failure(
    system: System,
) -> None:
    """Test that installation fails when a command fails."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuKeydConfiguration(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
