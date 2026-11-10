"""Test Linux component implementation strategies."""

from typing import Type

import pytest

from diogenos.component import AlpineComponentImplementation
from diogenos.component import APTComponentImplementation
from diogenos.component import ArchComponentImplementation
from diogenos.component import ComponentImplementation
from diogenos.component import DebianComponentImplementation
from diogenos.component import FedoraComponentImplementation
from diogenos.component import OpenSUSEComponentImplementation
from diogenos.component import SnapComponentImplementation
from diogenos.component import UbuntuComponentImplementation
from diogenos.component.implementation.method.types import MethodType


@pytest.mark.component
def test_apt_implementation_has_no_default_method() -> None:
    """Test that the APT capability does not declare a default."""
    assert APTComponentImplementation.DEFAULT_METHOD is None


@pytest.mark.component
def test_snap_implementation_has_no_default_method() -> None:
    """Test that the Snap capability does not declare a default."""
    assert SnapComponentImplementation.DEFAULT_METHOD is None


@pytest.mark.component
def test_debian_implementation() -> None:
    """Test the Debian implementation configuration."""
    assert issubclass(DebianComponentImplementation, APTComponentImplementation)
    assert DebianComponentImplementation.OS == "debian"
    assert DebianComponentImplementation.DEFAULT_METHOD == MethodType.APT


@pytest.mark.component
def test_ubuntu_implementation() -> None:
    """Test the Ubuntu implementation configuration."""
    assert issubclass(UbuntuComponentImplementation, APTComponentImplementation)
    assert issubclass(UbuntuComponentImplementation, SnapComponentImplementation)
    assert UbuntuComponentImplementation.OS == "ubuntu"
    assert UbuntuComponentImplementation.DEFAULT_METHOD == MethodType.SNAP


@pytest.mark.parametrize(
    ("implementation", "operating_system"),
    (
        (FedoraComponentImplementation, "fedora"),
        (ArchComponentImplementation, "arch"),
        (OpenSUSEComponentImplementation, "opensuse"),
        (AlpineComponentImplementation, "alpine"),
    ),
)
@pytest.mark.component
def test_other_linux_implementations(
    implementation: Type[ComponentImplementation],
    operating_system: str,
) -> None:
    """Test Linux implementations without an installation method default."""
    assert implementation.OS == operating_system
    assert implementation.DEFAULT_METHOD is None
