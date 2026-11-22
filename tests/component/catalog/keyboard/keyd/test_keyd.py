"""Test the Keyd component."""

import subprocess
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.keyboard.keyd import Keyd
from diogenos.component.catalog.keyboard.keyd import UbuntuKeyd
from diogenos.component.catalog.keyboard.keyd.keyd import KEYD_REPOSITORY
from diogenos.component.catalog.keyboard.keyd.keyd import KEYD_VERSION
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_keyd_registry_id() -> None:
    """Test the Keyd registry ID."""
    assert Keyd.registry_id == "keyd"


@pytest.mark.component
def test_keyd_dependencies() -> None:
    """Verify that Keyd declares its build dependencies."""
    component = Keyd()

    dependencies = component.dependencies()

    assert len(dependencies) == 3
    assert dependencies[0].name == "git"
    assert dependencies[1].name == "build_essentials"
    assert dependencies[2].name == "linux_kernel_headers"


@pytest.mark.component
def test_keyd_is_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that Keyd is satisfied when its service is enabled and active."""
    component = Keyd(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["systemctl", "is-enabled", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
        (
            ["systemctl", "is-active", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_keyd_is_not_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that Keyd is not satisfied when its service is unavailable."""
    run_stub.returncode = 1
    component = Keyd(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_keyd_implementations(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that Keyd provides an implementation for Ubuntu."""
    component = Keyd(run=run_stub)

    assert any(
        implementation.supports(system)
        for implementation in component.implementations()
    )


@pytest.mark.component
def test_ubuntu_keyd_install(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test installing Keyd on Ubuntu."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuKeyd(run=run_stub)

    implementation.install(system)

    clone_command = run_stub.calls[0][0]
    source_directory = Path(clone_command[-1])

    assert clone_command == [
        "git",
        "clone",
        "--branch",
        KEYD_VERSION,
        "--depth",
        "1",
        KEYD_REPOSITORY,
        str(source_directory),
    ]
    assert source_directory.name == "keyd"
    assert source_directory.parent.name.startswith("diogenos-keyd-")

    assert run_stub.calls[1] == (
        ["make"],
        {
            "cwd": source_directory,
            "check": True,
        },
    )
    assert run_stub.calls[2] == (
        ["make", "install"],
        {
            "cwd": source_directory,
            "check": True,
        },
    )
    assert run_stub.calls[3] == (
        ["systemctl", "daemon-reload"],
        {"check": True},
    )
    assert run_stub.calls[4] == (
        ["systemctl", "enable", "--now", "keyd"],
        {"check": True},
    )
    assert len(run_stub.calls) == 5


@pytest.mark.component
def test_ubuntu_keyd_install_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that privileged Keyd installation commands use sudo."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuKeyd(run=run_stub)

    implementation.install(system)

    clone_command = run_stub.calls[0][0]
    source_directory = Path(clone_command[-1])

    assert run_stub.calls[0][0][:7] == [
        "git",
        "clone",
        "--branch",
        KEYD_VERSION,
        "--depth",
        "1",
        KEYD_REPOSITORY,
    ]
    assert run_stub.calls[1] == (
        ["make"],
        {
            "cwd": source_directory,
            "check": True,
        },
    )
    assert run_stub.calls[2] == (
        ["sudo", "make", "install"],
        {
            "cwd": source_directory,
            "check": True,
        },
    )
    assert run_stub.calls[3] == (
        ["sudo", "systemctl", "daemon-reload"],
        {"check": True},
    )
    assert run_stub.calls[4] == (
        ["sudo", "systemctl", "enable", "--now", "keyd"],
        {"check": True},
    )
    assert len(run_stub.calls) == 5


@pytest.mark.component
def test_ubuntu_keyd_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test verifying Keyd on Ubuntu."""
    implementation = UbuntuKeyd(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["systemctl", "is-enabled", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
        (
            ["systemctl", "is-active", "--quiet", "keyd"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_keyd_verify_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test failed verification of Keyd on Ubuntu."""
    run_stub.returncode = 1
    implementation = UbuntuKeyd(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_keyd_install_failure(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that a failed Keyd installation command raises an error."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    run_stub.returncode = 1
    implementation = UbuntuKeyd(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
