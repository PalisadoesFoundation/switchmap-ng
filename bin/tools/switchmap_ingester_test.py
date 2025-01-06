#!/usr/bin/env python3
"""Switchmap-NG ingest test script."""

# Standard libraries
import sys
import os
import argparse

# Try to create a working PYTHONPATH
_SYS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_BIN_DIRECTORY = os.path.abspath(os.path.join(_SYS_DIRECTORY, os.pardir))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if (
    _SYS_DIRECTORY.endswith("{0}switchmap-ng{0}bin{0}tools".format(os.sep))
    is True
):
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "switchmap-ng{0}bin{0}tools" '
        "directory. Please fix.".format(os.sep)
    )
    sys.exit(2)

# Import app libraries
from switchmap.server.ingest import ingest
from switchmap.server import configuration
from switchmap.core import log


def main():
    """Runs a test poll of the selected device.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    config = configuration.ConfigServer()

    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        description="""\
This script can be used to test whether polled files sent the the \
switchmap server are being correctly loaded into the database without \
error. It is used as a troubleshooting tool. All data imported into the \
database is automatically deleted.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # CLI argument for starting
    parser.add_argument(
        "--cache_directory",
        required=True,
        type=str,
        help="Directory where the cache files are located.",
    )
    args = parser.parse_args()

    # Get the source directory
    cache_directory = args.cache_directory

    # Fail if the directory does not exist
    if bool(os.path.isdir(cache_directory)) is False:
        log_message = "Ingest directory {} does not exist".format(
            cache_directory
        )
        log.log2die(1051, log_message)

    # Ingest data
    _ingest = ingest.Ingest(
        config, test=True, test_cache_directory=args.cache_directory
    )
    _ingest.process()


if __name__ == "__main__":
    main()
