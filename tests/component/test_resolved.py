"""Test resolved components."""

import pytest

from diogenos.component.resolved import ResolvedComponent
from tests.component.support import ComponentStub


@pytest.mark.component
def test_resolved_component_stores_component_and_implementation(
    component: ComponentStub,
) -> None:
    """Verify that a resolved component stores its component and implementation."""
    implementation = component.implementations()[0]

    resolved = ResolvedComponent(
        component=component,
        implementation=implementation,
    )

    assert resolved.component is component
    assert resolved.implementation is implementation
