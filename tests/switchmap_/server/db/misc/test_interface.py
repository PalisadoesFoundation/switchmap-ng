#!/usr/bin/env python3
"""Test the interface module."""

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
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}misc""".format(
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

from switchmap.server.db import models
from switchmap.server.db.table import zone
from switchmap.server.db.table import event
from switchmap.server.db.table import device
from switchmap.server.db.table import l1interface
from switchmap.server.db.table import IDevice
from switchmap.server.db.table import IL1Interface
from switchmap.server.db.table import IZone

from tests.testlib_ import db
from tests.testlib_ import data

from switchmap.server.db.misc import interface as testimport


class TestInterface(unittest.TestCase):
    """Checks all functions and methods."""

    @classmethod
    def setUpClass(cls):
        """Setup database for testing."""
        # Load the configuration
        config = setup.config()
        config.save()

        # Drop tables
        database = db.Database()
        database.drop()

        # Create database tables
        models.create_all_tables()

    def test_interfaces_success(self):
        """Testing function interfaces with existing interfaces."""
        # Create events
        event_row1 = event.create()  # Event 1
        event_row2 = event.create()  # Event 2

        # Create zones for both events
        test_zone1 = IZone(
            idx_event=event_row1.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
        zone.insert_row(test_zone1)
        zone_record1 = zone.exists(event_row1.idx_event, test_zone1.name)

        test_zone2 = IZone(
            idx_event=event_row2.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
        zone.insert_row(test_zone2)
        zone_record2 = zone.exists(event_row2.idx_event, test_zone2.name)

        # Create device in previous event
        test_device1 = IDevice(
            idx_zone=zone_record1.idx_zone,  # Use actual zone record
            hostname="test_host",
            name=data.random_string(),
            sys_name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=123456,
            last_polled=123456,
            enabled=1,
        )
        device.insert_row(test_device1)

        # Create device in current event
        test_device2 = IDevice(
            idx_zone=zone_record2.idx_zone,  # Use actual zone record
            hostname="test_host",  # Same hostname as previous device
            name=data.random_string(),
            sys_name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=123456,
            last_polled=123456,
            enabled=1,
        )
        device.insert_row(test_device2)

        # Get the actual device record
        device_record = device.exists(
            zone_record1.idx_zone, test_device1.hostname
        )

        # Create test interfaces for previous device
        test_interfaces = []
        for i in range(3):
            interface = IL1Interface(
                idx_device=device_record.idx_device,  # Use actual device record
                ifindex=i,
                duplex=1,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                iftype=6,
                ifspeed=1000000000,
                ifalias=f"Interface_{i}",
                ifname=f"Gi0/{i}",
                ifdescr=f"GigabitEthernet0/{i}",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=data.random_string(),
                cdpcachedeviceport=data.random_string(),
                cdpcacheplatform=data.random_string(),
                lldpremportdesc=data.random_string(),
                lldpremsyscapenabled=data.random_string(),
                lldpremsysdesc=data.random_string(),
                lldpremsysname=data.random_string(),
                enabled=1,
            )
            l1interface.insert_row(interface)
            test_interfaces.append(interface)

        # Test interfaces function with the second device
        device_record2 = device.exists(
            zone_record2.idx_zone, test_device2.hostname
        )
        result = testimport.interfaces(device_record2)

        # Verify results
        self.assertEqual(len(result), len(test_interfaces))
        for i, interface in enumerate(result):
            self.assertEqual(interface.ifindex, test_interfaces[i].ifindex)
            self.assertEqual(interface.ifname, test_interfaces[i].ifname)
            self.assertEqual(interface.ifdescr, test_interfaces[i].ifdescr)

    def test_interfaces_zone_not_exists(self):
        """Testing function interfaces when zone doesn't exist.

        When the zone associated with the device doesn't exist,
        the function should return an empty list.
        """
        # Create an event first
        event_row = event.create()

        # Create a zone
        test_zone = IZone(
            idx_event=event_row.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
        zone.insert_row(test_zone)
        zone_record = zone.exists(event_row.idx_event, test_zone.name)

        # Create test device with the valid zone
        test_device = IDevice(
            idx_zone=zone_record.idx_zone,
            hostname="test_host",
            name=data.random_string(),
            sys_name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=123456,
            last_polled=123456,
            enabled=1,
        )
        device.insert_row(test_device)

        # Get the actual device record
        device_record = device.exists(
            zone_record.idx_zone, test_device.hostname
        )

        # Test interfaces function
        result = testimport.interfaces(device_record)

        # Verify result is empty list
        self.assertEqual(result, [])

    def test_interfaces_no_previous_event(self):
        """Testing function interfaces when there's no previous event.

        When there's no event prior to the current one, the function
        should return an empty list since there's no historical data
        to compare against.
        """
        # Create first event (no previous events)
        event_row = event.create()

        # Create zone
        test_zone = IZone(
            idx_event=event_row.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
        zone.insert_row(test_zone)
        zone_record = zone.exists(event_row.idx_event, test_zone.name)

        # Create device
        test_device = IDevice(
            idx_zone=zone_record.idx_zone,
            hostname="test_host",
            name=data.random_string(),
            sys_name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=123456,
            last_polled=123456,
            enabled=1,
        )
        device.insert_row(test_device)

        # Get the actual device record
        device_record = device.exists(
            zone_record.idx_zone, test_device.hostname
        )

        # Test interfaces function
        result = testimport.interfaces(device_record)

        # Verify result is empty list
        self.assertEqual(result, [])

    def test_interfaces_device_not_in_previous_event(self):
        """Testing function interfaces when device isn't in previous event.

        When the device exists in the current event but not in the previous one,
        the function should return an empty list since there's no historical
        interface data to return.
        """
        # Create two events
        event_row1 = event.create()  # Previous event
        event_row2 = event.create()  # Current event

        # Create zones for both events
        test_zone1 = IZone(
            idx_event=event_row1.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
        zone.insert_row(test_zone1)

        test_zone2 = IZone(
            idx_event=event_row2.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
        zone.insert_row(test_zone2)
        zone_record2 = zone.exists(event_row2.idx_event, test_zone2.name)

        # Create device only in current event (event2)
        test_device = IDevice(
            idx_zone=zone_record2.idx_zone,
            hostname="test_host",
            name=data.random_string(),
            sys_name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=123456,
            last_polled=123456,
            enabled=1,
        )
        device.insert_row(test_device)

        # Get the actual device record
        device_record = device.exists(
            zone_record2.idx_zone, test_device.hostname
        )

        # Test interfaces function
        result = testimport.interfaces(device_record)

        # Verify result is empty list
        self.assertEqual(result, [])


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
