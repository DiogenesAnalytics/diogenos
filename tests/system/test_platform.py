"""Test platform detection."""

import pytest
from pytest import MonkeyPatch

from diogenos.system.platform import Platform
from diogenos.system.platform import PlatformDetector


@pytest.mark.platform
@pytest.mark.system
def test_platform() -> None:
    """Test platform properties."""
    system_platform = Platform(
        os="ubuntu",
        version="24.04",
        pretty_name="Ubuntu 24.04.3 LTS",
    )

    assert system_platform.os == "ubuntu"
    assert system_platform.version == "24.04"
    assert system_platform.pretty_name == "Ubuntu 24.04.3 LTS"


@pytest.mark.platform
@pytest.mark.system
def test_detect_linux(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a Linux platform."""
    monkeypatch.setattr(
        "diogenos.system.platform.platform.system",
        lambda: "Linux",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.freedesktop_os_release",
        lambda: {
            "ID": "ubuntu",
            "VERSION_ID": "24.04",
            "PRETTY_NAME": "Ubuntu 24.04.3 LTS",
        },
    )

    system_platform = PlatformDetector().detect()

    assert system_platform.os == "ubuntu"
    assert system_platform.version == "24.04"
    assert system_platform.pretty_name == "Ubuntu 24.04.3 LTS"


@pytest.mark.platform
@pytest.mark.system
def test_detect_linux_uses_os_release(monkeypatch: MonkeyPatch) -> None:
    """Test that Linux detection uses OS release information."""
    monkeypatch.setattr(
        "diogenos.system.platform.platform.system",
        lambda: "Linux",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.freedesktop_os_release",
        lambda: {
            "ID": "fedora",
            "VERSION_ID": "43",
            "PRETTY_NAME": "Fedora Linux 43",
        },
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.release",
        lambda: "6.17.0",
    )

    system_platform = PlatformDetector().detect()

    assert system_platform.os == "fedora"
    assert system_platform.version == "43"
    assert system_platform.pretty_name == "Fedora Linux 43"


@pytest.mark.platform
@pytest.mark.system
def test_detect_macos(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a macOS platform."""
    monkeypatch.setattr(
        "diogenos.system.platform.platform.system",
        lambda: "Darwin",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.release",
        lambda: "25.0.0",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.platform",
        lambda: "macOS-26.0-arm64",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.freedesktop_os_release",
        lambda: pytest.fail("Linux detection should not be used on macOS"),
    )

    system_platform = PlatformDetector().detect()

    assert system_platform.os == "darwin"
    assert system_platform.version == "25.0.0"
    assert system_platform.pretty_name == "macOS-26.0-arm64"


@pytest.mark.platform
@pytest.mark.system
def test_detect_windows(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a Windows platform."""
    monkeypatch.setattr(
        "diogenos.system.platform.platform.system",
        lambda: "Windows",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.release",
        lambda: "11",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.platform",
        lambda: "Windows-11-10.0.26100-SP0",
    )
    monkeypatch.setattr(
        "diogenos.system.platform.platform.freedesktop_os_release",
        lambda: pytest.fail("Linux detection should not be used on Windows"),
    )

    system_platform = PlatformDetector().detect()

    assert system_platform.os == "windows"
    assert system_platform.version == "11"
    assert system_platform.pretty_name == "Windows-11-10.0.26100-SP0"
