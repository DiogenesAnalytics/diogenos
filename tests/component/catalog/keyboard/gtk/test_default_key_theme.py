"""Test the GTK default key theme component."""

import subprocess

import pytest

from diogenos.component.catalog.keyboard.gtk.default_key_theme import GTK_KEY_THEME
from diogenos.component.catalog.keyboard.gtk.default_key_theme import (
    GTK_KEY_THEME_VALUE,
)
from diogenos.component.catalog.keyboard.gtk.default_key_theme import GTK_SCHEMA
from diogenos.component.catalog.keyboard.gtk.default_key_theme import GtkDefaultKeyTheme
from diogenos.component.catalog.keyboard.gtk.default_key_theme import (
    UbuntuGtkDefaultKeyTheme,
)
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gtk_default_run_stub(run_stub: RunStub) -> RunStub:
    """Create a subprocess stub that reports the GTK default key theme."""
    run_stub.stdout = "'Default'\n"
    return run_stub


@pytest.mark.component
def test_gtk_default_key_theme_registry_id() -> None:
    """Test the GTK default key theme registry ID."""
    assert GtkDefaultKeyTheme.registry_id == "gtk_default_key_theme"


@pytest.mark.component
def test_gtk_default_key_theme_is_satisfied(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test that the GTK default key theme is satisfied when enabled."""
    component = GtkDefaultKeyTheme(run=gtk_default_run_stub)

    assert component.is_satisfied(system) is True
    assert gtk_default_run_stub.calls == [
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
def test_gtk_default_key_theme_is_not_satisfied(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test that the GTK default key theme is not satisfied when disabled."""
    gtk_default_run_stub.returncode = 1
    component = GtkDefaultKeyTheme(run=gtk_default_run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gtk_default_key_theme_implementations(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test that the GTK default key theme provides an implementation for Ubuntu."""
    component = GtkDefaultKeyTheme(run=gtk_default_run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_gtk_default_key_theme_install(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test enabling the GTK default key theme on Ubuntu."""
    implementation = UbuntuGtkDefaultKeyTheme(run=gtk_default_run_stub)

    implementation.install(system)

    assert gtk_default_run_stub.calls == [
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
def test_ubuntu_gtk_default_key_theme_verify(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test verifying the GTK default key theme on Ubuntu."""
    implementation = UbuntuGtkDefaultKeyTheme(run=gtk_default_run_stub)

    assert implementation.verify(system) is True
    assert gtk_default_run_stub.calls == [
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
def test_ubuntu_gtk_default_key_theme_verify_failure(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test failed verification of the GTK default key theme on Ubuntu."""
    gtk_default_run_stub.returncode = 1
    implementation = UbuntuGtkDefaultKeyTheme(run=gtk_default_run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gtk_default_key_theme_install_failure(
    system: System,
    gtk_default_run_stub: RunStub,
) -> None:
    """Test that a failed GTK default key theme installation raises an error."""
    gtk_default_run_stub.returncode = 1
    implementation = UbuntuGtkDefaultKeyTheme(run=gtk_default_run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
