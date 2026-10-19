"""Test component discovery and lookup."""

import pytest

from diogenos.component import Component
from diogenos.component.catalog.docker.engine import DockerEngine
from diogenos.component.catalog.git.git import GitComponent
from diogenos.component.catalog.tmux.tmux import TmuxPackage
from diogenos.component.registry import ComponentRegistry


@pytest.fixture
def registry() -> ComponentRegistry:
    """Provide a component registry."""
    return ComponentRegistry()


@pytest.mark.component
def test_registry_discovers_git(
    registry: ComponentRegistry,
) -> None:
    """Verify that the registry discovers Git."""
    assert registry.get("git") is GitComponent


@pytest.mark.component
def test_registry_discovers_tmux(
    registry: ComponentRegistry,
) -> None:
    """Verify that the registry discovers Tmux."""
    assert registry.get("tmux") is TmuxPackage


@pytest.mark.component
def test_registry_discovers_docker_engine(
    registry: ComponentRegistry,
) -> None:
    """Verify that the registry discovers Docker Engine."""
    assert registry.get("docker.engine") is DockerEngine


@pytest.mark.component
def test_registry_rejects_unknown_identifier(
    registry: ComponentRegistry,
) -> None:
    """Verify that lookup rejects unknown identifiers."""
    with pytest.raises(
        KeyError,
        match="unknown component identifier: missing",
    ):
        registry.get("missing")


@pytest.mark.component
def test_base_component_has_no_registry_identifier() -> None:
    """Verify that the abstract base component isn't registered."""
    assert Component.registry_id is None
