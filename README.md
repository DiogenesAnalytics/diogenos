[![tests](https://github.com/DiogenesAnalytics/diogenos/workflows/tests/badge.svg)][tests]
[![Docker](https://github.com/DiogenesAnalytics/diogenos/workflows/docker/badge.svg)][docker]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[tests]: https://github.com/DiogenesAnalytics/diogenos/actions?workflow=tests
[docker]: https://github.com/DiogenesAnalytics/diogenos/actions?workflow=docker
[black]: https://github.com/psf/black

# DiogenOS

> **Diogenes, but as an operating system.**

DiogenOS is a minimal, rigorously defined Linux environment.

Rather than maintaining a collection of installation scripts, configuration files, and undocumented system modifications, DiogenOS defines the desired state of a machine and provides the tools to bring a Linux system into that state.

```text
Current State → DiogenOS → Desired State
```

The goal is simple:

> **Define what a useful computer should be, then make it so.**

DiogenOS is built around two principles:

* **Minimalism** — install and configure only what is actually needed.
* **Logical rigor** — make system state explicit, reproducible, testable, and verifiable.

## Installation

DiogenOS is currently under development.

To install the development version:

```console
$ pip install git+https://github.com/DiogenesAnalytics/diogenos
```

## Status

DiogenOS is in the early stages of development. The initial implementation focuses on configuring a Linux system into a defined personal computing environment.

## License

Distributed under the terms of the [MIT license][license],
*DiogenOS* is free and open source software.

[license]: https://github.com/DiogenesAnalytics/diogenos/blob/main/LICENSE
[black]: https://github.com/psf/black
