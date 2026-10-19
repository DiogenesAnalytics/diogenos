"""Provide fixtures for component tests."""

import pytest

from tests.component.support import ComponentStub
from tests.component.support import RunStub


@pytest.fixture
def component() -> ComponentStub:
    """Create an unsatisfied component stub."""
    return ComponentStub()


@pytest.fixture
def satisfied_component() -> ComponentStub:
    """Create a satisfied component stub."""
    return ComponentStub(satisfied=True)


@pytest.fixture
def run_stub() -> RunStub:
    """Create a subprocess stub."""
    return RunStub()
