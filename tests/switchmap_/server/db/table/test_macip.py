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
from switchmap.server.db.table import IIp
from switchmap.server.db.table import IMac
from switchmap.server.db.table import ip
from switchmap.server.db.table import mac
from switchmap.server.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestDbTableMacIp(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    loops = 20

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

        # Loop a lot of times
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            nonexistent = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertFalse(nonexistent)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            preliminary_result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertTrue(preliminary_result)
            self.assertEqual(_convert(preliminary_result), _convert(row))

            # Test idx_index function
            result = testimport.idx_exists(preliminary_result.idx_macip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Loop a lot of times
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

    def test_insert_row(self):
        """Testing function insert_row."""
        # Loop a lot of times
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Loop a lot of times
        for _ in range(self.loops):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(row.idx_mac, row.idx_ip)
            self.assertTrue(result)
            self.assertEqual(_convert(result), _convert(row))

            # Do an update
            idx = result.idx_macip
            updated_row = MacIp(
                idx_ip=row.idx_ip,
                idx_mac=row.idx_mac,
                enabled=row.enabled,
            )
            testimport.update_row(idx, updated_row)

            # Test the update
            result = testimport.exists(updated_row.idx_ip, updated_row.idx_mac)
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
        idx_ip=row.idx_ip,
        idx_mac=row.idx_mac,
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
    idx_zone = 1

    while True:
        # Get an IP address
        item = data.ip_()

        # Create IP
        ip_result = IIp(
            idx_zone=idx_zone,
            address=item.address,
            version=item.version,
            hostname=data.random_string(),
            enabled=1,
        )
        ip_found = ip.exists(idx_zone, item.address)
        if bool(ip_found) is False:
            ip.insert_row(ip_result)
            ip_found = ip.exists(idx_zone, item.address)

        if bool(ip_found) is True:
            break

    while True:
        mac_address = data.mac()

        # Create Mac
        mac_result = IMac(
            idx_oui=1,
            idx_zone=idx_zone,
            mac=mac_address,
            enabled=1,
        )
        mac_found = mac.exists(idx_zone, mac_address)
        if bool(mac_found) is False:
            mac.insert_row(mac_result)
            mac_found = mac.exists(idx_zone, mac_address)

        if bool(mac_found) is True:
            break

    # Insert mac
    result = IMacIp(
        idx_ip=ip_found.idx_ip, idx_mac=mac_found.idx_mac, enabled=1
    )
    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
