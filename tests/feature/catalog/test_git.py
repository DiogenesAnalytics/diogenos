"""Test the Git feature."""

import pytest

from diogenos.component.catalog.git.git import GitComponent
from diogenos.feature.catalog.git import Git


@pytest.mark.feature
def test_git_contains_git_component() -> None:
    """Verify that the Git feature contains the Git component."""
    feature = Git()

    assert len(feature.components) == 1
    assert isinstance(feature.components[0], GitComponent)
