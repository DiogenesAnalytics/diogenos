"""Test Linux component implementation strategies."""

from typing import Type

import pytest

from diogenos.component import AlpineComponentImplementation
from diogenos.component import ArchComponentImplementation
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import OpenSUSEComponentImplementation
from diogenos.component import UbuntuComponentImplementation


@pytest.mark.parametrize(
    ("implementation", "operating_system"),
    (
        (DebianComponentImplementation, "debian"),
        (UbuntuComponentImplementation, "ubuntu"),
        (FedoraComponentImplementation, "fedora"),
        (ArchComponentImplementation, "arch"),
        (OpenSUSEComponentImplementation, "opensuse"),
        (AlpineComponentImplementation, "alpine"),
    ),
)
@pytest.mark.component
def test_linux_implementation(
    implementation: Type[ComponentImplementation],
    operating_system: str,
) -> None:
    """Test Linux implementation OS configuration."""
    assert implementation.OS == operating_system
