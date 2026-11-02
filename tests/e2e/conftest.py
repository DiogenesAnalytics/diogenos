"""Pytest configuration for the e2e tests."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "gui: tests requiring a graphical desktop.")
    config.addinivalue_line("markers", "lifecycle: feature lifecycle tests.")
