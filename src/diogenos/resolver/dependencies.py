"""Resolve component dependencies."""

from typing import List
from typing import Set
from typing import Tuple

from diogenos.component import Component
from diogenos.component.registry import ComponentRegistry


class DependencyResolver:
    """Resolve component dependencies in dependency-first order."""

    def __init__(self, registry: ComponentRegistry) -> None:
        """Initialize the dependency resolver."""
        self._registry = registry

    def resolve(
        self,
        components: Tuple[Component, ...],
    ) -> Tuple[Component, ...]:
        """Resolve the requested components and their dependencies."""
        resolved: List[Component] = []
        resolved_ids: Set[str] = set()
        visiting: List[str] = []

        for component in components:
            self._resolve_component(
                component,
                resolved,
                resolved_ids,
                visiting,
            )

        return tuple(resolved)

    def _resolve_component(
        self,
        component: Component,
        resolved: List[Component],
        resolved_ids: Set[str],
        visiting: List[str],
    ) -> None:
        """Resolve a component and recursively resolve its dependencies."""
        registry_id = component.registry_id

        if registry_id is None:
            raise ValueError(
                f"component {type(component).__name__} has no registry identifier",
            )

        if registry_id in visiting:
            cycle = visiting[visiting.index(registry_id) :] + [registry_id]
            raise ValueError(
                f"circular component dependency: {' -> '.join(cycle)}",
            )

        if registry_id in resolved_ids:
            return

        visiting.append(registry_id)

        try:
            for dependency in component.dependencies():
                dependency_class = self._registry.get(dependency.name)
                dependency_component = dependency_class()

                self._resolve_component(
                    dependency_component,
                    resolved,
                    resolved_ids,
                    visiting,
                )
        finally:
            visiting.pop()

        resolved.append(component)
        resolved_ids.add(registry_id)
