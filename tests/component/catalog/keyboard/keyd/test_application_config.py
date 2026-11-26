"""Test the Keyd application configuration component."""

import subprocess
from pathlib import Path

import pytest
from pytest import MonkeyPatch

import diogenos.component.catalog.keyboard.keyd.application_config as application_config
from diogenos.component.catalog.keyboard.keyd.application_config import (
    APPLICATION_CONFIG_CONTENT,
)
from diogenos.component.catalog.keyboard.keyd.application_config import (
    APPLICATION_CONFIG_PATH,
)
from diogenos.component.catalog.keyboard.keyd.application_config import (
    KeydApplicationConfig,
)
from diogenos.component.catalog.keyboard.keyd.application_config import (
    UbuntuKeydApplicationConfig,
)
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def application_config_run_stub() -> RunStub:
    """Return a stub for Keyd application configuration commands."""
    return RunStub()


@pytest.mark.component
def test_registry_id() -> None:
    """Test the component registry ID."""
    assert KeydApplicationConfig.registry_id == "keyd.config.application"


@pytest.mark.component
def test_dependencies(
    application_config_run_stub: RunStub,
) -> None:
    """Test the component dependencies."""
    component = KeydApplicationConfig(run=application_config_run_stub)

    assert tuple(dependency.name for dependency in component.dependencies()) == (
        "keyd",
    )


@pytest.mark.component
def test_is_satisfied(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test that an installed application configuration is satisfied."""
    path = tmp_path / "app.conf"
    path.write_text(APPLICATION_CONFIG_CONTENT, encoding="utf-8")
    monkeypatch.setattr(application_config, "APPLICATION_CONFIG_PATH", path)

    component = KeydApplicationConfig(run=application_config_run_stub)

    assert component.is_satisfied(system)


@pytest.mark.component
def test_is_not_satisfied(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test that a missing application configuration is not satisfied."""
    path = tmp_path / "app.conf"
    monkeypatch.setattr(application_config, "APPLICATION_CONFIG_PATH", path)

    component = KeydApplicationConfig(run=application_config_run_stub)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_is_not_satisfied_with_different_content(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test that an incorrect application configuration is not satisfied."""
    path = tmp_path / "app.conf"
    path.write_text("[some-other-application]\n", encoding="utf-8")
    monkeypatch.setattr(application_config, "APPLICATION_CONFIG_PATH", path)

    component = KeydApplicationConfig(run=application_config_run_stub)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_implementations(
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test the available component implementations."""
    component = KeydApplicationConfig(run=application_config_run_stub)

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuKeydApplicationConfig)
    assert implementations[0].supports(system)


@pytest.mark.component
def test_install(
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test installation of the application configuration."""
    implementation = UbuntuKeydApplicationConfig(
        run=application_config_run_stub,
    )

    implementation.install(system)

    assert application_config_run_stub.calls == [
        (
            ["mkdir", "-p", str(APPLICATION_CONFIG_PATH.parent)],
            {"check": True},
        ),
        (
            ["tee", str(APPLICATION_CONFIG_PATH)],
            {
                "input": APPLICATION_CONFIG_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_verify(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test verification of the application configuration."""
    path = tmp_path / "app.conf"
    path.write_text(APPLICATION_CONFIG_CONTENT, encoding="utf-8")
    monkeypatch.setattr(application_config, "APPLICATION_CONFIG_PATH", path)

    implementation = UbuntuKeydApplicationConfig(
        run=application_config_run_stub,
    )

    assert implementation.verify(system)


@pytest.mark.component
def test_verify_invalid_configuration(
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
    application_config_run_stub: RunStub,
    system: System,
) -> None:
    """Test verification of an invalid application configuration."""
    path = tmp_path / "app.conf"
    monkeypatch.setattr(application_config, "APPLICATION_CONFIG_PATH", path)

    implementation = UbuntuKeydApplicationConfig(
        run=application_config_run_stub,
    )

    assert not implementation.verify(system)


@pytest.mark.component
def test_install_failure(
    system: System,
) -> None:
    """Test that installation fails when a command fails."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuKeydApplicationConfig(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
