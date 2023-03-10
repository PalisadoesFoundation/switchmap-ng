#!/usr/bin/env python3
"""Test the ip module."""

import os
import sys
import unittest
from random import randint
from collections import namedtuple

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

from switchmap.server.db.table import ip as testimport
from switchmap.server.db.models import Ip
from switchmap.server.db.table import IIp
from switchmap.server.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestDbTableIp(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    idx_zone = 1
    loops = 1

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
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
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_idx_exists(self):
        """Testing function idx_exists."""
        # Repeat test
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            nonexistent = testimport.exists(self.idx_zone, row.address)
            self.assertFalse(nonexistent)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            preliminary_result = testimport.exists(self.idx_zone, row.address)
            self.assertTrue(preliminary_result)
            self.assertEqual(_convert(preliminary_result), _convert(row))

            # Test idx_index function
            result = testimport.idx_exists(preliminary_result.idx_ip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Repeat test
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(self.idx_zone, row.address)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(self.idx_zone, row.address)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

    def test_findip(self):
        """Testing function findip."""
        # Repeat test
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            idx_zone = row.idx_zone
            result = testimport.findip(idx_zone, row.address)
            self.assertFalse(bool(result))

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.findip(idx_zone, row.address)
            self.assertTrue(bool(result))
            self.assertTrue(isinstance(result, list))
            self.assertEqual(len(result), 1)
            self.assertEqual(_convert(result[0]), _convert(row))

    def test_insert_row(self):
        """Testing function insert_row."""
        # Repeat test
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(self.idx_zone, row.address)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(self.idx_zone, row.address)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Repeat test
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(self.idx_zone, row.address)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(self.idx_zone, row.address)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

            # Do an update
            idx = result.idx_ip
            updated_row = Ip(
                idx_zone=row.idx_zone,
                address=data.ipv4() if row.version == 4 else data.ipv6(),
                version=row.version,
                hostname=row.hostname,
                enabled=row.enabled,
            )
            testimport.update_row(idx, updated_row)

            # Test the update
            result = testimport.exists(self.idx_zone, updated_row.address)
            self.assertTrue(result)

            # The newly generated MAC address will not have an OUI entry.
            self.assertEqual(result.enabled, updated_row.enabled)
            self.assertEqual(result.address, updated_row.address)
            self.assertEqual(result.idx_zone, updated_row.idx_zone)

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RIp to IIp record.

    Args:
        row: RIp/IIp record

    Returns:
        result: IIp result

    """
    # Do conversion
    result = IIp(
        idx_zone=row.idx_zone,
        address=row.address,
        version=row.version,
        hostname=row.hostname,
        enabled=row.enabled,
    )
    return result


def _row():
    """Create an IIp record.

    Args:
        None

    Returns:
        result: IIp object

    """
    # Initialize key variables
    found = True
    idx_zone = 1
    IP = namedtuple("IP", "version address")
    ips = (
        (IP(version=4, address=data.ipv4())),
        (IP(version=6, address=data.ipv6())),
    )

    while True:
        # Get an IP address
        item = ips[randint(0, 1)]

        # Create result
        result = IIp(
            idx_zone=idx_zone,
            address=item.address,
            version=item.version,
            hostname=data.random_string(),
            enabled=1,
        )

        found = bool(testimport.exists(idx_zone, item.address))
        if bool(found) is False:
            break

    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
