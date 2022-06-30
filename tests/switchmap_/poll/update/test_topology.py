#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest
from copy import deepcopy
from pprint import pprint

from sqlalchemy import select

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '''{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}update\
'''.format(os.sep)
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

from switchmap.poll.update import topology as testimport
from switchmap.poll.update import device
from switchmap.db import db
from switchmap.db import models
from switchmap.db.models import MacPort
from switchmap.db.table import event
from switchmap.db.table import zone
from switchmap.db.table import IEvent
from switchmap.db.table import IZone
from switchmap.db.table import RMacPort

from tests.testlib_ import db as dblib
from tests.testlib_ import data as datalib


def _prerequisites():
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


def _insert_row():
    """Insert new Event record.

    Args:
        None

    Returns:
        result: REvent object

    """
    # Initialize key variables
    name = datalib.random_string()

    # Insert zone
    zone.insert_row(
        IZone(
            name=datalib.random_string(),
            company_name=datalib.random_string(),
            address_0=datalib.random_string(),
            address_1=datalib.random_string(),
            address_2=datalib.random_string(),
            city=datalib.random_string(),
            state=datalib.random_string(),
            country=datalib.random_string(),
            postal_code=datalib.random_string(),
            phone=datalib.random_string(),
            notes=datalib.random_string(),
            enabled=1
        )
    )

    # Insert event
    event.insert_row(
        IEvent(
            name=name,
            enabled=1
        )
    )

    # Get event data
    result = event.exists(name)
    return result


def _reset_db():
    """Reset the database.

    Args:
        None

    Returns:
        None

    """
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


class TestPollUpdateTopology(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Reset the database
    _reset_db()

    # Create event record
    _event = _insert_row()
    idx_event = _event.idx_event

    # Process the device
    _device = device.Device(_prerequisites())
    data = _device.process()

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Reset the database
        # _reset_db()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = dblib.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_process(self):
        """Testing function process."""
        pass

    def test_device(self):
        """Testing function device."""
        pass

    def test_l1interface(self):
        """Testing function l1interface."""
        pass

    def test_vlan(self):
        """Testing function vlan."""
        pass

    def test_mac(self):
        """Testing function mac."""
        pass

    def test_macport(self):
        """Testing function macport."""
        # Initialize key variables
        result = []

        # Reset the database
        _reset_db()

        # pprint(self.data)
        print('\n\n\n\n{}\n\n\n\n'.format(self.idx_event))

        # Process all the pre-requisite events
        testimport.device(self.data, self.idx_event)
        testimport.l1interface(self.data)
        testimport.vlan(self.data)
        testimport.mac(self.data, self.idx_event)
        testimport.macip(self.data)
        testimport.macport(self.data)

        # Verify macport data
        statement = select(MacPort)
        rows = db.db_select_row(1176, statement)

        # Return
        for row in rows:
            result.append(
                RMacPort(
                    idx_macport=row.idx_macport,
                    idx_l1interface=row.idx_l1interface,
                    idx_mac=row.idx_mac,
                    enabled=row.enabled,
                    ts_created=row.ts_created,
                    ts_modified=row.ts_modified
                )
            )
        print(result)

    def test_macip(self):
        """Testing function macip."""
        pass

    def test__process_macip(self):
        """Testing function _process_macip."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
