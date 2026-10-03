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
def test_system() -> None:
    """Test system properties."""
    system = System(
        platform=Platform(
            os="ubuntu",
            version="24.04",
            pretty_name="Ubuntu 24.04.3 LTS",
        ),
        hardware=Hardware(
            machine="x86_64",
            processor="Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz",
        ),
        desktop=Desktop(
            name="ubuntu:GNOME",
            pretty_name="GNOME",
        ),
    )

    assert system.platform.os == "ubuntu"
    assert system.hardware.machine == "x86_64"
    assert system.desktop.name == "ubuntu:GNOME"


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
