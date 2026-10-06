"""Pytest configuration for the test suite."""

import pytest

from diogenos.system.base import System
from diogenos.system.desktop import Desktop
from diogenos.system.hardware import Hardware
from diogenos.system.platform import Platform


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "resolver: resolver module tests.")


@pytest.fixture
def system() -> System:
    """Create a test system."""
    return System(
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
