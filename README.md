# bpq
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat)](https://github.com/badpacketsllc/bpq/graphs/commit-activity)
![Build Status](https://github.com/badpacketsllc/bpq/workflows/ci/badge.svg?style=flat)
![PyPI - Downloads](https://img.shields.io/pypi/dm/bpq?style=flat)
[![Docker image download](https://img.shields.io/docker/pulls/badpacketsllc/bpq?style=flat)](https://hub.docker.com/r/badpacketsllc/bpq)
[![License](https://img.shields.io/github/license/badpacketsllc/bpq?style=flat)](https://github.com/badpacketsllc/bpq/blob/main/LICENSE)
[![Follow us on twitter](https://img.shields.io/twitter/follow/bad_packets.svg?style=social)](https://twitter.com/bad_packets/)

A suite of helpful tools for interacting with the [Bad Packets Cyber Threat
Intelligence API](https://docs.badpackets.net/).

# Getting started

## Environment requirements
In order to run the code in this repository, you need to have a standard
release of Python version 3.6 or higher installed. No additional libraries are
required.

If you prefer running your applications in containers, skip to the
[container build and run section](#building-the-application-container).

## Installing
```shell
$ python3 -m pip install bpq
```

## Building
If you prefer to install `bpq` using a local build, you can do so using `pip`.

```shell
$ python3 -m pip install .
```

## Running the CLI tool
```shell
$ bpq -h
usage: bpq [-h]  # ... usage information follows

Pulls Bad Packets CTI data. All arguments given at the command line can be
specified using environment variables. For example, a command line option of
`--output-format csv` is equivalent to setting the environment variable
`OUTPUT_FORMAT=csv`. Any argument not specified will be populated with an
environment variable or the default value indicated in `--help`.

# ... argument documentation follows
```

### Running without building
You can still run the command line application without building a package if
you like. Just run `python3 -m bpq.cli` instead of `bpq`.


## Examples
You can find example scripts (using this CLI tool, the Python API and `curl`)
in the project's `examples`
[directory](https://github.com/badpacketsllc/bpq/-/tree/main/examples).

## Another note on authenticating and using command line arguments
The shell script will attempt to resolve parameters from environment variables.
The most important environment variables are:

| Variable name         | Description                                                              |
|-----------------------|--------------------------------------------------------------------------|
| BAD_PACKETS_API_TOKEN | Token use for API authentication                                         |
| LOG_LEVEL             | Log verbosity. Can have a value of `ERROR`, `WARNING`, `DEBUG` or `INFO` |

If no environment variable exists or a command line argument is given,
the tool will take the command line argument (i.e. command line arguments
always have priority over environment variables).

# Developing
Development help is always welcome! Full documentation on how to get started is
in the project's
[CONTRIBUTING.rst](https://github.com/badpacketsllc/bpq/-/blob/main/CONTRIBUTING.rst)
file.
Please be nice and follow our
[code of conduct](https://github.com/badpacketsllc/bpq/-/blob/main/CODE-OF-CONDUCT.md)
whenever you participate.

## Building the application container
This application is designed to run only in an unprivileged container as a
non-root user. Docker and Podman are supported for building container images,
and we currently support Alpine and
[Red Hat Universal Base Image (UBI)](https://developers.redhat.com/products/rhel/ubi)
as base operating systems.
You can control the version of Python defining the `PYTHON_VERSION` parameter
at build time.

### Using `docker`
To build a container with the default base image (Python 3.9 running on the
latest stable version of Alpine), run

`docker build --rm --no-cache -t bpq .`

The `PYTHON_VERSION` build argument can be used to control which
version of Python you are using. For example,
`docker build --rm --no-cache --build-arg PYTHON_VERSION=3.6 -t bpq .`
will build an application image running Python 3.6.

### Using `podman`
`podman build --rm --no-cache -t bpq .`

Note that `podman` reads `Containerfile` by default, which builds from the
[Red Hat Universal Base Image (UBI)](https://developers.redhat.com/products/rhel/ubi)
rather than images from Docker Hub. Due to Red Hat's naming conventions, Python
versions should be formatted as `${major}${minor}` rather than
`${major}.${minor}`. Concretely, `--build-arg PYTHON_VERSION=38` will build a
container that runs Python 3.8. If you  do not want to use the Python UBI at
all, pass `--file Dockerfile` to `podman`.

## Running the application container
`docker run -e BAD_PACKETS_API_TOKEN=${BAD_PACKETS_API_TOKEN} bpq` if using
Docker. `podman run -e BAD_PACKETS_API_TOKEN=${BAD_PACKETS_API_TOKEN} bpq` if
using Podman.

Contributing
------------

Contributions are encouraged! Learn how to contribute by reading
[CONTRIBUTING.md](https://github.com/badpacketsllc/bpq/blob/main/CONTRIBUTING.md).
Please be nice and follow our
[Code of Conduct](https://github.com/badpacketsllc/bpq/blob/main/CODE_OF_CONDUCT.md).

License
-------

GPLv3

Author Information
------------------

[Mathew Woodyard](https://www.matwoodyard.com)

[Bad Packets LLC](https://badpackets.net)
