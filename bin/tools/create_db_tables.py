#!/usr/bin/env python3
"""Script to create database."""

# Standard imports
import sys
import os

# Try to create a working PYTHONPATH
_SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_BIN_DIRECTORY = os.path.abspath(os.path.join(_SCRIPT_DIRECTORY, os.pardir))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _SCRIPT_DIRECTORY.endswith(
        '{0}switchmap-ng{0}bin{0}tools'.format(os.sep)) is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin/tools" '
        'directory. Please fix.')
    sys.exit(2)

# Switchmap-NG standard imports
from switchmap.db import models
from switchmap.db.table import ILocation
from switchmap.db.table import location


def main():
    """Create database.

    Args:
        None

    Returns:
        None

    """
    # Create database
    models.create_all_tables()

    # Create the default location
    exists = location.idx_exists(1)
    if bool(exists) is False:
        location.insert_row(
            ILocation(
                name='Default',
                company_name='',
                address_0='',
                address_1='',
                address_2='',
                city='',
                state='',
                country='',
                postal_code='',
                phone='',
                notes='',
                enabled=1,
            )
        )


if __name__ == '__main__':
    # Run main
    main()
