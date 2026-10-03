"""Pytest configuration of system sub-package."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """For configuring pytest with custom markers."""
    config.addinivalue_line("markers", "system: system package tests.")
    config.addinivalue_line("markers", "platform: platform module tests.")
    config.addinivalue_line("markers", "hardware: hardware module tests.")
    config.addinivalue_line("markers", "desktop: desktop module tests.")
    config.addinivalue_line("markers", "base: system.base module tests.")
