"""Test the Firefox component and its implementations."""

import subprocess

import pytest
from pytest import MonkeyPatch

from diogenos.component.catalog.browser.firefox.firefox import ArchFirefox
from diogenos.component.catalog.browser.firefox.firefox import DebianFirefox
from diogenos.component.catalog.browser.firefox.firefox import FedoraFirefox
from diogenos.component.catalog.browser.firefox.firefox import FirefoxPackage
from diogenos.component.catalog.browser.firefox.firefox import UbuntuFirefox
from diogenos.system.base import System
from tests.component.support import RunStub


@pytest.mark.component
def test_firefox_component_is_satisfied_when_firefox_is_available(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Firefox is satisfied when firefox --version succeeds."""
    component = FirefoxPackage(run=run_stub)

    assert component.is_satisfied(system) is True
    assert run_stub.calls == [
        (
            ["firefox", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_firefox_component_is_satisfied_when_firefox_esr_is_available(
    system: System,
) -> None:
    """Verify that Firefox is satisfied when only Firefox ESR is available."""
    calls = []

    def run(
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(
            args=command,
            returncode=127 if command[0] == "firefox" else 0,
            stdout="",
            stderr="",
        )

    component = FirefoxPackage(run=run)

    assert component.is_satisfied(system) is True
    assert calls == [
        (
            ["firefox", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
        (
            ["firefox-esr", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_firefox_component_is_not_satisfied_when_firefox_is_unavailable(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Firefox is not satisfied when neither executable is available."""
    run_stub.returncode = 127
    component = FirefoxPackage(run=run_stub)

    assert component.is_satisfied(system) is False
    assert len(run_stub.calls) == 2


@pytest.mark.component
def test_firefox_component_returns_implementations(
    system: System,
) -> None:
    """Verify that the Firefox component exposes compatible implementations."""
    component = FirefoxPackage()

    implementations = component.implementations()

    assert any(implementation.supports(system) for implementation in implementations)


@pytest.mark.component
def test_ubuntu_firefox_installs_firefox(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu Firefox installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = UbuntuFirefox(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["snap", "install", "firefox"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_firefox_installs_firefox_with_sudo(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Ubuntu Firefox installation uses sudo when not running as root."""
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    implementation = UbuntuFirefox(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["sudo", "snap", "install", "firefox"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_ubuntu_firefox_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Firefox reports successful verification."""
    implementation = UbuntuFirefox(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["firefox", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_ubuntu_firefox_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Ubuntu Firefox reports failed verification."""
    run_stub.returncode = 127
    implementation = UbuntuFirefox(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_ubuntu_firefox_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Snap failure interrupts Firefox installation."""
    run_stub.returncode = 1
    implementation = UbuntuFirefox(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_debian_firefox_installs_firefox(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Debian Firefox installation runs the expected commands."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = DebianFirefox(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["apt-get", "update"],
            {"check": True},
        ),
        (
            ["apt-get", "install", "-y", "firefox-esr"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_debian_firefox_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Firefox reports successful verification."""
    implementation = DebianFirefox(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["firefox-esr", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_debian_firefox_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Debian Firefox reports failed verification."""
    run_stub.returncode = 127
    implementation = DebianFirefox(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_debian_firefox_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that an APT failure interrupts Firefox installation."""
    run_stub.returncode = 1
    implementation = DebianFirefox(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_fedora_firefox_installs_firefox(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Fedora Firefox installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = FedoraFirefox(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["dnf", "install", "-y", "firefox"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_fedora_firefox_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Firefox reports successful verification."""
    implementation = FedoraFirefox(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["firefox", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_fedora_firefox_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Fedora Firefox reports failed verification."""
    run_stub.returncode = 127
    implementation = FedoraFirefox(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_fedora_firefox_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a DNF failure interrupts Firefox installation."""
    run_stub.returncode = 1
    implementation = FedoraFirefox(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)


@pytest.mark.component
def test_arch_firefox_installs_firefox(
    system: System,
    run_stub: RunStub,
    monkeypatch: MonkeyPatch,
) -> None:
    """Verify that Arch Firefox installation runs the expected command."""
    monkeypatch.setattr("os.geteuid", lambda: 0)
    implementation = ArchFirefox(run=run_stub)

    implementation.install(system)

    assert run_stub.calls == [
        (
            ["pacman", "-S", "--noconfirm", "firefox"],
            {"check": True},
        ),
    ]


@pytest.mark.component
def test_arch_firefox_verifies_successful_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Firefox reports successful verification."""
    implementation = ArchFirefox(run=run_stub)

    assert implementation.verify(system) is True
    assert run_stub.calls == [
        (
            ["firefox", "--version"],
            {
                "capture_output": True,
                "check": False,
                "text": True,
            },
        ),
    ]


@pytest.mark.component
def test_arch_firefox_verifies_failed_installation(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that Arch Firefox reports failed verification."""
    run_stub.returncode = 127
    implementation = ArchFirefox(run=run_stub)

    assert implementation.verify(system) is False


@pytest.mark.component
def test_arch_firefox_installation_propagates_command_failure(
    system: System,
    run_stub: RunStub,
) -> None:
    """Verify that a Pacman failure interrupts Firefox installation."""
    run_stub.returncode = 1
    implementation = ArchFirefox(run=run_stub)

    with pytest.raises(subprocess.CalledProcessError):
        implementation.install(system)
