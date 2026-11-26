"""Test the Keyd application mapper component."""

import subprocess
from typing import List

import pytest

from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    KEYD_EXTENSION_SOURCE,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    KEYD_EXTENSION_UUID,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import SERVICE_CONTENT
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    SERVICE_DIRECTORY,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import SERVICE_PATH
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    KeydApplicationMapper,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    UbuntuKeydApplicationMapper,
)
from diogenos.component.catalog.keyboard.keyd.application_mapper import (
    _get_extension_directory,
)
from diogenos.system.base import System
from tests.component.support import RunStub


class ApplicationMapperRunStub(RunStub):
    """Stub subprocess.run with command-specific results."""

    def __init__(
        self,
        extension_enabled: bool = True,
        service_enabled: bool = True,
        service_active: bool = True,
    ) -> None:
        """Initialize the stub."""
        super().__init__()
        self.extension_enabled = extension_enabled
        self.service_enabled = service_enabled
        self.service_active = service_active

    def __call__(
        self,
        command: List[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """Record a command and return a simulated result."""
        returncode = 0
        stdout = ""

        if command == ["gnome-extensions", "info", KEYD_EXTENSION_UUID]:
            if self.extension_enabled:
                stdout = "Enabled: Yes\nState: ACTIVE\n"
            else:
                stdout = "Enabled: No\nState: INACTIVE\n"
                returncode = 1

        elif command == [
            "systemctl",
            "--user",
            "is-enabled",
            "keyd-application-mapper.service",
        ]:
            returncode = 0 if self.service_enabled else 1

        elif command == [
            "systemctl",
            "--user",
            "is-active",
            "keyd-application-mapper.service",
        ]:
            returncode = 0 if self.service_active else 1

        self.calls.append((command, kwargs))

        result = subprocess.CompletedProcess(
            args=command,
            returncode=returncode,
            stdout=stdout,
            stderr="",
        )

        if kwargs.get("check", False) and returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=returncode,
                cmd=command,
                output=stdout,
                stderr="",
            )

        return result


@pytest.mark.component
def test_application_mapper_registry_id() -> None:
    """Test the application mapper registry ID."""
    assert KeydApplicationMapper.registry_id == "keyd.application_mapper"


@pytest.mark.component
def test_application_mapper_dependencies() -> None:
    """Test the application mapper dependency."""
    component = KeydApplicationMapper()

    dependencies = component.dependencies()

    assert len(dependencies) == 1
    assert dependencies[0].name == "keyd.config.user"


@pytest.mark.component
def test_application_mapper_is_satisfied(
    system: System,
) -> None:
    """Test that the application mapper is satisfied."""
    run_stub = ApplicationMapperRunStub()
    component = KeydApplicationMapper(run=run_stub)

    assert component.is_satisfied(system) is True


@pytest.mark.component
def test_application_mapper_is_not_satisfied_when_extension_is_disabled(
    system: System,
) -> None:
    """Test that a disabled extension makes the component unsatisfied."""
    run_stub = ApplicationMapperRunStub(extension_enabled=False)
    component = KeydApplicationMapper(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_application_mapper_is_not_satisfied_when_service_is_disabled(
    system: System,
) -> None:
    """Test that a disabled service makes the component unsatisfied."""
    run_stub = ApplicationMapperRunStub(service_enabled=False)
    component = KeydApplicationMapper(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_application_mapper_is_not_satisfied_when_service_is_inactive(
    system: System,
) -> None:
    """Test that an inactive service makes the component unsatisfied."""
    run_stub = ApplicationMapperRunStub(service_active=False)
    component = KeydApplicationMapper(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_application_mapper_implementations(
    system: System,
) -> None:
    """Test that the Ubuntu implementation is available."""
    component = KeydApplicationMapper()

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuKeydApplicationMapper)
    assert implementations[0].supports(system)


@pytest.mark.component
def test_ubuntu_application_mapper_install(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test installing the Keyd application mapper."""
    implementation = UbuntuKeydApplicationMapper(run=run_stub)

    implementation.install(system)

    extension_directory = _get_extension_directory()

    assert run_stub.calls == [
        (
            ["rm", "-rf", str(extension_directory)],
            {"check": True},
        ),
        (
            ["mkdir", "-p", str(extension_directory.parent)],
            {"check": True},
        ),
        (
            [
                "cp",
                "-r",
                str(KEYD_EXTENSION_SOURCE),
                str(extension_directory),
            ],
            {"check": True},
        ),
        (
            ["gnome-extensions", "enable", KEYD_EXTENSION_UUID],
            {"check": True},
        ),
        (
            ["mkdir", "-p", str(SERVICE_DIRECTORY)],
            {"check": True},
        ),
        (
            ["tee", str(SERVICE_PATH)],
            {
                "input": SERVICE_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (
            ["systemctl", "--user", "daemon-reload"],
            {"check": True},
        ),
        (
            [
                "systemctl",
                "--user",
                "enable",
                "--now",
                "keyd-application-mapper.service",
            ],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_application_mapper_verify(
    system: System,
) -> None:
    """Test verifying the Keyd application mapper."""
    run_stub = ApplicationMapperRunStub()
    implementation = UbuntuKeydApplicationMapper(run=run_stub)

    assert implementation.verify(system) is True


@pytest.mark.component
def test_ubuntu_application_mapper_verify_failure(
    system: System,
) -> None:
    """Test failed verification of the Keyd application mapper."""
    run_stub = ApplicationMapperRunStub(service_active=False)
    implementation = UbuntuKeydApplicationMapper(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_application_mapper_install_failure(
    system: System,
) -> None:
    """Test that an installation failure raises an error."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuKeydApplicationMapper(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
