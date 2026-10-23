"""Test the Pulsar feature."""

from diogenos.feature.catalog.pulsar import Pulsar


def test_pulsar_registry_id() -> None:
    """Test the Pulsar feature registry identifier."""
    assert Pulsar.registry_id == "pulsar"
