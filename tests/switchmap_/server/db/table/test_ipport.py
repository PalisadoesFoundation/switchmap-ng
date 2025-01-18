#!/usr/bin/env python3
"""Test the ipport module."""

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

from switchmap.server.db.table import ipport as testimport
from switchmap.server.db.models import IpPort
from switchmap.server.db.table import IIpPort
from switchmap.server.db import models

from tests.testlib_ import db


class TestDbTableIpPort(unittest.TestCase):
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
        # Start iterative tests
        for _ in range(1, db.TEST_MAXIMUM):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            nonexistent = testimport.exists(row.idx_l1interface, row.idx_ip)
            self.assertFalse(nonexistent)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            preliminary_result = testimport.exists(
                row.idx_l1interface, row.idx_ip
            )
            self.assertTrue(preliminary_result)
            self.assertEqual(_convert(preliminary_result), _convert(row))

            # Test idx_index function
            result = testimport.idx_exists(preliminary_result.idx_ipport)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Start iterative tests
        for _ in range(1, db.TEST_MAXIMUM):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(row.idx_l1interface, row.idx_ip)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(row.idx_l1interface, row.idx_ip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

    def test_find_idx_ip(self):
        """Testing function find_idx_ip."""
        # Initialize key variables
        finds = []

        # Test with known and unknown MACs
        for _ in range(1, db.TEST_MAXIMUM):
            row = _row()
            exists = testimport.exists(row.idx_l1interface, row.idx_ip)
            if bool(exists) is False:
                # Entry must not be found
                result = testimport.find_idx_ip(row.idx_ip)
                if row.idx_ip not in finds:
                    self.assertFalse(
                        bool(
                            testimport.exists(row.idx_l1interface, row.idx_ip)
                        )
                    )
                    # The combination idx_l1interface, idx_ip must not exist
                    for item in result:
                        self.assertFalse(
                            (item.idx_l1interface != row.idx_l1interface)
                            and (item.idx_ip != row.idx_ip)
                        )
                else:
                    for item in result:
                        self.assertEqual(item.idx_ip, row.idx_ip)
                    continue

                # Insert entry and then it should be found
                testimport.insert_row(row)
                now_exists = testimport.exists(row.idx_l1interface, row.idx_ip)
                self.assertTrue(bool(now_exists))
                post_result = testimport.find_idx_ip(now_exists.idx_ip)
                self.assertEqual(now_exists.idx_ip, row.idx_ip)

                # Test find
                for item in post_result:
                    self.assertEqual(item.idx_ip, row.idx_ip)
                self.assertTrue(bool(post_result))

                # Update found idx_ip values
                finds.append(now_exists.idx_ip)
            else:
                result = testimport.find_idx_ip(row.idx_ip)

                # Test find
                for item in result:
                    self.assertEqual(item.idx_ip, row.idx_ip)
                    self.assertEqual(item.idx_ip, exists.idx_ip)

                # Update found idx_ip values
                if exists.idx_ip not in finds:
                    finds.append(exists.idx_ip)

    def test_insert_row(self):
        """Testing function insert_row."""
        # Start iterative tests
        for _ in range(1, db.TEST_MAXIMUM):
            # Find a row combination that does not exist
            while True:
                # Create record
                row = _row()

                # Test before insertion of an initial row
                result = testimport.exists(row.idx_l1interface, row.idx_ip)
                if bool(result) is False:
                    self.assertFalse(result)
                    break

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(row.idx_l1interface, row.idx_ip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Start iterative tests
        for _ in range(1, db.TEST_MAXIMUM):
            # Create a reference to a row that is not in the database
            while True:
                idx_l1interface = random.randint(1, db.TEST_MAXIMUM)
                idx_ip = random.randint(1, db.TEST_MAXIMUM)

                found = testimport.exists(idx_l1interface, idx_ip)
                if bool(found) is True:
                    break

            # Create an updated record
            idx = found.idx_ipport
            new_idx_l1interface = random.randint(1, db.TEST_MAXIMUM)
            new_idx_ip = random.randint(1, db.TEST_MAXIMUM)
            updated_row = IpPort(
                idx_l1interface=new_idx_l1interface,
                idx_ip=new_idx_ip,
                enabled=found.enabled,
            )

            # Check if the new update alredy exists
            new_found = testimport.exists(new_idx_l1interface, new_idx_ip)
            if bool(new_found) is False:
                testimport.update_row(idx, updated_row)

                # Test the update
                result = testimport.exists(
                    updated_row.idx_l1interface, updated_row.idx_ip
                )
                self.assertTrue(result)
                self.assertEqual(_convert(result), _convert(updated_row))

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RIpPort to IIpPort record.

    Args:
        row: RIpPort/IIpPort record

    Returns:
        result: IIpPort result

    """
    # Do conversion
    result = IIpPort(
        idx_l1interface=row.idx_l1interface,
        idx_ip=row.idx_ip,
        enabled=row.enabled,
    )
    return result


def _row():
    """Create an IIpPort record.

    Args:
        None

    Returns:
        result: IIpPort object

    """
    # Create a reference to a row that is not in the database
    while True:
        idx_l1interface = random.randint(1, db.TEST_MAXIMUM)
        idx_ip = random.randint(1, db.TEST_MAXIMUM)

        # Create result
        result = IIpPort(
            idx_l1interface=idx_l1interface,
            idx_ip=idx_ip,
            enabled=1,
        )

        found = testimport.exists(idx_l1interface, idx_ip)
        if bool(found) is False:
            break

    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
