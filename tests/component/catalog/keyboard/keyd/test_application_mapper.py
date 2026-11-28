"""Test the Keyd application mapper component."""

import subprocess
from pathlib import Path
from typing import List

import pytest

import diogenos.component.catalog.keyboard.keyd.application_mapper as application_mapper
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
from diogenos.component.catalog.keyboard.keyd.application_mapper import SERVICE_NAME
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
        service_enabled: bool = True,
    ) -> None:
        """Initialize the stub."""
        super().__init__()
        self.service_enabled = service_enabled

    def __call__(
        self,
        command: List[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """Record a command and return a simulated result."""
        returncode = 0

        if command == [
            "systemctl",
            "--user",
            "is-enabled",
            SERVICE_NAME,
        ]:
            returncode = 0 if self.service_enabled else 1

        self.calls.append((command, kwargs))

        result = subprocess.CompletedProcess(
            args=command,
            returncode=returncode,
            stdout="",
            stderr="",
        )

        if kwargs.get("check", False) and returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=returncode,
                cmd=command,
            )

        return result


@pytest.fixture
def extension_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """Create a temporary Keyd GNOME extension directory."""
    directory = tmp_path / KEYD_EXTENSION_UUID
    directory.mkdir()

    (directory / "extension.js").write_text("", encoding="utf-8")
    (directory / "metadata.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        application_mapper,
        "_get_extension_directory",
        lambda: directory,
    )

    return directory


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
    extension_directory: Path,
) -> None:
    """Test that the installed application mapper is satisfied."""
    run_stub = ApplicationMapperRunStub()
    component = KeydApplicationMapper(run=run_stub)

    assert component.is_satisfied(system) is True


@pytest.mark.component
def test_application_mapper_is_not_satisfied_when_extension_is_missing(
    system: System,
    extension_directory: Path,
) -> None:
    """Test that a missing extension makes the component unsatisfied."""
    (extension_directory / "extension.js").unlink()
    component = KeydApplicationMapper(run=ApplicationMapperRunStub())

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_application_mapper_is_not_satisfied_when_service_is_disabled(
    system: System,
    extension_directory: Path,
) -> None:
    """Test that a disabled service makes the component unsatisfied."""
    run_stub = ApplicationMapperRunStub(service_enabled=False)
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
                SERVICE_NAME,
            ],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_application_mapper_verify(
    system: System,
    extension_directory: Path,
) -> None:
    """Test verifying the installed Keyd application mapper."""
    run_stub = ApplicationMapperRunStub()
    implementation = UbuntuKeydApplicationMapper(run=run_stub)

    assert implementation.verify(system) is True


@pytest.mark.component
def test_ubuntu_application_mapper_verify_failure(
    system: System,
    extension_directory: Path,
) -> None:
    """Test failed verification when the service is disabled."""
    run_stub = ApplicationMapperRunStub(service_enabled=False)
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
