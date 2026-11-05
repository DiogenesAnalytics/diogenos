"""Test the Zed component."""

import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Callable

import pytest

from diogenos.component import ComponentImplementation
from diogenos.component.catalog.zed.zed import ZED_EXECUTABLE
from diogenos.component.catalog.zed.zed import ArchZed
from diogenos.component.catalog.zed.zed import DebianZed
from diogenos.component.catalog.zed.zed import FedoraZed
from diogenos.component.catalog.zed.zed import UbuntuZed
from diogenos.component.catalog.zed.zed import ZedImplementation
from diogenos.component.catalog.zed.zed import ZedPackage
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.fixture
def system_with_platform(
    system: System,
) -> Callable[[str], System]:
    """Return a system with the specified operating system."""

    def create(operating_system: str) -> System:
        return replace(
            system,
            platform=replace(system.platform, os=operating_system),
        )

    return create


@pytest.mark.component
def test_zed_package_registry_id() -> None:
    """Test the Zed component registry identifier."""
    assert ZedPackage.registry_id == "zed"


@pytest.mark.component
def test_zed_package_is_satisfied(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test that Zed is satisfied when its executable succeeds."""
    component = ZedPackage(run=run_stub)

    assert component.is_satisfied(system)

    assert run_stub.calls == [
        (
            [str(ZED_EXECUTABLE), "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_zed_package_is_not_satisfied(
    system: System,
) -> None:
    """Test that Zed is not satisfied when its executable fails."""
    run_stub = RunStub(returncode=1)
    component = ZedPackage(run=run_stub)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_zed_package_implementations(run_stub: RunStub) -> None:
    """Test the implementations exposed by the Zed component."""
    implementations = ZedPackage(run=run_stub).implementations()

    assert len(implementations) == 4
    assert isinstance(implementations[0], UbuntuZed)
    assert isinstance(implementations[1], DebianZed)
    assert isinstance(implementations[2], FedoraZed)
    assert isinstance(implementations[3], ArchZed)
    assert all(
        isinstance(implementation, ComponentImplementation)
        for implementation in implementations
    )


@pytest.mark.parametrize(
    ("implementation", "operating_system"),
    [
        (UbuntuZed, "ubuntu"),
        (DebianZed, "debian"),
        (FedoraZed, "fedora"),
        (ArchZed, "arch"),
    ],
)
@pytest.mark.component
def test_zed_implementation_supports(
    run_stub: RunStub,
    implementation: Callable[..., ComponentImplementation],
    operating_system: str,
    system_with_platform: Callable[[str], System],
) -> None:
    """Test that each implementation supports its target operating system."""
    component = implementation(run=run_stub)

    assert component.supports(system_with_platform(operating_system))


@pytest.mark.parametrize(
    "implementation",
    [
        UbuntuZed,
        DebianZed,
        FedoraZed,
        ArchZed,
    ],
)
@pytest.mark.component
def test_zed_implementation_rejects_unsupported_system(
    run_stub: RunStub,
    implementation: Callable[..., ComponentImplementation],
    system_with_platform: Callable[[str], System],
) -> None:
    """Test that each implementation rejects unsupported systems."""
    component = implementation(run=run_stub)

    assert not component.supports(system_with_platform("opensuse"))


@pytest.mark.component
def test_zed_implementation_inheritance() -> None:
    """Test that platform implementations inherit the shared Zed behavior."""
    assert issubclass(UbuntuZed, ZedImplementation)
    assert issubclass(DebianZed, ZedImplementation)
    assert issubclass(FedoraZed, ZedImplementation)
    assert issubclass(ArchZed, ZedImplementation)


@pytest.mark.component
def test_zed_install(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test installing Zed using its official Linux installer."""
    run_stub.stdout = "installer script"
    component = UbuntuZed(run=run_stub)

    component.install(system)

    assert run_stub.calls == [
        (
            ["curl", "-fL", "https://zed.dev/install.sh"],
            {
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (
            ["sh"],
            {
                "input": "installer script",
                "check": True,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_zed_install_failure(
    system: System,
) -> None:
    """Test that Zed installation stops when downloading the installer fails."""
    run_stub = RunStub(returncode=1)
    component = UbuntuZed(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        component.install(system)

    assert len(run_stub.calls) == 1
    assert run_stub.calls[0] == (
        ["curl", "-fL", "https://zed.dev/install.sh"],
        {
            "capture_output": True,
            "check": True,
            "text": True,
        },
    )


@pytest.mark.component
def test_zed_verify(
    run_stub: RunStub,
    system: System,
) -> None:
    """Test successful verification of Zed."""
    component = UbuntuZed(run=run_stub)

    assert component.verify(system)

    assert run_stub.calls == [
        (
            [str(ZED_EXECUTABLE), "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_zed_verify_failure(
    system: System,
) -> None:
    """Test unsuccessful verification of Zed."""
    run_stub = RunStub(returncode=1)
    component = UbuntuZed(run=run_stub)

    assert not component.verify(system)


@pytest.mark.component
def test_zed_executable() -> None:
    """Test the Zed executable path."""
    assert ZED_EXECUTABLE == Path.home() / ".local/bin/zed"
