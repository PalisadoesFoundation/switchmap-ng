#!/usr/bin/env python3
"""Switchmap-NG  script to create database."""

# Standard imports
import sys
import os

# Try to create a working PYTHONPATH
script_directory = os.path.dirname(os.path.realpath(__file__))
bin_directory = os.path.abspath(os.path.join(script_directory, os.pardir))
root_directory = os.path.abspath(os.path.join(bin_directory, os.pardir))
if script_directory.endswith(
        '{0}switchmap-ng{0}bin{0}tools'.format(os.sep)) is True:
    sys.path.append(root_directory)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin/tools" '
        'directory. Please fix.')
    sys.exit(2)

# Switchmap-NG standard imports
from switchmap.db import models


def main():
    """Create database.

    Args:
        None

    Returns:
        None

    """
    # Create database
    models.create_all_tables()


if __name__ == '__main__':
    # Run main
    main()
