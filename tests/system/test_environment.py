"""Test environment detection."""

import pytest
from pytest import MonkeyPatch

from diogenos.system.environment import Environment
from diogenos.system.environment import EnvironmentDetector


@pytest.mark.environment
@pytest.mark.system
def test_environment() -> None:
    """Test environment properties."""
    environment = Environment(
        os="ubuntu",
        version="24.04",
        pretty_name="Ubuntu 24.04.3 LTS",
    )

    assert environment.os == "ubuntu"
    assert environment.version == "24.04"
    assert environment.pretty_name == "Ubuntu 24.04.3 LTS"


@pytest.mark.environment
@pytest.mark.system
def test_detect_linux(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a Linux environment."""
    monkeypatch.setattr(
        "diogenos.system.environment.platform.system",
        lambda: "Linux",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.freedesktop_os_release",
        lambda: {
            "ID": "ubuntu",
            "VERSION_ID": "24.04",
            "PRETTY_NAME": "Ubuntu 24.04.3 LTS",
        },
    )

    environment = EnvironmentDetector().detect()

    assert environment.os == "ubuntu"
    assert environment.version == "24.04"
    assert environment.pretty_name == "Ubuntu 24.04.3 LTS"


@pytest.mark.environment
@pytest.mark.system
def test_detect_linux_uses_os_release(monkeypatch: MonkeyPatch) -> None:
    """Test that Linux detection uses OS release information."""
    monkeypatch.setattr(
        "diogenos.system.environment.platform.system",
        lambda: "Linux",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.freedesktop_os_release",
        lambda: {
            "ID": "fedora",
            "VERSION_ID": "43",
            "PRETTY_NAME": "Fedora Linux 43",
        },
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.release",
        lambda: "6.17.0",
    )

    environment = EnvironmentDetector().detect()

    assert environment.os == "fedora"
    assert environment.version == "43"
    assert environment.pretty_name == "Fedora Linux 43"


@pytest.mark.environment
@pytest.mark.system
def test_detect_macos(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a macOS environment."""
    monkeypatch.setattr(
        "diogenos.system.environment.platform.system",
        lambda: "Darwin",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.release",
        lambda: "25.0.0",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.platform",
        lambda: "macOS-26.0-arm64",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.freedesktop_os_release",
        lambda: pytest.fail("Linux detection should not be used on macOS"),
    )

    environment = EnvironmentDetector().detect()

    assert environment.os == "darwin"
    assert environment.version == "25.0.0"
    assert environment.pretty_name == "macOS-26.0-arm64"


@pytest.mark.environment
@pytest.mark.system
def test_detect_windows(monkeypatch: MonkeyPatch) -> None:
    """Test detection of a Windows environment."""
    monkeypatch.setattr(
        "diogenos.system.environment.platform.system",
        lambda: "Windows",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.release",
        lambda: "11",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.platform",
        lambda: "Windows-11-10.0.26100-SP0",
    )
    monkeypatch.setattr(
        "diogenos.system.environment.platform.freedesktop_os_release",
        lambda: pytest.fail("Linux detection should not be used on Windows"),
    )

    environment = EnvironmentDetector().detect()

    assert environment.os == "windows"
    assert environment.version == "11"
    assert environment.pretty_name == "Windows-11-10.0.26100-SP0"
