#!/usr/bin/env python3
"""Test the mac module."""

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
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}db{0}table".format(os.sep)
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

from switchmap.db.table import mac as testimport
from switchmap.db.table import event
from switchmap.db.table import zone
from switchmap.db.table import oui
from switchmap.db.models import Mac
from switchmap.db.table import RMac
from switchmap.db.table import IMac
from switchmap.db.table import IEvent
from switchmap.db.table import IZone
from switchmap.db.table import IOui
from switchmap.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestDbTableMac(unittest.TestCase):
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
        _prerequisites()

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
        nonexistent = testimport.exists(row.mac)
        self.assertFalse(nonexistent)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        preliminary_result = testimport.exists(row.mac)
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test idx_index function
        result = testimport.idx_exists(preliminary_result.idx_mac)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.mac)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.mac)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))
        self.assertTrue(row.idx_oui != 1)

    def test_findmac(self):
        """Testing function findmac."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.findmac(row.mac)
        self.assertFalse(bool(result))

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.findmac(row.mac)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 1)
        self.assertEqual(_convert(result[0]), _convert(row))
        self.assertTrue(row.idx_oui != 1)

    def test_insert_row(self):
        """Testing function insert_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.mac)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.mac)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))
        self.assertTrue(row.idx_oui != 1)

    def test_update_row(self):
        """Testing function update_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.mac)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.mac)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))
        self.assertTrue(row.idx_oui != 1)

        # Do an update
        idx = result.idx_mac
        updated_row = Mac(
            idx_oui=row.idx_oui,
            idx_event=row.idx_event,
            idx_zone=row.idx_zone,
            mac=data.mac(),
            enabled=row.enabled,
        )
        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.exists(updated_row.mac)
        self.assertTrue(result)

        # Everything except the idx_oui should be the same.
        # The newly generated MAC address will not have an OUI entry.
        self.assertEqual(result.idx_event, updated_row.idx_event)
        self.assertEqual(result.enabled, updated_row.enabled)
        self.assertEqual(result.mac, updated_row.mac)
        self.assertEqual(result.idx_zone, updated_row.idx_zone)
        self.assertEqual(result.idx_event, updated_row.idx_event)

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert RMac to IMac record.

    Args:
        row: RMac/IMac record

    Returns:
        result: IMac result

    """
    # Do conversion
    result = IMac(
        idx_oui=row.idx_oui,
        idx_event=row.idx_event,
        idx_zone=row.idx_zone,
        mac=row.mac,
        enabled=row.enabled,
    )
    return result


def _row():
    """Create an IMac record.

    Args:
        None

    Returns:
        result: IMac object

    """
    # Initialize key variables
    mac = data.mac()

    # Create an OUI entry
    oui.insert_row(IOui(oui=mac[:6], organization=data.random_string(), enabled=1))

    # Get IDX OUI value
    idx_oui = oui.idx_oui(mac)

    # Create result
    result = IMac(idx_oui=idx_oui, idx_event=1, idx_zone=1, mac=mac, enabled=1)

    return result


def _prerequisites():
    """Create prerequisite rows.

    Args:
        None

    Returns:
        mac: MAC address for testing

    """
    # Create database entries
    event.insert_row(IEvent(name=data.random_string(), enabled=1))
    zone.insert_row(
        IZone(
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
            enabled=1,
        )
    )
    oui.insert_row(IOui(oui=None, organization=None, enabled=1))


if __name__ == "__main__":

    # Do the unit test
    unittest.main()
