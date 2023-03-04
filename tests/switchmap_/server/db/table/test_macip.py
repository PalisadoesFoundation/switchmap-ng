#!/usr/bin/env python3
"""Test the macip module."""

import os
import sys
import unittest

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

from switchmap.server.db.table import macip as testimport
from switchmap.server.db.models import MacIp
from switchmap.server.db.table import IMacIp
from switchmap.server.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestDbTableMacIp(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

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
        # Create record
        row = _row()

        # Test before insertion of an initial row
        nonexistent = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertFalse(nonexistent)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        preliminary_result = testimport.exists(
            row.idx_device, row.idx_mac, row.ip_
        )
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test idx_index function
        result = testimport.idx_exists(preliminary_result.idx_macip)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_findip(self):
        """Testing function findip."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertFalse(result)

        # Test NotFound
        results = testimport.findip(row.idx_device, row.ip_)
        self.assertFalse(bool(result))

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertTrue(result)

        # Test Found
        results = testimport.findip(row.idx_device, row.ip_)
        self.assertEqual(len(results), 1)
        for result in results:
            self.assertTrue(bool(result))

    def test_findhostname(self):
        """Testing function findhostname."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.idx_mac, row.hostname)
        self.assertFalse(result)

        # Test NotFound
        results = testimport.findhostname(row.hostname)
        self.assertFalse(bool(result))

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertTrue(result)

        # Test Found
        results = testimport.findhostname(row.hostname)
        self.assertEqual(len(results), 1)
        for result in results:
            self.assertTrue(bool(result))

        # Test partial string
        partial = row.hostname[2:-2]
        results = testimport.findhostname(partial)
        self.assertEqual(len(results), 1)
        for result in results:
            self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing function insert_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.idx_device, row.idx_mac, row.ip_)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

        # Get random IP address
        ip_ = data.ip_()

        # Do an update
        idx = result.idx_macip
        updated_row = MacIp(
            idx_device=row.idx_device,
            idx_mac=row.idx_mac,
            ip_=ip_.address,
            hostname=data.random_string(),
            version=ip_.version,
            enabled=row.enabled,
        )
        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.exists(
            updated_row.idx_device, updated_row.idx_mac, updated_row.ip_
        )
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(updated_row))

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RMacIp to IMacIp record.

    Args:
        row: RMacIp/IMacIp record

    Returns:
        result: IMacIp result

    """
    # Do conversion
    result = IMacIp(
        idx_device=row.idx_device,
        idx_mac=row.idx_mac,
        ip_=row.ip_,
        hostname=row.hostname,
        version=row.version,
        enabled=row.enabled,
    )
    return result


def _row():
    """Create an IMacIp record.

    Args:
        None

    Returns:
        result: IMacIp object

    """
    # Initialize key variables
    ip_ = data.ip_()

    # Create result
    result = IMacIp(
        idx_device=1,
        idx_mac=1,
        ip_=ip_.address,
        hostname=data.random_string(),
        version=ip_.version,
        enabled=1,
    )
    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
