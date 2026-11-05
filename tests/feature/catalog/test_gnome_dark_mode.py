"""Test the GNOME dark mode feature."""

import pytest

from diogenos.feature.catalog.gnome_dark_mode import GnomeDarkMode


@pytest.mark.feature
def test_gnome_dark_mode_registry_id() -> None:
    """Test the GNOME dark mode registry ID."""
    assert GnomeDarkMode.registry_id == "gnome_dark_mode"
