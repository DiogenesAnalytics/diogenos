"""Test hardware detection."""

import pytest
from pytest import MonkeyPatch

from diogenos.system.hardware import Hardware
from diogenos.system.hardware import HardwareDetector


@pytest.mark.hardware
@pytest.mark.system
def test_hardware() -> None:
    """Test hardware properties."""
    hardware = Hardware(
        machine="x86_64",
        processor="Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz",
        architecture="amd64",
    )

    assert hardware.machine == "x86_64"
    assert hardware.processor == "Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz"
    assert hardware.architecture == "amd64"


@pytest.mark.hardware
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
    assert hardware.architecture == "amd64"


@pytest.mark.hardware
@pytest.mark.system
@pytest.mark.parametrize(
    ("machine", "architecture"),
    (
        ("x86_64", "amd64"),
        ("amd64", "amd64"),
        ("aarch64", "arm64"),
        ("arm64", "arm64"),
    ),
)
def test_detect_architecture(
    monkeypatch: MonkeyPatch,
    machine: str,
    architecture: str,
) -> None:
    """Test detection of normalized architecture."""
    monkeypatch.setattr(
        "diogenos.system.hardware.platform.machine",
        lambda: machine,
    )

    hardware = HardwareDetector().detect()

    assert hardware.architecture == architecture


@pytest.mark.hardware
@pytest.mark.system
def test_detect_unknown_architecture(
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that an unknown architecture is preserved."""
    monkeypatch.setattr(
        "diogenos.system.hardware.platform.machine",
        lambda: "mips64",
    )

    hardware = HardwareDetector().detect()

    assert hardware.architecture == "mips64"
