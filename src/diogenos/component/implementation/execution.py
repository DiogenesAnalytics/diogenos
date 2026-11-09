"""Provide command execution utilities."""

import os
import tempfile
import urllib.request
from pathlib import Path
from typing import List
from typing import Sequence


def privileged_command(command: Sequence[str]) -> List[str]:
    """Prepare a command for privileged execution."""
    if os.geteuid() == 0:
        return list(command)

    return ["sudo", *command]


def prepare_command(
    command: Sequence[str],
    *,
    privileged: bool = False,
) -> List[str]:
    """Prepare a command for execution."""
    executable = list(command)

    if privileged:
        executable = privileged_command(executable)

    return executable


def download_file(
    url: str,
    destination: Path,
    *,
    chunk_size: int = 1024 * 1024,
) -> None:
    """Download a file while reporting progress."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "DiogenOS"},
    )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=destination.parent,
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)

            with urllib.request.urlopen(request, timeout=30) as response:
                content_length = response.headers.get("Content-Length")
                total_size = int(content_length) if content_length else None

                downloaded = 0

                while chunk := response.read(chunk_size):
                    temporary_file.write(chunk)
                    downloaded += len(chunk)

                    if total_size is not None:
                        percentage = downloaded / total_size * 100
                        progress = (
                            f"\rDownloading: {percentage:5.1f}% "
                            f"({downloaded:,} / {total_size:,} bytes)"
                        )
                    else:
                        progress = f"\rDownloading: {downloaded:,} bytes"

                    print(progress, end="", flush=True)

                if total_size is not None and downloaded != total_size:
                    raise RuntimeError(
                        f"incomplete download: expected {total_size} bytes, "
                        f"received {downloaded} bytes",
                    )

        temporary_path.replace(destination)

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    print()
