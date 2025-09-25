#!/usr/bin/env python3
"""Script to update the Oui table."""

# Standard imports
import os
import argparse
import sys

# Try to create a working PYTHONPATH
_SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_BIN_DIRECTORY = os.path.abspath(os.path.join(_SCRIPT_DIRECTORY, os.pardir))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if (
    _SCRIPT_DIRECTORY.endswith("{0}switchmap-ng{0}bin{0}tools".format(os.sep))
    is True
):
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin/tools" '
        "directory. Please fix."
    )
    sys.exit(2)

# Package imports
from switchmap.server.db.misc import oui as _oui


def main():
    """Update database with OUI data.

    Args:
        None

    Returns:
        None

    """
    # Read Oui file
    args = _cli()
    #  _oui.update_db_oui(args.filename, new=args.new_installation)
    _oui.update_db_oui(args.filename)


def _cli():
    """Process the CLI.

    Args:
        None

    Returns:
        args: Parsed CLI arguments

    """
    # Initialize key variables
    default_filepath = """\
{1}{0}setup{0}data{0}mac_address_file.txt""".format(
        os.sep, _ROOT_DIRECTORY
    )

    # Get CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        default=default_filepath,
        type=str,
        help=("Oui filename to process. Default: {}".format(default_filepath)),
    )
    parser.add_argument(
        "-n",
        "--new_installation",
        action="store_true",
        help=(
            """New installation. Checks for existing OUI database entries are \
not done"""
        ),
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # Run main
    main()
