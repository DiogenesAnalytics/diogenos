"""Pytest configuration of feature sub-package."""

import pytest

from tests.feature.support import RunStub


@pytest.fixture
def run_stub() -> RunStub:
    """Provide a stub for subprocess.run."""
    return RunStub()
