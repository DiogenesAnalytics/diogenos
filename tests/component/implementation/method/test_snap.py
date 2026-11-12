"""Test the Snap installation method."""

from typing import Tuple

import pytest

from diogenos.component.implementation.command import Command
from diogenos.component.implementation.method.operations import SnapOperation
from diogenos.component.implementation.method.snap import SnapMethod
from diogenos.component.implementation.method.snap import SnapOptions


@pytest.mark.parametrize(
    ("options", "packages", "expected"),
    (
        (
            SnapOptions(),
            ("firefox",),
            ("sudo", "snap", "install", "firefox"),
        ),
        (
            SnapOptions(classic=True),
            ("firefox",),
            ("sudo", "snap", "install", "--classic", "firefox"),
        ),
        (
            SnapOptions(channel="candidate"),
            ("firefox",),
            (
                "sudo",
                "snap",
                "install",
                "--channel",
                "candidate",
                "firefox",
            ),
        ),
        (
            SnapOptions(channel="beta", classic=True),
            ("firefox",),
            (
                "sudo",
                "snap",
                "install",
                "--classic",
                "--channel",
                "beta",
                "firefox",
            ),
        ),
        (
            SnapOptions(),
            ("firefox", "curl"),
            ("sudo", "snap", "install", "firefox", "curl"),
        ),
    ),
)
@pytest.mark.component
def test_build(
    options: SnapOptions,
    packages: Tuple[str, ...],
    expected: Tuple[str, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test building Snap installation commands."""
    monkeypatch.setattr(
        "diogenos.component.implementation.execution.os.geteuid",
        lambda: 1000,
    )

    method = SnapMethod(options)

    command = method.build(SnapOperation.INSTALL, packages)

    assert command == Command.from_arguments(expected)
