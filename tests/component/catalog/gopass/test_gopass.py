"""Test the GoPass component."""

import subprocess

import pytest

from diogenos.component.catalog.gopass.gopass import KEYRING_PATH
from diogenos.component.catalog.gopass.gopass import KEYRING_URL
from diogenos.component.catalog.gopass.gopass import PREFERENCES_CONTENT
from diogenos.component.catalog.gopass.gopass import PREFERENCES_PATH
from diogenos.component.catalog.gopass.gopass import SOURCE_CONTENT
from diogenos.component.catalog.gopass.gopass import SOURCE_PATH
from diogenos.component.catalog.gopass.gopass import ArchGoPass
from diogenos.component.catalog.gopass.gopass import DebianGoPass
from diogenos.component.catalog.gopass.gopass import FedoraGoPass
from diogenos.component.catalog.gopass.gopass import GoPassPackage
from diogenos.component.catalog.gopass.gopass import UbuntuGoPass
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_gopass_package_registry_id() -> None:
    """Test the GoPass package registry ID."""
    assert GoPassPackage.registry_id == "gopass"


@pytest.mark.component
def test_gopass_package_is_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that GoPass is satisfied when its version command succeeds."""
    package = GoPassPackage(run=run_stub)

    assert package.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["gopass", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_gopass_package_is_not_satisfied(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that GoPass is not satisfied when its version command fails."""
    run_stub.returncode = 1
    package = GoPassPackage(run=run_stub)

    assert package.is_satisfied(system) is False


@pytest.mark.component
def test_gopass_package_implementations(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that GoPass provides an implementation for the system."""
    package = GoPassPackage(run=run_stub)

    assert any(
        implementation.supports(system) for implementation in package.implementations()
    )


@pytest.mark.component
def test_ubuntu_gopass_install(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test installing GoPass on Ubuntu."""
    implementation = UbuntuGoPass(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["curl", "-L", "-q", KEYRING_URL, "-o", KEYRING_PATH],
            {"check": True},
        ),
        (
            ["tee", SOURCE_PATH],
            {
                "input": SOURCE_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (
            ["tee", PREFERENCES_PATH],
            {
                "input": PREFERENCES_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (["apt-get", "update"], {"check": True}),
        (
            [
                "apt-get",
                "install",
                "-y",
                "gopass",
                "gopass-archive-keyring",
            ],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_gopass_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test verifying GoPass on Ubuntu."""
    implementation = UbuntuGoPass(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gopass", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_gopass_verify_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test failed verification of GoPass on Ubuntu."""
    run_stub.returncode = 1
    implementation = UbuntuGoPass(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_gopass_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that a failed GoPass installation command raises an error."""
    run_stub.returncode = 1
    implementation = UbuntuGoPass(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_gopass_install(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test installing GoPass on Debian."""
    implementation = DebianGoPass(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["curl", "-L", "-q", KEYRING_URL, "-o", KEYRING_PATH],
            {"check": True},
        ),
        (
            ["tee", SOURCE_PATH],
            {
                "input": SOURCE_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (
            ["tee", PREFERENCES_PATH],
            {
                "input": PREFERENCES_CONTENT,
                "capture_output": True,
                "check": True,
                "text": True,
            },
        ),
        (["apt-get", "update"], {"check": True}),
        (
            [
                "apt-get",
                "install",
                "-y",
                "gopass",
                "gopass-archive-keyring",
            ],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_gopass_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test verifying GoPass on Debian."""
    implementation = DebianGoPass(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gopass", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_gopass_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that a failed GoPass installation command raises an error."""
    run_stub.returncode = 1
    implementation = DebianGoPass(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_gopass_install(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test installing GoPass on Fedora."""
    implementation = FedoraGoPass(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "gopass"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_gopass_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test verifying GoPass on Fedora."""
    implementation = FedoraGoPass(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gopass", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_gopass_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that a failed GoPass installation command raises an error."""
    run_stub.returncode = 1
    implementation = FedoraGoPass(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_gopass_install(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test installing GoPass on Arch Linux."""
    implementation = ArchGoPass(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "gopass"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_gopass_verify(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test verifying GoPass on Arch Linux."""
    implementation = ArchGoPass(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["gopass", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_gopass_install_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Test that a failed GoPass installation command raises an error."""
    run_stub.returncode = 1
    implementation = ArchGoPass(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
