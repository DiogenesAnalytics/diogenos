"""Test the Emacs keymap component."""

import subprocess
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.keyboard.keyd import EmacsKeymap
from diogenos.component.catalog.keyboard.keyd import UbuntuEmacsKeymap
from diogenos.component.catalog.keyboard.keyd.configuration import CONFIGURATION_PATH
from diogenos.component.catalog.keyboard.keyd.emacs_keymap import KEYMAP_CONTENT
from diogenos.component.catalog.keyboard.keyd.emacs_keymap import KEYMAP_PATH
from diogenos.system.base import System
from tests.component.support import RunStub


def install_keymap_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    content: str,
) -> None:
    """Create a temporary keymap file and patch its path."""
    keymap_path = tmp_path / "diogenos-emacs"
    keymap_path.write_text(content, encoding="utf-8")

    monkeypatch.setattr(
        "diogenos.component.catalog.keyboard.keyd.emacs_keymap.KEYMAP_PATH",
        keymap_path,
    )


@pytest.mark.component
def test_emacs_keymap_registry_id() -> None:
    """Test the Emacs keymap registry ID."""
    assert EmacsKeymap.registry_id == "keyd.keymap.emacs"


@pytest.mark.component
def test_emacs_keymap_is_satisfied(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that the Emacs keymap is satisfied when installed and valid."""
    install_keymap_file(tmp_path, monkeypatch, KEYMAP_CONTENT)
    component = EmacsKeymap(run=run_stub)

    assert component.is_satisfied(system) is True


@pytest.mark.component
def test_emacs_keymap_is_not_satisfied_when_empty(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that an empty Emacs keymap is not satisfied."""
    install_keymap_file(tmp_path, monkeypatch, "")
    component = EmacsKeymap(run=run_stub)

    assert component.is_satisfied(system) is False
    assert run_stub.calls == []


@pytest.mark.component
def test_emacs_keymap_is_not_satisfied_when_incorrect(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that an incorrect Emacs keymap is not satisfied."""
    install_keymap_file(tmp_path, monkeypatch, "[control]\nb = b\n")
    component = EmacsKeymap(run=run_stub)

    assert component.is_satisfied(system) is False
    assert run_stub.calls == []


@pytest.mark.component
def test_emacs_keymap_is_not_satisfied_when_configuration_is_invalid(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that an invalid Keyd configuration is not satisfied."""
    install_keymap_file(tmp_path, monkeypatch, KEYMAP_CONTENT)
    run_stub.returncode = 1
    component = EmacsKeymap(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_emacs_keymap_implementations(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that the Emacs keymap provides an implementation for Ubuntu."""
    component = EmacsKeymap(run=run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_emacs_keymap_install(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test installing the Emacs keymap on Ubuntu."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuEmacsKeymap(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["tee", KEYMAP_PATH],
            {
                "input": KEYMAP_CONTENT,
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
            ["keyd", "reload"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_emacs_keymap_install_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that installing the Emacs keymap uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuEmacsKeymap(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "tee", KEYMAP_PATH],
            {
                "input": KEYMAP_CONTENT,
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
            ["sudo", "keyd", "reload"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_emacs_keymap_verify(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test verifying the Emacs keymap on Ubuntu."""
    install_keymap_file(tmp_path, monkeypatch, KEYMAP_CONTENT)
    implementation = UbuntuEmacsKeymap(run=run_stub)

    assert implementation.verify(system) is True


@pytest.mark.component
def test_ubuntu_emacs_keymap_verify_failure(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test failed verification of the Emacs keymap on Ubuntu."""
    install_keymap_file(tmp_path, monkeypatch, KEYMAP_CONTENT)
    run_stub.returncode = 1
    implementation = UbuntuEmacsKeymap(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_emacs_keymap_verify_missing_file(
    system: System,
    run_stub: RunStub,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test verification fails when the Emacs keymap file is missing."""
    monkeypatch.setattr(
        "diogenos.component.catalog.keyboard.keyd.emacs_keymap.KEYMAP_PATH",
        tmp_path / "missing",
    )
    implementation = UbuntuEmacsKeymap(run=run_stub)

    assert implementation.verify(system) is False
    assert run_stub.calls == []


@pytest.mark.component
def test_ubuntu_emacs_keymap_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that a failed Emacs keymap installation raises an error."""
    run_stub.returncode = 1
    implementation = UbuntuEmacsKeymap(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_emacs_keymap_dependencies() -> None:
    """Verify that the Emacs keymap depends on Keyd configuration."""
    component = EmacsKeymap()

    dependencies = component.dependencies()

    assert len(dependencies) == 1
    assert dependencies[0].name == "keyd.config"
