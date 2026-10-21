"""Test E2E test selection."""

import pytest


@pytest.mark.e2e
def test_e2e_marker() -> None:
    """Verify that an E2E test can run."""
    assert True
