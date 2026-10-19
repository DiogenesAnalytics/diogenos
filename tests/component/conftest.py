"""Provide fixtures for component tests."""

import pytest

from tests.component.support import ComponentStub


@pytest.fixture
def component() -> ComponentStub:
    """Create an unsatisfied component stub."""
    return ComponentStub()


@pytest.fixture
def satisfied_component() -> ComponentStub:
    """Create a satisfied component stub."""
    return ComponentStub(satisfied=True)
