"""Test the Build Essentials component and its implementations."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.build.build_essentials import (
    BuildEssentials,
)
from diogenos.component.catalog.build.build_essentials import (
    DebianBuildEssentials,
)
from diogenos.component.catalog.build.build_essentials import (
    UbuntuBuildEssentials,
)
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_build_essentials_has_registry_id() -> None:
    """Verify that Build Essentials has the expected registry ID."""
    assert BuildEssentials.registry_id == "build_essentials"


@pytest.mark.component
def test_build_essentials_is_satisfied_when_package_is_installed(
    system: System,
) -> None:
    """Verify that Build Essentials is satisfied when its package is installed."""
    run_stub = RunStub(stdout="installed")
    component = BuildEssentials(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            [
                "dpkg-query",
                "-W",
                "-f=${db:Status-Status}",
                "build-essential",
            ],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_build_essentials_is_not_satisfied_when_package_is_missing(
    system: System,
) -> None:
    """Verify that Build Essentials is not satisfied when its package is missing."""
    run_stub = RunStub(returncode=1)
    component = BuildEssentials(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_build_essentials_is_not_satisfied_when_package_is_not_installed(
    system: System,
) -> None:
    """Verify Build Essentials is not satisfied when package is not installed."""
    run_stub = RunStub(stdout="config-files")
    component = BuildEssentials(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_build_essentials_returns_compatible_implementations(
    system: System,
) -> None:
    """Verify that Build Essentials exposes compatible implementations."""
    component = BuildEssentials()

    implementations = component.implementations()

    assert any(
        implementation.supports(system)
        for implementation in implementations
    )


@pytest.mark.component
def test_ubuntu_build_essentials_installs_package(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu Build Essentials installation runs the expected commands."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuBuildEssentials(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "build-essential"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_build_essentials_installs_package_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu Build Essentials uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuBuildEssentials(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "apt-get", "update"],
            {"check": True},
        ),
        (
            ["sudo", "apt-get", "install", "-y", "build-essential"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_build_essentials_verifies_successful_installation(
    system: System,
) -> None:
    """Verify that Ubuntu Build Essentials reports successful verification."""
    run_stub = RunStub(stdout="installed")
    implementation = UbuntuBuildEssentials(run=run_stub)

    assert implementation.verify(system) is True


@pytest.mark.component
def test_ubuntu_build_essentials_verifies_failed_installation(
    system: System,
) -> None:
    """Verify that Ubuntu Build Essentials reports failed verification."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuBuildEssentials(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_build_essentials_installation_propagates_command_failure(
    system: System,
) -> None:
    """Verify that an APT failure interrupts Build Essentials installation."""
    run_stub = RunStub(returncode=1)
    implementation = UbuntuBuildEssentials(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_build_essentials_installs_package(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Debian Build Essentials installs its package using APT."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = DebianBuildEssentials(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "build-essential"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_build_essentials_verifies_successful_installation(
    system: System,
) -> None:
    """Verify that Debian Build Essentials reports successful verification."""
    run_stub = RunStub(stdout="installed")
    implementation = DebianBuildEssentials(run=run_stub)

    assert implementation.verify(system) is True


@pytest.mark.component
def test_debian_build_essentials_verifies_failed_installation(
    system: System,
) -> None:
    """Verify that Debian Build Essentials reports failed verification."""
    run_stub = RunStub(returncode=1)
    implementation = DebianBuildEssentials(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_build_essentials_installation_propagates_command_failure(
    system: System,
) -> None:
    """Verify that an APT failure interrupts Debian Build Essentials installation."""
    run_stub = RunStub(returncode=1)
    implementation = DebianBuildEssentials(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
