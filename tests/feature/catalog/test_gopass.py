"""Test the GoPass feature."""

import pytest

from diogenos.feature.catalog.gopass import GoPass


@pytest.mark.feature
def test_gopass_registry_id() -> None:
    """Test the GoPassfeature registry ID."""
    assert GoPass.registry_id == "gopass"
