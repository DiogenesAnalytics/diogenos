"""Test component registry configuration."""

from unittest.mock import patch

import pytest

import diogenos.component.catalog
from diogenos.component.base import Component
from diogenos.component.registry import ComponentRegistry


@pytest.mark.registry
@pytest.mark.component
def test_registry_configures_component_catalog() -> None:
    """Verify that the registry is configured for the component catalog."""
    with patch(
        "diogenos.component.registry.Registry.__init__",
        return_value=None,
    ) as initialize:
        ComponentRegistry()

    assert initialize.call_args.kwargs == {
        "base_class": Component,
        "package_name": diogenos.component.catalog.__name__,
        "package_path": diogenos.component.catalog.__path__,
        "item_name": "component",
    }
