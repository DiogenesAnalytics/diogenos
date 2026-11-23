"""Test the macOS keymap component."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.keyboard.keyd import MacOSKeymap
from diogenos.component.catalog.keyboard.keyd import UbuntuMacOSKeymap
from diogenos.component.catalog.keyboard.keyd.configuration import CONFIGURATION_PATH
from diogenos.component.catalog.keyboard.keyd.macos_keymap import KEYMAP_CONTENT
from diogenos.component.catalog.keyboard.keyd.macos_keymap import KEYMAP_PATH
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_macos_keymap_registry_id() -> None:
    """Verify the macOS keymap registry ID."""
    assert MacOSKeymap.registry_id == "keyd.keymap.macos"


@pytest.mark.component
def test_macos_keymap_dependencies() -> None:
    """Verify that the macOS keymap depends on Keyd configuration."""
    component = MacOSKeymap()

    dependencies = component.dependencies()

    assert len(dependencies) == 1
    assert dependencies[0].name == "keyd.config"


@pytest.mark.component
def test_macos_keymap_is_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that the macOS keymap is satisfied when its configuration is valid."""
    component = MacOSKeymap(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["keyd", "check", CONFIGURATION_PATH],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_macos_keymap_is_not_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify macOS keymap not satisfied when its configuration is invalid."""
    run_stub.returncode = 1
    component = MacOSKeymap(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_macos_keymap_implementations(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that the macOS keymap provides an Ubuntu implementation."""
    component = MacOSKeymap(run=run_stub)

    implementations = component.implementations()

    assert len(implementations) == 1
    assert isinstance(implementations[0], UbuntuMacOSKeymap)
    assert implementations[0].supports(system)


@pytest.mark.component
def test_ubuntu_macos_keymap_install(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify installing the macOS keymap on Ubuntu."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuMacOSKeymap(run=run_stub)

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
def test_ubuntu_macos_keymap_install_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that installation uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuMacOSKeymap(run=run_stub)

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
def test_ubuntu_macos_keymap_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify the macOS keymap implementation."""
    implementation = UbuntuMacOSKeymap(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["keyd", "check", CONFIGURATION_PATH],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_macos_keymap_verify_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that failed configuration validation is reported."""
    run_stub.returncode = 1
    implementation = UbuntuMacOSKeymap(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_macos_keymap_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that installation propagates command failures."""
    run_stub.returncode = 1
    implementation = UbuntuMacOSKeymap(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
