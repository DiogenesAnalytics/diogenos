"""Pytest configuration of feature sub-package."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "feature: feature package tests.")
    config.addinivalue_line("markers", "component: component module tests.")
