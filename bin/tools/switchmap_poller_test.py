#!/usr/bin/env python3
"""Switchmap-NG polling test script."""

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
from switchmap.poller import poll


def main():
    """Runs a test poll of the selected device.

    Args:
        None

    Returns:
        None

    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        description="""\
This script can be used to test whether your configuration is setup \
correctly to poll a specific device. If successful the content of the \
polling data for the host will be displayed on the screen.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # CLI argument for starting
    parser.add_argument(
        "--hostname",
        required=True,
        type=str,
        help="Hostname to test for pollability.",
    )
    args = parser.parse_args()

    # Poll
    poll.cli_device(args.hostname)


if __name__ == "__main__":
    main()
