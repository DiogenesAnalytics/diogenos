"""Test the Curl component and its implementations."""

import subprocess

import pytest

from diogenos.component.catalog.curl.curl import ArchCurl
from diogenos.component.catalog.curl.curl import CurlPackage
from diogenos.component.catalog.curl.curl import DebianCurl
from diogenos.component.catalog.curl.curl import FedoraCurl
from diogenos.component.catalog.curl.curl import UbuntuCurl
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_curl_package_has_registry_id() -> None:
    """Verify that the Curl package has the expected registry ID."""
    assert CurlPackage.registry_id == "curl"


@pytest.mark.component
def test_curl_package_is_satisfied_when_curl_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Curl is satisfied when curl --version succeeds."""
    component = CurlPackage(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["curl", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_curl_package_is_not_satisfied_when_curl_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Curl is not satisfied when curl --version fails."""
    run_stub.returncode = 127
    component = CurlPackage(run=run_stub)

    assert component.is_satisfied(system) is False


@pytest.mark.component
def test_curl_package_returns_compatible_implementations(
    system: System,
) -> None:
    """Verify that the Curl package exposes compatible implementations."""
    component = CurlPackage()

    implementations = component.implementations()

    assert any(implementation.supports(system) for implementation in implementations)


@pytest.mark.component
def test_ubuntu_curl_installs_curl(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Curl installation runs the expected commands."""
    implementation = UbuntuCurl(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "curl"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_curl_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Curl reports successful verification."""
    implementation = UbuntuCurl(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["curl", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_curl_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Curl reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuCurl(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_curl_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Curl installation."""
    run_stub.returncode = 1
    implementation = UbuntuCurl(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_curl_installs_curl(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Curl installation delegates to Ubuntu Curl."""
    implementation = DebianCurl(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "curl"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_curl_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Curl reports successful verification."""
    implementation = DebianCurl(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["curl", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_curl_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Curl reports failed verification."""
    run_stub.returncode = 127
    implementation = DebianCurl(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_curl_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Curl installation on Debian."""
    run_stub.returncode = 1
    implementation = DebianCurl(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_curl_installs_curl(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Curl installation runs the expected command."""
    implementation = FedoraCurl(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "curl"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_curl_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Curl reports successful verification."""
    implementation = FedoraCurl(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["curl", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_curl_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Curl reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraCurl(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_fedora_curl_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts Curl installation."""
    run_stub.returncode = 1
    implementation = FedoraCurl(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_curl_installs_curl(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Curl installation runs the expected command."""
    implementation = ArchCurl(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "curl"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_curl_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Curl reports successful verification."""
    implementation = ArchCurl(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["curl", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_curl_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Curl reports failed verification."""
    run_stub.returncode = 127
    implementation = ArchCurl(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_arch_curl_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts Curl installation."""
    run_stub.returncode = 1
    implementation = ArchCurl(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
