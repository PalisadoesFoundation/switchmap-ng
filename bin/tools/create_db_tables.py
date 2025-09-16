#!/usr/bin/env python3
"""Script to create database."""

# Standard imports
import sys
import os

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

# Switchmap-NG standard imports
from switchmap.server.db.misc import oui as _oui
from switchmap.server.db.table import oui
from switchmap.server.db.table import event
from switchmap.server.db.table import root
from switchmap.server.db.table import IOui
from switchmap.server.db.table import IRoot
from switchmap.server.db import models


def main():
    """Create database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    oui_filepath = """\
{1}{0}setup{0}data{0}mac_address_file.txt""".format(
        os.sep, _ROOT_DIRECTORY
    )

    # Create database
    models.create_all_tables()

    # Create the default event
    exists = event.idx_exists(1)
    if bool(exists) is False:
        warning_message = "SWITCHMAP - DO NOT DELETE THIS ROW"
        _event = event.create(name=warning_message)
        root.insert_row(
            IRoot(
                idx_event=_event.idx_event,
                name=warning_message,
                enabled=1,
            )
        )
        # oui.insert_row(
        #     IOui(
        #         oui=None,
        #         organization=None,
        #         enabled=1,
        #     )
        # )
        # Skip dummy OUI insertion - real data will be populated from file

    # Populate the OUI data
    _oui.update_db_oui(oui_filepath)


if __name__ == "__main__":
    # Run main
    main()
