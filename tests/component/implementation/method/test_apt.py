"""Test the APT installation method."""

from typing import Tuple

import pytest

from diogenos.component.implementation.method.apt import APTMethod
from diogenos.component.implementation.method.apt import APTOptions


@pytest.mark.parametrize(
    ("options", "packages", "expected"),
    (
        (
            APTOptions(),
            ("firefox",),
            ("sudo", "apt-get", "install", "-y", "firefox"),
        ),
        (
            APTOptions(assume_yes=False),
            ("firefox",),
            ("sudo", "apt-get", "install", "firefox"),
        ),
        (
            APTOptions(no_install_recommends=True),
            ("firefox",),
            (
                "sudo",
                "apt-get",
                "install",
                "-y",
                "--no-install-recommends",
                "firefox",
            ),
        ),
        (
            APTOptions(),
            ("firefox", "curl"),
            ("sudo", "apt-get", "install", "-y", "firefox", "curl"),
        ),
    ),
)
@pytest.mark.component
def test_build(
    options: APTOptions,
    packages: Tuple[str, ...],
    expected: Tuple[str, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test building APT installation commands."""
    monkeypatch.setattr(
        "diogenos.component.implementation.execution.os.geteuid",
        lambda: 1000,
    )

    method = APTMethod(options)

    assert method.build(packages) == expected
