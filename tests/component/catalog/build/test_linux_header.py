"""Test the Linux kernel headers component."""

from typing import Any
import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.build.linux_header import (
    DebianLinuxKernelHeaders,
)
from diogenos.component.catalog.build.linux_header import (
    LinuxKernelHeaders,
)
from diogenos.component.catalog.build.linux_header import (
    UbuntuLinuxKernelHeaders,
)
from diogenos.system.base import System
from tests.component.support import RunStub


KERNEL_VERSION = "test-kernel-version"
PACKAGE = f"linux-headers-{KERNEL_VERSION}"


@pytest.fixture
def linux_kernel_headers_run_stub() -> RunStub:
    """Create a subprocess stub for installed kernel headers."""
    return RunStub(
        outputs=[
            f"{KERNEL_VERSION}\n",
            "installed\n",
        ],
    )


@pytest.fixture
def linux_kernel_headers_apt_failure_run_stub() -> RunStub:
    """Create a subprocess stub that simulates an APT failure."""
    return RunStub(
        outputs=[f"{KERNEL_VERSION}\n"],
        returncodes=[0, 1],
    )


@pytest.mark.component
def test_registry_id() -> None:
    """Test the component registry ID."""
    assert LinuxKernelHeaders.registry_id == "linux_kernel_headers"


@pytest.mark.component
def test_is_satisfied(
    system: System,
    linux_kernel_headers_run_stub: RunStub,
) -> None:
    """Test that installed kernel headers satisfy the component."""
    component = LinuxKernelHeaders(run=linux_kernel_headers_run_stub)

    assert component.is_satisfied(system)


@pytest.mark.component
def test_is_not_satisfied(system: System) -> None:
    """Test that missing kernel headers do not satisfy the component."""
    run = RunStub(
        outputs=[
            f"{KERNEL_VERSION}\n",
            "not-installed\n",
        ],
    )
    component = LinuxKernelHeaders(run=run)

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_is_not_satisfied_when_kernel_version_unavailable(
    system: System,
) -> None:
    """Test that an unavailable kernel version is not satisfied."""
    component = LinuxKernelHeaders(run=RunStub(returncode=1))

    assert not component.is_satisfied(system)


@pytest.mark.component
def test_implementations(system: System) -> None:
    """Test the available implementations."""
    component = LinuxKernelHeaders()
    implementations = component.implementations()

    assert len(implementations) == 2
    assert any(
        implementation.supports(system)
        for implementation in implementations
    )


@pytest.mark.component
@pytest.mark.parametrize(
    "implementation_class",
    [
        UbuntuLinuxKernelHeaders,
        DebianLinuxKernelHeaders,
    ],
)
def test_install(
    system: System,
    implementation_class: Any,
) -> None:
    """Test installing headers for the running kernel."""
    run = RunStub(outputs=[f"{KERNEL_VERSION}\n"])
    implementation = implementation_class(run=run)

    implementation.install(system)

    assert len(run.calls) == 3
    assert run.calls[0][0] == ["uname", "-r"]
    assert run.calls[1][1]["check"] is True
    assert run.calls[2][1]["check"] is True
    assert PACKAGE in run.calls[2][0]


@pytest.mark.component
def test_install_uses_sudo(
    system: System,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that package installation uses privileged commands."""
    run = RunStub(outputs=[f"{KERNEL_VERSION}\n"])
    implementation = UbuntuLinuxKernelHeaders(run=run)

    monkeypatch.setattr(
        "diogenos.component.catalog.build.linux_header.prepare_command",
        lambda command, privileged=False: (
            ["sudo", *command] if privileged else command
        ),
    )

    implementation.install(system)

    assert run.calls[1][0][0] == "sudo"
    assert run.calls[2][0][0] == "sudo"


@pytest.mark.component
def test_verify(system: System) -> None:
    """Test successful verification."""
    run = RunStub(
        outputs=[
            f"{KERNEL_VERSION}\n",
            "installed\n",
        ],
    )
    implementation = UbuntuLinuxKernelHeaders(run=run)

    assert implementation.verify(system)


@pytest.mark.component
def test_verify_failure(system: System) -> None:
    """Test unsuccessful verification."""
    run = RunStub(
        outputs=[
            f"{KERNEL_VERSION}\n",
            "not-installed\n",
        ],
    )
    implementation = UbuntuLinuxKernelHeaders(run=run)

    assert not implementation.verify(system)


@pytest.mark.component
def test_install_failure_when_kernel_version_unavailable(
    system: System,
) -> None:
    """Test installation failure when the kernel version is unavailable."""
    implementation = UbuntuLinuxKernelHeaders(
        run=RunStub(returncode=1),
    )

    with pytest.raises(RuntimeError):
        implementation.install(system)


@pytest.mark.component
def test_install_failure(
    system: System,
    linux_kernel_headers_apt_failure_run_stub: RunStub,
) -> None:
    """Test APT installation failure."""
    implementation = UbuntuLinuxKernelHeaders(
        run=linux_kernel_headers_apt_failure_run_stub,
    )

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)

    assert len(linux_kernel_headers_apt_failure_run_stub.calls) == 2


@pytest.mark.component
def test_debian_install_failure_when_kernel_version_unavailable(
    system: System,
) -> None:
    """Test Debian installation failure when the kernel version is unavailable."""
    implementation = DebianLinuxKernelHeaders(
        run=RunStub(returncode=1),
    )

    with pytest.raises(RuntimeError):
        implementation.install(system)
