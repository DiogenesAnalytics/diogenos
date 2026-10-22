"""Define the DiogenOS command-line interface."""

import click


@click.group(no_args_is_help=True)
def main() -> None:
    """Configure and manage a DiogenOS environment."""


if __name__ == "__main__":
    main()
