"""Test the Tmux configuration component and its implementation."""

import subprocess
from pathlib import Path

import pytest

from diogenos.component.catalog.tmux.config import REPOSITORY
from diogenos.component.catalog.tmux.config import AlpineTmuxConfig
from diogenos.component.catalog.tmux.config import ArchTmuxConfig
from diogenos.component.catalog.tmux.config import DebianTmuxConfig
from diogenos.component.catalog.tmux.config import FedoraTmuxConfig
from diogenos.component.catalog.tmux.config import OpenSUSETmuxConfig
from diogenos.component.catalog.tmux.config import TmuxConfig
from diogenos.component.catalog.tmux.config import UbuntuTmuxConfig
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_tmux_config_declares_git_dependency() -> None:
    """Verify that Tmux configuration depends on Git."""
    component = TmuxConfig()

    dependencies = component.dependencies()

    assert len(dependencies) == 1
    assert dependencies[0].name == "git"


@pytest.mark.component
def test_tmux_config_returns_implementations(
    system: System,
) -> None:
    """Verify that Tmux configuration exposes supported implementations."""
    component = TmuxConfig()

    implementations = component.implementations()

    assert len(implementations) == 6
    assert any(isinstance(item, UbuntuTmuxConfig) for item in implementations)
    assert any(isinstance(item, DebianTmuxConfig) for item in implementations)
    assert any(isinstance(item, FedoraTmuxConfig) for item in implementations)
    assert any(isinstance(item, ArchTmuxConfig) for item in implementations)
    assert any(isinstance(item, OpenSUSETmuxConfig) for item in implementations)
    assert any(isinstance(item, AlpineTmuxConfig) for item in implementations)

    ubuntu = next(
        item for item in implementations if isinstance(item, UbuntuTmuxConfig)
    )
    assert ubuntu.supports(system)


@pytest.mark.component
def test_tmux_config_is_satisfied_when_configuration_exists(
    system: System,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that Tmux configuration is satisfied when fully installed."""
    home = tmp_path
    repository = home / ".tmux"
    repository.mkdir()
    (repository / ".tmux.conf").touch()
    (home / ".tmux.conf.local").touch()
    (home / ".tmux.conf").symlink_to(".tmux/.tmux.conf")
    monkeypatch.setattr(Path, "home", lambda: home)

    component = TmuxConfig()

    assert component.is_satisfied(system) is True


@pytest.mark.component
def test_tmux_config_is_not_satisfied_when_configuration_is_missing(
    system: System,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that Tmux configuration is not satisfied when absent."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    component = TmuxConfig()

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_ubuntu_tmux_config_installs_configuration(
    system: System,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Tmux configuration runs the expected commands."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    implementation = UbuntuTmuxConfig(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["git", "clone", REPOSITORY],
            {
                "check": True,
                "cwd": tmp_path,
            },
        ),
        (
            ["ln", "-s", "-f", ".tmux/.tmux.conf", ".tmux.conf"],
            {
                "check": True,
                "cwd": tmp_path,
            },
        ),
        (
            ["cp", ".tmux/.tmux.conf.local", ".tmux.conf.local"],
            {
                "check": True,
                "cwd": tmp_path,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_tmux_config_verifies_successful_installation(
    system: System,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that Ubuntu Tmux configuration reports success."""
    repository = tmp_path / ".tmux"
    repository.mkdir()
    (repository / ".tmux.conf").touch()
    (tmp_path / ".tmux.conf.local").touch()
    (tmp_path / ".tmux.conf").symlink_to(".tmux/.tmux.conf")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    implementation = UbuntuTmuxConfig()

    assert implementation.verify(system) is True


@pytest.mark.component
def test_ubuntu_tmux_config_verifies_failed_installation(
    system: System,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that Ubuntu Tmux configuration reports failure."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    implementation = UbuntuTmuxConfig()

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_tmux_config_installation_propagates_command_failure(
    system: System,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    run_stub: RunStub,
) -> None:
    """Verify that a Git failure interrupts configuration installation."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    run_stub.returncode = 1
    implementation = UbuntuTmuxConfig(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert len(run_stub.calls) == 1
