"""Pytest configuration of feature sub-package."""

import pytest

from tests.feature.support import RunStub


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "feature: feature package tests.")
    config.addinivalue_line("markers", "component: component module tests.")


@pytest.fixture
def run_stub() -> RunStub:
    """Provide a stub for subprocess.run."""
    return RunStub()
