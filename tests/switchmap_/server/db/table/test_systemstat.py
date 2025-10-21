#!/usr/bin/env python3
"""Test the systemstat module."""

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

from switchmap.server.db.table import systemstat as testimport
from switchmap.server.db.table import ISystemStat
from switchmap.server.db.table import device
from switchmap.server.db.table import IDevice
from switchmap.server.db import models

from tests.testlib_ import db
from tests.testlib_ import data
import random


class TestDbTableSystemStat(unittest.TestCase):
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
        # Get a device to use
        _device = _create_device()

        # Create systemstat record
        row = _row(_device.idx_device)

        # Test before insertion
        result = testimport.idx_exists(999999)
        self.assertFalse(result)

        # Test after insertion
        testimport.insert_row(row)
        result = testimport.device_exists(_device.idx_device)
        self.assertTrue(result)

        # Test idx_exists function
        result = testimport.idx_exists(result.idx_systemstat)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_device_exists(self):
        """Testing function device_exists."""
        # Get a device to use
        _device = _create_device()

        # Create systemstat record
        row = _row(_device.idx_device)

        # Test before insertion
        result = testimport.device_exists(_device.idx_device)
        self.assertFalse(result)

        # Test after insertion
        testimport.insert_row(row)
        result = testimport.device_exists(_device.idx_device)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_insert_row_single(self):
        """Testing function insert_row with single row."""
        # Get a device to use
        _device = _create_device()

        # Create systemstat record
        row = _row(_device.idx_device)

        # Test before insertion
        result = testimport.device_exists(_device.idx_device)
        self.assertFalse(result)

        # Test after insertion of a single row
        testimport.insert_row(row)
        result = testimport.device_exists(_device.idx_device)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_insert_row_list(self):
        """Testing function insert_row with list of rows."""
        # Get devices to use
        device1 = _create_device()
        device2 = _create_device()

        # Create systemstat records
        row1 = _row(device1.idx_device)
        row2 = _row(device2.idx_device)
        rows = [row1, row2]

        # Test before insertion
        result1 = testimport.device_exists(device1.idx_device)
        result2 = testimport.device_exists(device2.idx_device)
        self.assertFalse(result1)
        self.assertFalse(result2)

        # Test after insertion of multiple rows
        testimport.insert_row(rows)
        result1 = testimport.device_exists(device1.idx_device)
        result2 = testimport.device_exists(device2.idx_device)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(_convert(result1), _convert(row1))
        self.assertEqual(_convert(result2), _convert(row2))

    def test_insert_row_duplicates(self):
        """Testing function insert_row with duplicate rows."""
        # Get a device to use
        _device = _create_device()

        # Create duplicate systemstat records
        row = _row(_device.idx_device)
        rows = [row, row, row]

        # Test before insertion
        result = testimport.device_exists(_device.idx_device)
        self.assertFalse(result)

        # Test after insertion - duplicates should be removed
        testimport.insert_row(rows)
        result = testimport.device_exists(_device.idx_device)
        self.assertTrue(result)

    def test_update_row(self):
        """Testing function update_row."""
        # Get a device to use
        _device = _create_device()

        # Create systemstat record
        row = _row(_device.idx_device)

        # Test before insertion
        result = testimport.device_exists(_device.idx_device)
        self.assertFalse(result)

        # Test after insertion
        testimport.insert_row(row)
        result = testimport.device_exists(_device.idx_device)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

        # Do an update
        idx = result.idx_systemstat
        updated_row = ISystemStat(
            idx_device=_device.idx_device,
            cpu_5min=75,
            mem_used=9000,
            mem_free=1000,
        )

        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.idx_exists(idx)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(updated_row))

    def test_update_row_with_none_values(self):
        """Testing function update_row with None values."""
        # Get a device to use
        _device = _create_device()

        # Create systemstat record
        row = _row(_device.idx_device)

        # Test after insertion
        testimport.insert_row(row)
        result = testimport.device_exists(_device.idx_device)
        self.assertTrue(result)

        # Do an update with None values
        idx = result.idx_systemstat
        updated_row = ISystemStat(
            idx_device=_device.idx_device,
            cpu_5min=None,
            mem_used=None,
            mem_free=None,
        )

        testimport.update_row(idx, updated_row)

        # Test the update - None values should be preserved
        result = testimport.idx_exists(idx)
        self.assertTrue(result)
        self.assertIsNone(result.cpu_5min)
        self.assertIsNone(result.mem_used)
        self.assertIsNone(result.mem_free)


def _create_device():
    """Create a device for testing.

    Args:
        None

    Returns:
        result: Device object

    """
    # Create a device
    row = IDevice(
        idx_zone=1,
        sys_name=data.random_string(),
        hostname=data.random_string(),
        name=data.random_string(),
        sys_description=data.random_string(),
        sys_objectid=data.random_string(),
        sys_uptime=random.randint(0, 1000000),
        last_polled=random.randint(0, 1000000),
        enabled=1,
    )

    # Insert the device
    device.insert_row(row)

    # Get and return the device
    result = device.exists(row.idx_zone, row.hostname)
    return result


def _convert(row):
    """Convert SystemStat to ISystemStat record.

    Args:
        row: SystemStat/ISystemStat record

    Returns:
        result: ISystemStat result

    """
    # Do conversion
    result = ISystemStat(
        idx_device=row.idx_device,
        cpu_5min=row.cpu_5min,
        mem_used=row.mem_used,
        mem_free=row.mem_free,
    )
    return result


def _row(idx_device):
    """Create an ISystemStat record.

    Args:
        idx_device: Device index

    Returns:
        result: ISystemStat object

    """
    # Create result
    result = ISystemStat(
        idx_device=idx_device,
        cpu_5min=50,
        mem_used=8192,
        mem_free=2048,
    )

    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
