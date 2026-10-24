"""Test the GnuPG feature."""

import pytest

from diogenos.feature.catalog.gnupg import GnuPG


@pytest.mark.feature
def test_gnupg_registry_id() -> None:
    """Test the GnuPG feature registry ID."""
    assert GnuPG.registry_id == "gnupg"
