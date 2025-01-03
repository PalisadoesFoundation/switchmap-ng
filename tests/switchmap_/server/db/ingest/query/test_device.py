#!/usr/bin/env python3
"""Test the macport module."""

import os
import sys
import unittest

from sqlalchemy import select

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
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}ingest{0}query""".format(
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

from switchmap.server.db.table import device
from switchmap.server.db.table import l1interface
from switchmap.server.db.models import MacPort
from switchmap.server.db import models
from switchmap.server.db import db as realdb

from tests.testlib_ import db

from switchmap.server.db.ingest.query import device as testimport
from switchmap.server.db.ingest.query import mac as macdetail


class TestDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
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
    def tearDownClass(cls):
        """Execute these steps after each tests is completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_device(self):
        """Testing function device."""
        # Initialize key variables
        device_ = device.idx_exists(1)

        # Test
        expected = device.exists(device_.idx_zone, device_.hostname)
        meta = testimport.Device(device_.idx_zone, device_.hostname)
        result = meta.device()
        self.assertEqual(result, expected)

    def test_interfaces(self):
        """Testing function interfaces."""
        # Initialize key variables
        device_ = device.idx_exists(1)

        # Test
        meta = testimport.Device(device_.idx_zone, device_.hostname)
        results = meta.interfaces()

        for key in range(db.TEST_MAXIMUM):
            # Initialize loop variables
            macresult = []
            idx_macs = []

            # Test interface
            idx_l1interface = key + 1
            expected_interface = l1interface.idx_exists(idx_l1interface)
            self.assertEqual(results[key].RL1Interface, expected_interface)

            # Get the MAC idx_mac values associated with the interface.
            statement = select(MacPort).where(
                MacPort.idx_l1interface == idx_l1interface,
            )
            rows = realdb.db_select_row(1197, statement)
            for row in rows:
                idx_macs.append(row.idx_mac)

            # Get the MacDetail values
            for item in idx_macs:
                macresult.extend(macdetail.by_idx_mac(item))

            # Test macs
            self.assertEqual(results[key].MacDetails, macresult)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
