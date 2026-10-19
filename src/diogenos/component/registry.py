"""Discover and look up components."""

import importlib
import inspect
import pkgutil
from typing import Dict
from typing import Type

import diogenos.component.catalog
from diogenos.component.base import Component


class ComponentRegistry:
    """Discover components and look them up by identifier."""

    def __init__(self) -> None:
        """Initialize the registry by discovering catalog components."""
        self._components: Dict[str, Type[Component]] = {}
        self._discover()

    def _discover(self) -> None:
        """Discover and register components in the component catalog."""
        package = diogenos.component.catalog

        for module_info in pkgutil.walk_packages(
            package.__path__,
            prefix=f"{package.__name__}.",
        ):
            module = importlib.import_module(module_info.name)

            for _, component_class in inspect.getmembers(
                module,
                inspect.isclass,
            ):
                if (
                    component_class is Component
                    or not issubclass(component_class, Component)
                    or inspect.isabstract(component_class)
                    or component_class.__module__ != module.__name__
                ):
                    continue

                registry_id = component_class.registry_id

                if registry_id is None:
                    continue

                if registry_id in self._components:
                    raise ValueError(
                        f"duplicate component registry identifier: " f"{registry_id}",
                    )

                self._components[registry_id] = component_class

    def get(self, registry_id: str) -> Type[Component]:
        """Return a component class by identifier."""
        try:
            return self._components[registry_id]
        except KeyError as error:
            raise KeyError(
                f"unknown component identifier: {registry_id}",
            ) from error
