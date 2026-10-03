"""Test system detection."""

import pytest
from pytest import MonkeyPatch

from diogenos.system.base import System
from diogenos.system.base import SystemDetector
from diogenos.system.desktop import Desktop
from diogenos.system.hardware import Hardware
from diogenos.system.platform import Platform


@pytest.mark.base
@pytest.mark.system
def test_system(system: System) -> None:
    """Test system properties."""
    assert system.platform.os == "ubuntu"
    assert system.hardware.machine == "x86_64"
    assert system.desktop.name == "ubuntu:GNOME"


@pytest.mark.base
@pytest.mark.system
def test_system_supports_platform(system: System) -> None:
    """Test platform support."""
    assert system.supports(platform="ubuntu")
    assert not system.supports(platform="fedora")


@pytest.mark.base
@pytest.mark.system
def test_system_supports_desktop(system: System) -> None:
    """Test desktop support."""
    assert system.supports(desktop="ubuntu:GNOME")
    assert not system.supports(desktop="kde")


@pytest.mark.base
@pytest.mark.system
def test_system_supports_machine(system: System) -> None:
    """Test hardware support."""
    assert system.supports(machine="x86_64")
    assert not system.supports(machine="aarch64")


@pytest.mark.base
@pytest.mark.system
def test_system_supports_multiple_conditions(system: System) -> None:
    """Test multiple support conditions."""
    assert system.supports(
        platform="ubuntu",
        desktop="ubuntu:GNOME",
        machine="x86_64",
    )


@pytest.mark.base
@pytest.mark.system
def test_system_supports_requires_condition(system: System) -> None:
    """Test that support requires at least one condition."""
    with pytest.raises(ValueError, match="at least one condition"):
        system.supports()


@pytest.mark.base
@pytest.mark.system
def test_detect(monkeypatch: MonkeyPatch) -> None:
    """Test detection of the current system."""
    monkeypatch.setattr(
        "diogenos.system.base.PlatformDetector.detect",
        lambda _: Platform(
            os="ubuntu",
            version="24.04",
            pretty_name="Ubuntu 24.04.3 LTS",
        ),
    )
    monkeypatch.setattr(
        "diogenos.system.base.HardwareDetector.detect",
        lambda _: Hardware(
            machine="x86_64",
            processor="Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz",
        ),
    )
    monkeypatch.setattr(
        "diogenos.system.base.DesktopDetector.detect",
        lambda _: Desktop(
            name="ubuntu:GNOME",
            pretty_name="GNOME",
        ),
    )

    system = SystemDetector().detect()

    assert system.platform.os == "ubuntu"
    assert system.hardware.machine == "x86_64"
    assert system.desktop.name == "ubuntu:GNOME"
