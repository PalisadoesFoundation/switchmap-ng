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
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.server.db import models
from switchmap.server.db.table import (
    root as root_table,
)
from switchmap.server.db.misc import rows
from switchmap.server.db.table import zone
from switchmap.server.db.table import event
from switchmap.server.db.table import device
from switchmap.server.db.table import l1interface
from switchmap.server.db.table import IDevice
from switchmap.server.db.table import IL1Interface
from switchmap.server.db.table import IZone
from switchmap.server.db.table import mac
from switchmap.server.db.table import IMac
from switchmap.server.db.table import IRoot
from switchmap.server.db.table import macip
from switchmap.server.db.table import IMacIp
from switchmap.server.db.table import ip as ip_table
from switchmap.server.db.table import IOui
from switchmap.server.db.table import oui
from tests.testlib_ import db
from tests.testlib_ import data

from switchmap.server.db.misc import rows as testimport
from switchmap.server.db import scoped_session


class TestRows(unittest.TestCase):
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

    def test_device(self):
        """Test rows.device()."""
        # Create parent records
        event_row = event.create()

        # Insert zone and retrieve it
        zone_name = data.random_string()
        zone.insert_row(
            IZone(
                idx_event=event_row.idx_event,
                name=zone_name,
                notes=data.random_string(),
                enabled=1,
            )
        )
        zone_record = zone.exists(event_row.idx_event, zone_name)

        # Create device
        test_data = IDevice(
            idx_zone=zone_record.idx_zone,
            hostname=b"test_host",
            name=data.random_string(),
            sys_name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=1000,
            last_polled=2000,
            enabled=1,
        )
        device.insert_row(test_data)
        device_record = device.exists(zone_record.idx_zone, "test_host")

        # Test conversion
        result = rows.device(device_record)
        self.assertEqual(result.idx_device, device_record.idx_device)
        self.assertEqual(result.hostname, "test_host")

    def test_root(self):
        """Test rows.root()."""
        event_row = event.create()
        root_name = data.random_string()
        root_table.insert_row(
            IRoot(
                idx_event=event_row.idx_event,
                name=root_name,
                enabled=1,
            )
        )
        root_record = root_table.exists(event_row.idx_event, root_name)
        result = rows.root(root_record)
        self.assertEqual(result.idx_root, root_record.idx_root)

    def test_event(self):
        """Test rows.event()."""
        # Create event using table function
        event_row = event.create()
        result = rows.event(event_row)
        self.assertEqual(result.idx_event, event_row.idx_event)
        self.assertEqual(result.name, event_row.name)

    def test_l1interface(self):
        """Test rows.l1interface()."""
        event_row = event.create()

        # Insert zone
        zone_name = data.random_string()
        zone.insert_row(
            IZone(
                idx_event=event_row.idx_event,
                name=zone_name,
                notes=data.random_string(),
                enabled=1,
            )
        )
        zone_record = zone.exists(event_row.idx_event, zone_name)

        # Insert device
        device.insert_row(
            IDevice(
                idx_zone=zone_record.idx_zone,
                hostname=b"test",
                name=data.random_string(),
                sys_name=data.random_string(),
                sys_description=data.random_string(),
                sys_objectid=data.random_string(),
                sys_uptime=0,
                last_polled=0,
                enabled=1,
            )
        )
        device_record = device.exists(zone_record.idx_zone, "test")

        # Create interface
        if_row = l1interface.insert_row(
            IL1Interface(
                idx_device=device_record.idx_device,
                ifindex=1,
                duplex=1,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                iftype=6,
                ifspeed=1000,
                ifalias=b"Test Alias",
                ifname=b"eth0",
                ifdescr=b"Ethernet0",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                enabled=1,
            )
        )
        result = rows.l1interface(if_row)
        self.assertEqual(result.ifname, "eth0")

    def test_mac(self):
        """Test rows.mac()."""
        event_row = event.create()

        # Insert zone
        zone_name = data.random_string()
        zone.insert_row(
            IZone(
                idx_event=event_row.idx_event,
                name=zone_name,
                notes=data.random_string(),
                enabled=1,
            )
        )
        zone_record = zone.exists(event_row.idx_event, zone_name)

        # Insert OUI
        oui_value = "00:11:22"
        oui.insert_row(
            IOui(
                oui=oui_value,
                organization=data.random_string(),
                enabled=1,
            )
        )
        oui_record = oui.exists(oui_value)

        # Insert MAC
        mac_row = mac.insert_row(
            IMac(
                idx_oui=oui_record.idx_oui,
                idx_zone=zone_record.idx_zone,
                mac=b"00:11:22:33:44:55",
                enabled=1,
            )
        )
        result = rows.mac(mac_row)
        self.assertEqual(result.mac, "00:11:22:33:44:55")

    def test_macip(self):
        """Test rows.macip()."""
        event_row = event.create()

        # Insert zone
        zone_name = data.random_string()
        zone.insert_row(
            IZone(
                idx_event=event_row.idx_event,
                name=zone_name,
                notes=data.random_string(),
                enabled=1,
            )
        )
        zone_record = zone.exists(event_row.idx_event, zone_name)

        # Insert MAC
        mac_row = mac.insert_row(
            IMac(
                idx_zone=zone_record.idx_zone,
                mac=b"00:11:22:33:44:55",
                enabled=1,
            )
        )

        # Insert IP
        ip_row = ip_table.insert_row(
            ip_table.IIp(
                idx_zone=zone_record.idx_zone,
                address=b"192.168.1.1",
                version=4,
                enabled=1,
            )
        )

        # Insert MAC IP
        macip_row = macip.insert_row(
            IMacIp(
                idx_mac=mac_row.idx_mac,
                idx_ip=ip_row.idx_ip,
                enabled=1,
            )
        )
        result = rows.macip(macip_row)
        self.assertEqual(result.idx_mac, mac_row.idx_mac)


if __name__ == "__main__":
    unittest.main()
