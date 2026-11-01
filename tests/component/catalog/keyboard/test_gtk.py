"""Test the GTK Emacs keymap component."""

import subprocess

import pytest

from diogenos.component.catalog.keyboard.gtk import GTK_KEY_THEME
from diogenos.component.catalog.keyboard.gtk import GTK_KEY_THEME_VALUE
from diogenos.component.catalog.keyboard.gtk import GTK_SCHEMA
from diogenos.component.catalog.keyboard.gtk import GtkEmacsKeymap
from diogenos.component.catalog.keyboard.gtk import UbuntuGtkEmacsKeymap
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gtk_emacs_run_stub(run_stub: RunStub) -> RunStub:
    """Create a subprocess stub that reports the GTK Emacs key theme."""
    run_stub.stdout = "'Emacs'\n"
    return run_stub


@pytest.mark.component
def test_gtk_emacs_keymap_registry_id() -> None:
    """Test the GTK Emacs keymap registry ID."""
    assert GtkEmacsKeymap.registry_id == "gtk_emacs_keymap"


@pytest.mark.component
def test_gtk_emacs_keymap_is_satisfied(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test that the GTK Emacs keymap is satisfied when enabled."""
    component = GtkEmacsKeymap(run=gtk_emacs_run_stub)

    assert component.is_satisfied(system) is True
    assert gtk_emacs_run_stub.calls == [
        (
            ["gsettings", "get", GTK_SCHEMA, GTK_KEY_THEME],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_gtk_emacs_keymap_is_not_satisfied(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test that the GTK Emacs keymap is not satisfied when disabled."""
    gtk_emacs_run_stub.returncode = 1
    component = GtkEmacsKeymap(run=gtk_emacs_run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gtk_emacs_keymap_implementations(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test that the GTK Emacs keymap provides an implementation for Ubuntu."""
    component = GtkEmacsKeymap(run=gtk_emacs_run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_gtk_emacs_keymap_install(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test enabling the GTK Emacs keymap on Ubuntu."""
    implementation = UbuntuGtkEmacsKeymap(run=gtk_emacs_run_stub)

    implementation.install(system)

    assert gtk_emacs_run_stub.calls == [
        (
            [
                "gsettings",
                "set",
                GTK_SCHEMA,
                GTK_KEY_THEME,
                GTK_KEY_THEME_VALUE,
            ],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_gtk_emacs_keymap_verify(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test verifying the GTK Emacs keymap on Ubuntu."""
    implementation = UbuntuGtkEmacsKeymap(run=gtk_emacs_run_stub)

    assert implementation.verify(system) is True
    assert gtk_emacs_run_stub.calls == [
        (
            ["gsettings", "get", GTK_SCHEMA, GTK_KEY_THEME],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gtk_emacs_keymap_verify_failure(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test failed verification of the GTK Emacs keymap on Ubuntu."""
    gtk_emacs_run_stub.returncode = 1
    implementation = UbuntuGtkEmacsKeymap(run=gtk_emacs_run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gtk_emacs_keymap_install_failure(
    system: System,
    gtk_emacs_run_stub: RunStub,
) -> None:
    """Test that a failed GTK Emacs keymap installation raises an error."""
    gtk_emacs_run_stub.returncode = 1
    implementation = UbuntuGtkEmacsKeymap(run=gtk_emacs_run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
