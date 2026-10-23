"""Define the shared registry."""

import importlib
import inspect
import pkgutil
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Type


class Registry:
    """Discover classes and look them up by identifier."""

    def __init__(
        self,
        base_class: Type[object],
        package_name: str,
        package_path: Iterable[str],
        item_name: str,
    ) -> None:
        """Initialize the registry and discover available classes."""
        self._item_name = item_name
        self._items: Dict[str, Type[object]] = {}

        for module_info in pkgutil.walk_packages(
            package_path,
            prefix=f"{package_name}.",
        ):
            module = importlib.import_module(module_info.name)

            for _, item_class in inspect.getmembers(
                module,
                inspect.isclass,
            ):
                if (
                    item_class is base_class
                    or not issubclass(item_class, base_class)
                    or inspect.isabstract(item_class)
                    or item_class.__module__ != module.__name__
                ):
                    continue

                registry_id: Optional[str] = vars(item_class).get("registry_id")

                if registry_id is None:
                    continue

                if registry_id in self._items:
                    raise ValueError(
                        f"duplicate {item_name} registry identifier: " f"{registry_id}",
                    )

                self._items[registry_id] = item_class

    def get(self, registry_id: str) -> Type[object]:
        """Return a registered class by identifier."""
        try:
            return self._items[registry_id]
        except KeyError as error:
            raise KeyError(
                f"unknown {self._item_name} identifier: {registry_id}",
            ) from error

    def list(self) -> tuple[str, ...]:
        """Return registered identifiers."""
        return tuple(sorted(self._items))
