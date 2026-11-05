"""Test the Zed feature."""

from diogenos.feature.catalog.zed import Zed


def test_zed_registry_id() -> None:
    """Test the Zed feature registry identifier."""
    assert Zed.registry_id == "zed"
