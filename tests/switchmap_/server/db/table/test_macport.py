#!/usr/bin/env python3
"""Test the macport module."""

import os
import sys
import unittest
import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(
                            os.path.join(
                                os.path.abspath(
                                    os.path.join(EXEC_DIR, os.pardir)
                                ),
                                os.pardir,
                            )
                        ),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}table""".format(
    os.sep
)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.server.db.table import macport as testimport
from switchmap.server.db.models import MacPort
from switchmap.server.db.table import IMacPort
from switchmap.server.db import models

from tests.testlib_ import db


class TestDbTableMacPort(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUp(cls):
        """Execute these steps before starting each test."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

        # Create database tables
        models.create_all_tables()

        # Pollinate db with prerequisites
        db.populate()

    @classmethod
    def tearDown(cls):
        """Execute these steps after each tests is completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_idx_exists(self):
        """Testing function idx_exists."""
        # Create record
        while True:
            row = _row()
            if not testimport.exists(row.idx_l1interface, row.idx_mac):
                break

        # Test before insertion
        nonexistent = testimport.exists(row.idx_l1interface, row.idx_mac)
        self.assertFalse(nonexistent)

        # Insert
        testimport.insert_row(row)
        preliminary_result = testimport.exists(row.idx_l1interface, row.idx_mac)
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test idx_index function
        result = testimport.idx_exists(preliminary_result.idx_macport)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Create record
        while True:
            row = _row()
            if not testimport.exists(row.idx_l1interface, row.idx_mac):
                break

        # Test before insertion
        result = testimport.exists(row.idx_l1interface, row.idx_mac)
        self.assertFalse(result)

        # Insert
        testimport.insert_row(row)
        result = testimport.exists(row.idx_l1interface, row.idx_mac)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_find_idx_mac(self):
        """Testing function find_idx_mac."""
        # Initialize key variables
        finds = []

        # Test with known and unknown MACs
        for _ in range(1, db.TEST_MAXIMUM):
            row = _row()
            exists = testimport.exists(row.idx_l1interface, row.idx_mac)
            if bool(exists) is False:
                # Entry must not be found
                result = testimport.find_idx_mac(row.idx_mac)
                if row.idx_mac not in finds:
                    self.assertFalse(
                        bool(
                            testimport.exists(row.idx_l1interface, row.idx_mac)
                        )
                    )
                    # The combination idx_l1interface, idx_mac must not exist
                    for item in result:
                        self.assertFalse(
                            (item.idx_l1interface != row.idx_l1interface)
                            and (item.idx_mac != row.idx_mac)
                        )
                else:
                    for item in result:
                        self.assertEqual(item.idx_mac, row.idx_mac)
                    continue

                # Insert entry and then it should be found
                testimport.insert_row(row)
                now_exists = testimport.exists(row.idx_l1interface, row.idx_mac)
                self.assertTrue(bool(now_exists))
                post_result = testimport.find_idx_mac(now_exists.idx_mac)
                self.assertEqual(now_exists.idx_mac, row.idx_mac)

                # Test find
                for item in post_result:
                    self.assertEqual(item.idx_mac, row.idx_mac)
                self.assertTrue(bool(post_result))

                # Update found idx_mac values
                finds.append(now_exists.idx_mac)
            else:
                result = testimport.find_idx_mac(row.idx_mac)

                # Test find
                for item in result:
                    self.assertEqual(item.idx_mac, row.idx_mac)
                    self.assertEqual(item.idx_mac, exists.idx_mac)

                # Update found idx_mac values
                if exists.idx_mac not in finds:
                    finds.append(exists.idx_mac)

    def test_insert_row(self):
        """Testing function insert_row."""
        # Find a row combination that does not exist
        while True:
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(row.idx_l1interface, row.idx_mac)
            if bool(result) is False:
                self.assertFalse(result)
                break

        # Test after insertion
        testimport.insert_row(row)
        result = testimport.exists(row.idx_l1interface, row.idx_mac)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Find a row combination that does exist
        while True:
            row = _row()
            result = testimport.exists(row.idx_l1interface, row.idx_mac)
            if bool(result) is True:
                self.assertTrue(result)
                break

        # Do an update
        idx = result.idx_macport
        updated_row = MacPort(
            idx_l1interface=random.randint(1, db.TEST_MAXIMUM),
            idx_mac=random.randint(1, db.TEST_MAXIMUM),
            enabled=row.enabled,
        )
        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.exists(
            updated_row.idx_l1interface, updated_row.idx_mac
        )
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(updated_row))

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RMacPort to IMacPort record.

    Args:
        row: RMacPort/IMacPort record

    Returns:
        result: IMacPort result

    """
    # Do conversion
    result = IMacPort(
        idx_l1interface=row.idx_l1interface,
        idx_mac=row.idx_mac,
        enabled=row.enabled,
    )
    return result


def _row():
    """Create an IMacPort record.

    Args:
        None

    Returns:
        result: IMacPort object

    """
    # Create result
    result = IMacPort(
        idx_l1interface=random.randint(1, db.TEST_MAXIMUM),
        idx_mac=random.randint(1, db.TEST_MAXIMUM),
        enabled=1,
    )
    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
