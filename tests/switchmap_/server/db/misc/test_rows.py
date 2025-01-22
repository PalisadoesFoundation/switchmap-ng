#!/usr/bin/env python3
"""Test the rows module."""

import os
import sys
import unittest
from unittest.mock import MagicMock

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

from switchmap.server.db.misc import rows as testimport


class TestRows(unittest.TestCase):
    """Checks all functions and methods."""

    def setUp(self):
        """Set up test data."""
        self.mock_row = MagicMock()

    def tearDown(self):
        """Clean up after each test."""
        del self.mock_row

    def test_device(self):
        """Testing function device."""
        # Mock a database row
        self.mock_row.idx_device = 1
        self.mock_row.idx_zone = 2
        self.mock_row.sys_name = b"sys_name"
        self.mock_row.hostname = b"hostname"
        self.mock_row.name = b"name"
        self.mock_row.sys_description = b"sys_description"
        self.mock_row.sys_objectid = b"sys_objectid"
        self.mock_row.sys_uptime = 100
        self.mock_row.last_polled = 200
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 300
        self.mock_row.ts_modified = 400

        # Call the function
        result = testimport.device(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_device, 1)
        self.assertEqual(result.idx_zone, 2)
        self.assertEqual(result.sys_name, "sys_name")
        self.assertEqual(result.hostname, "hostname")
        self.assertEqual(result.name, "name")
        self.assertEqual(result.sys_description, "sys_description")
        self.assertEqual(result.sys_objectid, "sys_objectid")
        self.assertEqual(result.sys_uptime, 100)
        self.assertEqual(result.last_polled, 200)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 300)
        self.assertEqual(result.ts_modified, 400)

    def test_device_with_none_values(self):
        """Testing function device with None values."""
        # Mock a database row with None values
        self.mock_row.idx_device = 1
        self.mock_row.idx_zone = 2
        self.mock_row.sys_name = None
        self.mock_row.hostname = None
        self.mock_row.name = None
        self.mock_row.sys_description = None
        self.mock_row.sys_objectid = None
        self.mock_row.sys_uptime = 100
        self.mock_row.last_polled = 200
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 300
        self.mock_row.ts_modified = 400

        # Call the function
        result = testimport.device(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_device, 1)
        self.assertEqual(result.idx_zone, 2)
        self.assertIsNone(result.sys_name)
        self.assertIsNone(result.hostname)
        self.assertIsNone(result.name)
        self.assertIsNone(result.sys_description)
        self.assertIsNone(result.sys_objectid)
        self.assertEqual(result.sys_uptime, 100)
        self.assertEqual(result.last_polled, 200)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 300)
        self.assertEqual(result.ts_modified, 400)

    def test_root(self):
        """Testing function root."""
        # Mock a database row
        self.mock_row.idx_root = 1
        self.mock_row.idx_event = 2
        self.mock_row.name = b"name"
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 300
        self.mock_row.ts_modified = 400

        # Call the function
        result = testimport.root(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_root, 1)
        self.assertEqual(result.idx_event, 2)
        self.assertEqual(result.name, "name")
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 300)
        self.assertEqual(result.ts_modified, 400)

    def test_event(self):
        """Testing function event."""
        # Mock a database row
        self.mock_row.idx_event = 1
        self.mock_row.name = b"name"
        self.mock_row.epoch_utc = 100
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 300
        self.mock_row.ts_modified = 400

        # Call the function
        result = testimport.event(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_event, 1)
        self.assertEqual(result.name, "name")
        self.assertEqual(result.epoch_utc, 100)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 300)
        self.assertEqual(result.ts_modified, 400)

    def test_l1interface(self):
        """Testing function l1interface."""
        # Mock a database row
        self.mock_row.idx_l1interface = 1
        self.mock_row.idx_device = 2
        self.mock_row.ifindex = 3
        self.mock_row.duplex = 4
        self.mock_row.ethernet = 5
        self.mock_row.nativevlan = 6
        self.mock_row.trunk = 7
        self.mock_row.iftype = 8
        self.mock_row.ifspeed = 9
        self.mock_row.ifalias = b"ifalias"
        self.mock_row.ifname = b"ifname"
        self.mock_row.ifdescr = b"ifdescr"
        self.mock_row.ifadminstatus = 10
        self.mock_row.ifoperstatus = 11
        self.mock_row.ts_idle = 12
        self.mock_row.cdpcachedeviceid = b"cdpcachedeviceid"
        self.mock_row.cdpcachedeviceport = b"cdpcachedeviceport"
        self.mock_row.cdpcacheplatform = b"cdpcacheplatform"
        self.mock_row.lldpremportdesc = b"lldpremportdesc"
        self.mock_row.lldpremsyscapenabled = b"lldpremsyscapenabled"
        self.mock_row.lldpremsysdesc = b"lldpremsysdesc"
        self.mock_row.lldpremsysname = b"lldpremsysname"
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 300
        self.mock_row.ts_modified = 400

        # Call the function
        result = testimport.l1interface(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_l1interface, 1)
        self.assertEqual(result.idx_device, 2)
        self.assertEqual(result.ifindex, 3)
        self.assertEqual(result.duplex, 4)
        self.assertEqual(result.ethernet, 5)
        self.assertEqual(result.nativevlan, 6)
        self.assertEqual(result.trunk, 7)
        self.assertEqual(result.iftype, 8)
        self.assertEqual(result.ifspeed, 9)
        self.assertEqual(result.ifalias, "ifalias")
        self.assertEqual(result.ifname, "ifname")
        self.assertEqual(result.ifdescr, "ifdescr")
        self.assertEqual(result.ifadminstatus, 10)
        self.assertEqual(result.ifoperstatus, 11)
        self.assertEqual(result.ts_idle, 12)
        self.assertEqual(result.cdpcachedeviceid, "cdpcachedeviceid")
        self.assertEqual(result.cdpcachedeviceport, "cdpcachedeviceport")
        self.assertEqual(result.cdpcacheplatform, "cdpcacheplatform")
        self.assertEqual(result.lldpremportdesc, "lldpremportdesc")
        self.assertEqual(result.lldpremsyscapenabled, "lldpremsyscapenabled")
        self.assertEqual(result.lldpremsysdesc, "lldpremsysdesc")
        self.assertEqual(result.lldpremsysname, "lldpremsysname")
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 300)
        self.assertEqual(result.ts_modified, 400)

    def test_mac(self):
        """Testing function mac."""
        # Mock a database row
        self.mock_row.idx_mac = 1
        self.mock_row.idx_oui = 2
        self.mock_row.idx_zone = 3
        self.mock_row.mac = b"00:11:22:33:44:55"
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.mac(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_mac, 1)
        self.assertEqual(result.idx_oui, 2)
        self.assertEqual(result.idx_zone, 3)
        self.assertEqual(result.mac, "00:11:22:33:44:55")
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_macip(self):
        """Testing function macip."""
        # Mock a database row
        self.mock_row.idx_macip = 1
        self.mock_row.idx_ip = 2
        self.mock_row.idx_mac = 3
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.macip(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_macip, 1)
        self.assertEqual(result.idx_ip, 2)
        self.assertEqual(result.idx_mac, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_macport(self):
        """Testing function macport."""
        # Mock a database row
        self.mock_row.idx_macport = 1
        self.mock_row.idx_l1interface = 2
        self.mock_row.idx_mac = 3
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.macport(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_macport, 1)
        self.assertEqual(result.idx_l1interface, 2)
        self.assertEqual(result.idx_mac, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_oui(self):
        """Testing function oui."""
        # Mock a database row
        self.mock_row.idx_oui = 1
        self.mock_row.oui = b"00:11:22"
        self.mock_row.organization = b"Test Organization"
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.oui(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_oui, 1)
        self.assertEqual(result.oui, "00:11:22")
        self.assertEqual(result.organization, "Test Organization")
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_vlan(self):
        """Testing function vlan."""
        # Mock a database row
        self.mock_row.idx_vlan = 1
        self.mock_row.idx_device = 2
        self.mock_row.vlan = 10
        self.mock_row.name = b"VLAN10"
        self.mock_row.state = 1
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.vlan(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_vlan, 1)
        self.assertEqual(result.idx_device, 2)
        self.assertEqual(result.vlan, 10)
        self.assertEqual(result.name, "VLAN10")
        self.assertEqual(result.state, 1)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_vlanport(self):
        """Testing function vlanport."""
        # Mock a database row
        self.mock_row.idx_vlanport = 1
        self.mock_row.idx_l1interface = 2
        self.mock_row.idx_vlan = 3
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.vlanport(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_vlanport, 1)
        self.assertEqual(result.idx_l1interface, 2)
        self.assertEqual(result.idx_vlan, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_zone(self):
        """Testing function zone."""
        # Mock a database row
        self.mock_row.idx_zone = 1
        self.mock_row.idx_event = 2
        self.mock_row.name = b"Zone1"
        self.mock_row.notes = b"Test Zone"
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.zone(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_zone, 1)
        self.assertEqual(result.idx_event, 2)
        self.assertEqual(result.name, "Zone1")
        self.assertEqual(result.notes, "Test Zone")
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_ip(self):
        """Testing function ip."""
        # Mock a database row
        self.mock_row.idx_ip = 1
        self.mock_row.idx_zone = 2
        self.mock_row.address = b"192.168.1.1"
        self.mock_row.hostname = b"hostname.example.com"
        self.mock_row.version = 4
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.ip(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_ip, 1)
        self.assertEqual(result.idx_zone, 2)
        self.assertEqual(result.address, "192.168.1.1")
        self.assertEqual(result.hostname, "hostname.example.com")
        self.assertEqual(result.version, 4)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)

    def test_ipport(self):
        """Testing function ipport."""
        # Mock a database row
        self.mock_row.idx_ipport = 1
        self.mock_row.idx_l1interface = 2
        self.mock_row.idx_ip = 3
        self.mock_row.enabled = 1
        self.mock_row.ts_created = 100
        self.mock_row.ts_modified = 200

        # Call the function
        result = testimport.ipport(self.mock_row)

        # Assertions
        self.assertEqual(result.idx_ipport, 1)
        self.assertEqual(result.idx_l1interface, 2)
        self.assertEqual(result.idx_ip, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 100)
        self.assertEqual(result.ts_modified, 200)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
