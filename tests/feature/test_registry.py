"""Test feature registry configuration."""

from unittest.mock import patch

import pytest

import diogenos.feature.catalog
from diogenos.feature.base import Feature
from diogenos.feature.registry import FeatureRegistry


@pytest.mark.registry
@pytest.mark.feature
def test_registry_configures_feature_catalog() -> None:
    """Verify that the registry is configured for the feature catalog."""
    with patch(
        "diogenos.feature.registry.Registry.__init__",
        return_value=None,
    ) as initialize:
        FeatureRegistry()

    assert initialize.call_args.kwargs == {
        "base_class": Feature,
        "package_name": diogenos.feature.catalog.__name__,
        "package_path": diogenos.feature.catalog.__path__,
        "item_name": "feature",
    }
