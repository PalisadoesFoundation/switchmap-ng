#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest
from copy import deepcopy


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
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}ingest""".format(
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


# Create the necessary configuration
from tests.testlib_ import setup
from tests.testlib_ import data

CONFIG = setup.config()
CONFIG.save()

from switchmap.poller.update import device
from switchmap.server.db.ingest.update import device as device_update
from switchmap.server.db.ingest.update import zone as zone_update
from switchmap.server.db.ingest import update as testimport
from switchmap.server.db.ingest import ingest
from switchmap.server.db.table import zone
from switchmap.server.db.table import oui
from switchmap.server.db.table import event
from switchmap.server.db import db
from switchmap.server.db import models
from switchmap.server.db.models import IpPort
from switchmap.server.db.table import RIpPort
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IOui

from tests.testlib_ import db as dblib
from tests.testlib_ import data as datalib


def _polled_data():
    """Create prerequisite data.

    Strip out all l1_ keys from the data

    Args:
        None

    Returns:
        result: Stripped data

    """
    # Get data
    result = deepcopy(datalib.polled_data())
    return result


def _reset_db():
    """Reset the database.

    Args:
        None

    Returns:
        result: List of

    """
    # Initialize key variables
    idx_zone = 1

    # Load the configuration in case it's been deleted after loading the
    # configuration above. Sometimes this happens when running
    # `python3 -m unittest discover` where another the tearDownClass of
    # another test module prematurely deletes the configuration required
    # for this module
    config = setup.config()
    config.save()

    # Drop tables
    database = dblib.Database()
    database.drop()

    # Create database tables
    models.create_all_tables()

    # Create a zone
    event_name = data.random_string()
    row = event.create(name=event_name)
    zone.insert_row(
        IZone(
            idx_event=row.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
    )

    # Create an OUI entry
    oui.insert_row(IOui(oui="testing", organization="testing", enabled=1))

    # Process the device
    _device = device.Device(_polled_data())
    device_data = _device.process()

    # Update the Zone ARP table
    _zone = zone_update.Topology(device_data, idx_zone)
    result = ingest.insert_arptable(_zone.process(dns=False))
    return result


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    idx_zone = 1
    max_loops = 10

    @classmethod
    def setUp(cls):
        """Execute these steps before starting tests."""
        # Reset the database
        cls.pairmacips = _reset_db()

    @classmethod
    def tearDown(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = dblib.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_ipport(self):
        """Testing function ipport."""
        # Initialize key variables
        return
        result = []
        expected = []

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Make sure the device exists
        exists = device_update.device(self.idx_zone, data)

        # Test transaction
        setup = device_update.Topology(exists, data, dns=False)
        setup.l1interface(test=True)
        setup.vlan(test=True)
        setup.vlanport(test=True)
        setup.macport(test=True)

        # Verify macport data
        statement = select(IpPort)
        rows = db.db_select_row(1074, statement)

        # Return
        for row in rows:
            result.append(
                RIpPort(
                    idx_ipport=row.idx_ipport,
                    idx_l1interface=row.idx_l1interface,
                    idx_ip=row.idx_ip,
                    enabled=1,
                    ts_created=None,
                    ts_modified=None,
                )
            )

        result.sort(key=lambda x: (x.idx_ipport))

        self.assertEqual(result[: self.max_loops * 3], expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
