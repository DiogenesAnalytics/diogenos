"""Test generic registry discovery and lookup."""

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Generator
from typing import Tuple
from typing import Type

import pytest
from pytest import MonkeyPatch

from diogenos.registry import Registry


@pytest.fixture
def registry_package(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> Generator[Tuple[ModuleType, Type[object], Path], None, None]:
    """Provide an isolated package for registry tests."""
    package_name = "registry_fixture"
    package_path = tmp_path / package_name
    package_path.mkdir()

    (package_path / "__init__.py").write_text("")
    (package_path / "base.py").write_text(
        "class Base:\n" "    registry_id = None\n",
    )

    monkeypatch.syspath_prepend(str(tmp_path))

    package = importlib.import_module(package_name)
    base_module = importlib.import_module(f"{package_name}.base")
    base_class = base_module.__dict__["Base"]

    yield package, base_class, package_path

    for module_name in list(sys.modules):
        if (
            module_name == package_name
            or module_name.startswith(f"{package_name}.")
            or module_name == "external_registry_item"
        ):
            del sys.modules[module_name]


def write_module(
    package_path: Path,
    module_name: str,
    source: str,
) -> None:
    """Write a module into the temporary package."""
    (package_path / f"{module_name}.py").write_text(source)


@pytest.mark.registry
def test_registry_discovers_concrete_subclass(
    registry_package: Tuple[ModuleType, Type[object], Path],
) -> None:
    """Verify that the registry discovers concrete subclasses."""
    package, base_class, package_path = registry_package

    write_module(
        package_path,
        "concrete",
        "from .base import Base\n"
        "\n"
        "class ConcreteItem(Base):\n"
        '    registry_id = "concrete"\n',
    )

    registry = Registry(
        base_class=base_class,
        package_name=package.__name__,
        package_path=package.__path__,
        item_name="test item",
    )

    concrete_module = importlib.import_module(
        f"{package.__name__}.concrete",
    )

    assert registry.get("concrete") is concrete_module.ConcreteItem


@pytest.mark.registry
def test_registry_excludes_abstract_subclass(
    registry_package: Tuple[ModuleType, Type[object], Path],
) -> None:
    """Verify that the registry excludes abstract subclasses."""
    package, base_class, package_path = registry_package

    write_module(
        package_path,
        "abstract_item",
        "from abc import ABC, abstractmethod\n"
        "from .base import Base\n"
        "\n"
        "class AbstractItem(Base, ABC):\n"
        '    registry_id = "abstract"\n'
        "\n"
        "    @abstractmethod\n"
        "    def run(self) -> None:\n"
        "        pass\n",
    )

    registry = Registry(
        base_class=base_class,
        package_name=package.__name__,
        package_path=package.__path__,
        item_name="test item",
    )

    with pytest.raises(
        KeyError,
        match="unknown test item identifier: abstract",
    ):
        registry.get("abstract")


@pytest.mark.registry
def test_registry_excludes_classes_imported_from_other_modules(
    registry_package: Tuple[ModuleType, Type[object], Path],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that imported subclasses aren't registered from another module."""
    package, base_class, package_path = registry_package

    (tmp_path / "external_registry_item.py").write_text(
        "from registry_fixture.base import Base\n"
        "\n"
        "class ExternalItem(Base):\n"
        '    registry_id = "external"\n',
    )

    monkeypatch.syspath_prepend(str(tmp_path))

    write_module(
        package_path,
        "imports",
        "from external_registry_item import ExternalItem\n",
    )

    registry = Registry(
        base_class=base_class,
        package_name=package.__name__,
        package_path=package.__path__,
        item_name="test item",
    )

    with pytest.raises(
        KeyError,
        match="unknown test item identifier: external",
    ):
        registry.get("external")


@pytest.mark.registry
def test_registry_skips_classes_without_registry_identifier(
    registry_package: Tuple[ModuleType, Type[object], Path],
) -> None:
    """Verify that subclasses without registry identifiers are skipped."""
    package, base_class, package_path = registry_package

    write_module(
        package_path,
        "unregistered",
        "from .base import Base\n" "\n" "class UnregisteredItem(Base):\n" "    pass\n",
    )

    registry = Registry(
        base_class=base_class,
        package_name=package.__name__,
        package_path=package.__path__,
        item_name="test item",
    )

    with pytest.raises(
        KeyError,
        match="unknown test item identifier: missing",
    ):
        registry.get("missing")


@pytest.mark.registry
def test_registry_rejects_duplicate_identifiers(
    registry_package: Tuple[ModuleType, Type[object], Path],
) -> None:
    """Verify that duplicate registry identifiers are rejected."""
    package, base_class, package_path = registry_package

    write_module(
        package_path,
        "first",
        "from .base import Base\n"
        "\n"
        "class FirstItem(Base):\n"
        '    registry_id = "duplicate"\n',
    )

    write_module(
        package_path,
        "second",
        "from .base import Base\n"
        "\n"
        "class SecondItem(Base):\n"
        '    registry_id = "duplicate"\n',
    )

    with pytest.raises(
        ValueError,
        match="duplicate test item registry identifier: duplicate",
    ):
        Registry(
            base_class=base_class,
            package_name=package.__name__,
            package_path=package.__path__,
            item_name="test item",
        )


@pytest.mark.registry
def test_registry_rejects_unknown_identifier(
    registry_package: Tuple[ModuleType, Type[object], Path],
) -> None:
    """Verify that lookup rejects unknown identifiers."""
    package, base_class, package_path = registry_package

    registry = Registry(
        base_class=base_class,
        package_name=package.__name__,
        package_path=package.__path__,
        item_name="test item",
    )

    with pytest.raises(
        KeyError,
        match="unknown test item identifier: missing",
    ):
        registry.get("missing")


@pytest.mark.registry
def test_registry_lists_identifiers_in_sorted_order(
    registry_package: Tuple[ModuleType, Type[object], Path],
) -> None:
    """Verify that registered identifiers are returned in sorted order."""
    package, base_class, package_path = registry_package

    write_module(
        package_path,
        "zebra",
        "from .base import Base\n"
        "\n"
        "class Zebra(Base):\n"
        '    registry_id = "zebra"\n',
    )

    write_module(
        package_path,
        "apple",
        "from .base import Base\n"
        "\n"
        "class Apple(Base):\n"
        '    registry_id = "apple"\n',
    )

    registry = Registry(
        base_class=base_class,
        package_name=package.__name__,
        package_path=package.__path__,
        item_name="test item",
    )

    assert registry.list() == ("apple", "zebra")
