"""Test hardware detection."""

import pytest
from pytest import MonkeyPatch

from diogenos.system.hardware import Hardware
from diogenos.system.hardware import HardwareDetector


@pytest.mark.system
def test_hardware() -> None:
    """Test hardware properties."""
    hardware = Hardware(
        machine="x86_64",
        processor="Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz",
    )

    assert hardware.machine == "x86_64"
    assert hardware.processor == "Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz"


@pytest.mark.system
def test_detect(monkeypatch: MonkeyPatch) -> None:
    """Test detection of hardware."""
    monkeypatch.setattr(
        "diogenos.system.hardware.platform.machine",
        lambda: "x86_64",
    )
    monkeypatch.setattr(
        "diogenos.system.hardware.platform.processor",
        lambda: "Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz",
    )

    hardware = HardwareDetector().detect()

    assert hardware.machine == "x86_64"
    assert hardware.processor == "Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz"
