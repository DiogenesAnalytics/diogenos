"""Test the Firefox feature."""

from diogenos.feature.catalog.firefox import Firefox


def test_firefox_registry_id() -> None:
    """Test the Firefox feature registry identifier."""
    assert Firefox.registry_id == "firefox"
