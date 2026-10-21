"""Pytest configuration for the test suite."""

import os
from typing import List

import pytest

from diogenos.system.base import System
from diogenos.system.desktop import Desktop
from diogenos.system.hardware import Hardware
from diogenos.system.platform import Platform


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "component: component module tests.")
    config.addinivalue_line(
        "markers", "e2e: end-to-end tests requiring a virtual machine."
    )
    config.addinivalue_line("markers", "feature: feature package tests.")
    config.addinivalue_line("markers", "resolver: resolver module tests.")
    config.addinivalue_line("markers", "system: system package tests.")


def pytest_collection_modifyitems(
    items: List[pytest.Item],
) -> None:
    """Skip E2E tests unless explicitly enabled."""
    if os.environ.get("DIOGENOS_E2E") == "1":
        return

    skip_e2e = pytest.mark.skip(reason="E2E tests require DIOGENOS_E2E=1")

    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)


@pytest.fixture
def system() -> System:
    """Create a test system."""
    return System(
        platform=Platform(
            os="ubuntu",
            version="24.04",
            codename="noble",
            pretty_name="Ubuntu 24.04.3 LTS",
        ),
        hardware=Hardware(
            machine="x86_64",
            processor="Intel(R) Core(TM) i5-2500 CPU @ 3.30GHz",
            architecture="amd64",
        ),
        desktop=Desktop(
            name="ubuntu:GNOME",
            pretty_name="GNOME",
        ),
    )
