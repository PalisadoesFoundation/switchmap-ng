#!/usr/bin/env python3
"""Test the mib_essswitch module."""

import os
import sys
import unittest

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}switchmap-ng{0}tests{0}switchmap_{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


# Create the necessary configuration
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

from switchmap.db.table import location as testimport
from switchmap.db.models import Location
from switchmap.db.table import RLocation
from switchmap.db.table import ILocation
from switchmap.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestSuite(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Steps to execute when before tests start."""
        # Create database tables
        models.create_all_tables()

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_idx_exists(self):
        """Testing function idx_exists."""
        # Create record
        row = ILocation(
            name=data.random_string(),
            company_name=data.random_string(),
            address_0=data.random_string(),
            address_1=data.random_string(),
            address_2=data.random_string(),
            city=data.random_string(),
            state=data.random_string(),
            country=data.random_string(),
            postal_code=data.random_string(),
            phone=data.random_string(),
            notes=data.random_string(),
            enabled=1
        )

        # Test before insertion of an initial row
        nonexistent = testimport.exists(row.name)
        self.assertFalse(nonexistent)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        preliminary_result = testimport.exists(row.name)
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test idx_index function
        result = testimport.idx_exists(preliminary_result.idx_location)
        self.assertTrue(result)

    def test_exists(self):
        """Testing function exists."""
        # Create record
        row = ILocation(
            name=data.random_string(),
            company_name=data.random_string(),
            address_0=data.random_string(),
            address_1=data.random_string(),
            address_2=data.random_string(),
            city=data.random_string(),
            state=data.random_string(),
            country=data.random_string(),
            postal_code=data.random_string(),
            phone=data.random_string(),
            notes=data.random_string(),
            enabled=1
        )

        # Test before insertion of an initial row
        result = testimport.exists(row.name)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_insert_row(self):
        """Testing function insert_row."""
        # Create record
        row = ILocation(
            name=data.random_string(),
            company_name=data.random_string(),
            address_0=data.random_string(),
            address_1=data.random_string(),
            address_2=data.random_string(),
            city=data.random_string(),
            state=data.random_string(),
            country=data.random_string(),
            postal_code=data.random_string(),
            phone=data.random_string(),
            notes=data.random_string(),
            enabled=1
        )

        # Test before insertion of an initial row
        result = testimport.exists(row.name)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Create record
        row = ILocation(
            name=data.random_string(),
            company_name=data.random_string(),
            address_0=data.random_string(),
            address_1=data.random_string(),
            address_2=data.random_string(),
            city=data.random_string(),
            state=data.random_string(),
            country=data.random_string(),
            postal_code=data.random_string(),
            phone=data.random_string(),
            notes=data.random_string(),
            enabled=1
        )

        # Test before insertion of an initial row
        result = testimport.exists(row.name)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

        # Do an update
        idx = result.idx_location
        updated_row = ILocation(
            name=data.random_string(),
            company_name=row.company_name,
            address_0=row.address_0,
            address_1=row.address_1,
            address_2=row.address_2,
            city=row.city,
            state=row.city,
            country=row.country,
            postal_code=row.postal_code,
            phone=row.phone,
            notes=data.random_string(),
            enabled=row.enabled
        )
        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.exists(updated_row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(updated_row))

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RLocation to ILocation record.

    Args:
        row: RLocation/ILocation record

    Returns:
        result: ILocation result

    """
    # Do conversion
    result = ILocation(
        name=row.name,
        company_name=row.company_name,
        address_0=row.address_0,
        address_1=row.address_1,
        address_2=row.address_2,
        city=row.city,
        state=row.city,
        country=row.country,
        postal_code=row.postal_code,
        phone=row.phone,
        notes=row.notes,
        enabled=row.enabled
    )
    return result


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
