"""Test the Emacs keymap component."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.keyboard.emacs_keymap import KEYMAP_CONTENT
from diogenos.component.catalog.keyboard.emacs_keymap import KEYMAP_PATH
from diogenos.component.catalog.keyboard.emacs_keymap import EmacsKeymap
from diogenos.component.catalog.keyboard.emacs_keymap import UbuntuEmacsKeymap
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_emacs_keymap_registry_id() -> None:
    """Test the Emacs keymap registry ID."""
    assert EmacsKeymap.registry_id == "emacs_keymap"


@pytest.mark.component
def test_emacs_keymap_is_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that the Emacs keymap is satisfied when its configuration is valid."""
    component = EmacsKeymap(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["keyd", "check", KEYMAP_PATH],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_emacs_keymap_is_not_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that the Emacs keymap is not satisfied when its configuration is invalid."""
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
            ["keyd", "check", KEYMAP_PATH],
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
            ["keyd", "check", KEYMAP_PATH],
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
) -> None:
    """Test verifying the Emacs keymap on Ubuntu."""
    implementation = UbuntuEmacsKeymap(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["keyd", "check", KEYMAP_PATH],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_emacs_keymap_verify_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test failed verification of the Emacs keymap on Ubuntu."""
    run_stub.returncode = 1
    implementation = UbuntuEmacsKeymap(run=run_stub)

    assert implementation.verify(system) is False


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
