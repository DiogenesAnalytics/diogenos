"""Test desktop environment detection."""

import pytest
from pytest import MonkeyPatch

from diogenos.system.desktop import Desktop
from diogenos.system.desktop import DesktopDetector


@pytest.mark.desktop
@pytest.mark.system
def test_desktop() -> None:
    """Test desktop properties."""
    desktop = Desktop(
        name="ubuntu:GNOME",
        pretty_name="GNOME",
    )

    assert desktop.name == "ubuntu:GNOME"
    assert desktop.pretty_name == "GNOME"


@pytest.mark.desktop
@pytest.mark.system
def test_detect_gnome(monkeypatch: MonkeyPatch) -> None:
    """Test detection of GNOME."""
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "GNOME")

    desktop = DesktopDetector().detect()

    assert desktop.name == "GNOME"
    assert desktop.pretty_name == "GNOME"


@pytest.mark.desktop
@pytest.mark.system
def test_detect_compound_desktop(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a desktop from a compound identifier."""
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "ubuntu:GNOME")

    desktop = DesktopDetector().detect()

    assert desktop.name == "ubuntu:GNOME"
    assert desktop.pretty_name == "GNOME"


@pytest.mark.desktop
@pytest.mark.system
def test_detect_kde(monkeypatch: MonkeyPatch) -> None:
    """Test detection of KDE Plasma."""
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "KDE")

    desktop = DesktopDetector().detect()

    assert desktop.name == "KDE"
    assert desktop.pretty_name == "KDE Plasma"


@pytest.mark.desktop
@pytest.mark.system
def test_detect_unknown_desktop(monkeypatch: MonkeyPatch) -> None:
    """Test detection of an unknown desktop."""
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "SomeNewDesktop")

    desktop = DesktopDetector().detect()

    assert desktop.name == "SomeNewDesktop"
    assert desktop.pretty_name == "SomeNewDesktop"


@pytest.mark.desktop
@pytest.mark.system
def test_detect_desktop_session(monkeypatch: MonkeyPatch) -> None:
    """Test detection using DESKTOP_SESSION."""
    monkeypatch.delenv("XDG_CURRENT_DESKTOP", raising=False)
    monkeypatch.setenv("DESKTOP_SESSION", "gnome")

    desktop = DesktopDetector().detect()

    assert desktop.name == "gnome"
    assert desktop.pretty_name == "gnome"


@pytest.mark.desktop
@pytest.mark.system
def test_detect_no_desktop(monkeypatch: MonkeyPatch) -> None:
    """Test detection when no desktop is reported."""
    monkeypatch.delenv("XDG_CURRENT_DESKTOP", raising=False)
    monkeypatch.delenv("DESKTOP_SESSION", raising=False)

    desktop = DesktopDetector().detect()

    assert desktop.name == ""
    assert desktop.pretty_name == ""
