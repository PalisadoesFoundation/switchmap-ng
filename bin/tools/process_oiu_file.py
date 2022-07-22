#!/usr/bin/env python3
"""Script to update the Oui table."""

# Standard imports
import sys
import os
import argparse

import pandas

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

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Oui
from switchmap.db.table import oui
from switchmap.db.table import IOui


def main():
    """Create database.

    Args:
        None

    Returns:
        None

    """
    # Read Oui file
    args = _cli()
    df_ = _read_file(args.filename)
    _update_db(df_)


def _update_db(df_):
    """Update the database with Oui data.

    Args:
        df_: pd.Dataframe

    Returns:
        None

    """
    # Initialize key variables
    inserts = []

    # Process DataFrame (Enables)
    for _, row in df_.iterrows():
        db_record = oui.exists(row["oui"])
        file_record = IOui(
            oui=row["oui"], organization=row["organization"], enabled=1
        )

        # Process insertions and updates
        if bool(db_record) is False:
            inserts.append(file_record)
        else:
            if db_record.organization != file_record.organization:
                oui.update_row(db_record.idx_oui, file_record)

    # Do insertions
    if bool(inserts):
        oui.insert_row(inserts)


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
    args = parser.parse_args()
    return args


def _read_file(filepath):
    """Read Oui file.

    Args:
        filepath: Name of file to process

    Returns:
        df_: DataFrame of data

    """
    # Initialize key variables
    df_ = pandas.read_csv(filepath, delimiter=":")
    df_.columns = ["oui", "organization"]
    return df_


if __name__ == "__main__":
    # Run main
    main()
