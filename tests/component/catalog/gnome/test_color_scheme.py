"""Test the GNOME color scheme component."""

import subprocess

import pytest

from diogenos.component.catalog.gnome.color_scheme import COLOR_SCHEME_KEY
from diogenos.component.catalog.gnome.color_scheme import COLOR_SCHEME_SCHEMA
from diogenos.component.catalog.gnome.color_scheme import GnomeColorScheme
from diogenos.component.catalog.gnome.color_scheme import UbuntuGnomeColorScheme
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def gnome_color_scheme_run_stub(run_stub: RunStub) -> RunStub:
    """Create a subprocess stub that reports the dark color scheme."""
    run_stub.stdout = "'prefer-dark'\n"
    return run_stub


@pytest.mark.component
def test_gnome_color_scheme_registry_id() -> None:
    """Test the GNOME color scheme registry ID."""
    assert GnomeColorScheme.registry_id == "gnome_color_scheme"


@pytest.mark.component
def test_gnome_color_scheme_is_satisfied(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test that the GNOME color scheme is satisfied when configured."""
    component = GnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    assert component.is_satisfied(system) is True
    assert gnome_color_scheme_run_stub.calls == [
        (
            ["gsettings", "get", COLOR_SCHEME_SCHEMA, COLOR_SCHEME_KEY],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_gnome_color_scheme_is_not_satisfied(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test that the GNOME color scheme is not satisfied when misconfigured."""
    component = GnomeColorScheme(
        color_scheme="default",
        run=gnome_color_scheme_run_stub,
    )

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gnome_color_scheme_is_not_satisfied_on_command_failure(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test that the GNOME color scheme is not satisfied when gsettings fails."""
    gnome_color_scheme_run_stub.returncode = 1
    component = GnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_gnome_color_scheme_implementations(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test that the GNOME color scheme provides an implementation for Ubuntu."""
    component = GnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_gnome_color_scheme_install(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test setting the GNOME color scheme on Ubuntu."""
    implementation = UbuntuGnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    implementation.install(system)

    assert gnome_color_scheme_run_stub.calls == [
        (
            [
                "gsettings",
                "set",
                COLOR_SCHEME_SCHEMA,
                COLOR_SCHEME_KEY,
                "prefer-dark",
            ],
            {
                "check": True,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gnome_color_scheme_verify(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test verifying the GNOME color scheme on Ubuntu."""
    implementation = UbuntuGnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    assert implementation.verify(system) is True
    assert gnome_color_scheme_run_stub.calls == [
        (
            ["gsettings", "get", COLOR_SCHEME_SCHEMA, COLOR_SCHEME_KEY],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gnome_color_scheme_verify_failure(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test failed verification of the GNOME color scheme on Ubuntu."""
    gnome_color_scheme_run_stub.returncode = 1
    implementation = UbuntuGnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gnome_color_scheme_install_failure(
    system: System,
    gnome_color_scheme_run_stub: RunStub,
) -> None:
    """Test that a failed GNOME color scheme installation raises an error."""
    gnome_color_scheme_run_stub.returncode = 1
    implementation = UbuntuGnomeColorScheme(
        color_scheme="prefer-dark",
        run=gnome_color_scheme_run_stub,
    )

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
