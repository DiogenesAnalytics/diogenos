"""Test the component implementation abstraction."""

from typing import Optional
from typing import Tuple

import pytest

from diogenos.component import ComponentImplementation
from diogenos.component.implementation.method import APTInstallMixin
from diogenos.component.implementation.method import InstallMethodType
from diogenos.component.implementation.method import SnapInstallMixin
from diogenos.system.base import System


class ComponentImplementationStub(ComponentImplementation):
    """Provide an OS-aware component implementation for testing."""

    OS = "ubuntu"

    def __init__(
        self,
        verified: bool = True,
    ) -> None:
        """Initialize the component implementation stub."""
        self.verified = verified
        self.install_called = False
        self.install_method: Optional[InstallMethodType] = None
        self.verify_called = False

    def install(
        self,
        system: System,
        method: Optional[InstallMethodType] = None,
    ) -> None:
        """Record that installation was called."""
        self.install_called = True
        self.install_method = method

    def verify(self, system: System) -> bool:
        """Record that verification was called."""
        self.verify_called = True
        return self.verified


class PackageComponentImplementationStub(
    ComponentImplementationStub,
    APTInstallMixin,
    SnapInstallMixin,
):
    """Provide package installation methods for testing."""

    def __init__(self) -> None:
        """Initialize the package component implementation stub."""
        super().__init__()
        self.installed_packages: Tuple[str, ...] = ()
        self.installed_method: Optional[InstallMethodType] = None

    def install_apt(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Record APT package installation."""
        self.installed_packages = packages
        self.installed_method = InstallMethodType.APT

    def install_snap(
        self,
        system: System,
        packages: Tuple[str, ...],
    ) -> None:
        """Record Snap package installation."""
        self.installed_packages = packages
        self.installed_method = InstallMethodType.SNAP


class DefaultPackageComponentImplementationStub(
    PackageComponentImplementationStub,
):
    """Provide a default package installation method."""

    DEFAULT_INSTALL_METHOD = InstallMethodType.SNAP


@pytest.mark.component
def test_implementation_is_abstract() -> None:
    """Test that ComponentImplementation cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ComponentImplementation()  # type: ignore[abstract]


@pytest.mark.component
def test_implementation_supports_system(
    system: System,
) -> None:
    """Test that an implementation supports its system."""
    implementation = ComponentImplementationStub()

    assert implementation.supports(system) is True


@pytest.mark.component
def test_implementation_does_not_support_system(
    system: System,
) -> None:
    """Test that an implementation does not support another system."""
    implementation = ComponentImplementationStub()

    system = System(
        platform=system.platform.__class__(
            os="fedora",
            version=system.platform.version,
            codename=system.platform.codename,
            pretty_name="Fedora Linux",
        ),
        hardware=system.hardware,
        desktop=system.desktop,
    )

    assert implementation.supports(system) is False


@pytest.mark.component
def test_implementation_install_without_method(
    system: System,
) -> None:
    """Test that installation can be called without an explicit method."""
    implementation = ComponentImplementationStub()

    implementation.install(system)

    assert implementation.install_called is True
    assert implementation.install_method is None


@pytest.mark.component
def test_implementation_install_with_method(
    system: System,
) -> None:
    """Test that an explicit installation method is passed through."""
    implementation = ComponentImplementationStub()

    implementation.install(system, InstallMethodType.SNAP)

    assert implementation.install_called is True
    assert implementation.install_method == InstallMethodType.SNAP


@pytest.mark.component
def test_implementation_install_methods() -> None:
    """Test that available installation methods are discovered."""
    implementation = PackageComponentImplementationStub()

    assert implementation.install_methods == (
        InstallMethodType.APT,
        InstallMethodType.SNAP,
    )


@pytest.mark.component
@pytest.mark.parametrize(
    "method",
    (
        InstallMethodType.APT,
        InstallMethodType.SNAP,
    ),
)
def test_implementation_install_packages_with_method(
    system: System,
    method: InstallMethodType,
) -> None:
    """Test that packages are installed using the selected method."""
    implementation = PackageComponentImplementationStub()
    packages = ("firefox",)

    implementation.install_packages(system, packages, method)

    assert implementation.installed_method == method
    assert implementation.installed_packages == packages


@pytest.mark.component
def test_implementation_install_packages_with_default_method(
    system: System,
) -> None:
    """Test that the default installation method is used."""
    implementation = DefaultPackageComponentImplementationStub()
    packages = ("firefox",)

    implementation.install_packages(system, packages)

    assert implementation.installed_method == InstallMethodType.SNAP
    assert implementation.installed_packages == packages


@pytest.mark.component
def test_implementation_install_packages_without_method(
    system: System,
) -> None:
    """Test that package installation requires a method."""
    implementation = PackageComponentImplementationStub()

    with pytest.raises(ValueError, match="No installation method specified"):
        implementation.install_packages(system, ("firefox",))


@pytest.mark.component
def test_implementation_install_packages_with_unsupported_method(
    system: System,
) -> None:
    """Test that unsupported installation methods are rejected."""
    implementation = PackageComponentImplementationStub()

    with pytest.raises(ValueError, match="Unsupported installation method"):
        implementation.install_packages(
            system,
            ("firefox",),
            InstallMethodType.DOCKER,
        )


@pytest.mark.component
def test_implementation_without_install_methods() -> None:
    """Test that components can exist without package installation methods."""
    implementation = ComponentImplementationStub()

    assert implementation.install_methods == ()


@pytest.mark.component
def test_implementation_verify(
    system: System,
) -> None:
    """Test that verification is called."""
    implementation = ComponentImplementationStub()

    assert implementation.verify(system) is True
    assert implementation.verify_called is True


@pytest.mark.component
def test_implementation_verify_returns_false(
    system: System,
) -> None:
    """Test that verification can report an unsuccessful installation."""
    implementation = ComponentImplementationStub(verified=False)

    assert implementation.verify(system) is False
    assert implementation.verify_called is True
