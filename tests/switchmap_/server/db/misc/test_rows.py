import unittest
import os
import sys
from unittest import mock
from switchmap.server.db.misc import rows
from switchmap.server.db.table import RMacPort, RL1Interface, RDevice, RMac
from switchmap.server.db.table import RMacIp, RIp, ROui, RVlan, RVlanPort
from switchmap.server.db.table import RIpPort, RZone, REvent, RRoot

#!/usr/bin/env python3
"""Test the rows module."""


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}misc".format(os.sep)
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

# Import the module being tested


class TestRows(unittest.TestCase):
    """Checks all rows functions."""

    # Required
    maxDiff = None

    def test_device(self):
        """Testing function device."""
        # Create mock row
        row = mock.Mock()
        row.idx_device = 123
        row.idx_zone = 456
        row.sys_name = b'system123'
        row.hostname = b'host123'
        row.name = b'name123'
        row.sys_description = b'description123'
        row.sys_objectid = b'objectid123'
        row.sys_uptime = 789
        row.last_polled = 1000
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.device(row)
        self.assertIsInstance(result, RDevice)
        self.assertEqual(result.idx_device, 123)
        self.assertEqual(result.idx_zone, 456)
        self.assertEqual(result.sys_name, 'system123')
        self.assertEqual(result.hostname, 'host123')
        self.assertEqual(result.name, 'name123')
        self.assertEqual(result.sys_description, 'description123')
        self.assertEqual(result.sys_objectid, 'objectid123')
        self.assertEqual(result.sys_uptime, 789)
        self.assertEqual(result.last_polled, 1000)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with None/False values
        row.sys_name = False
        row.hostname = False
        row.name = False
        row.sys_description = False
        row.sys_objectid = False
        row.enabled = False

        result = rows.device(row)
        self.assertIsInstance(result, RDevice)
        self.assertEqual(result.sys_name, None)
        self.assertEqual(result.hostname, None)
        self.assertEqual(result.name, None)
        self.assertEqual(result.sys_description, None)
        self.assertEqual(result.sys_objectid, None)
        self.assertEqual(result.enabled, 0)

    def test_root(self):
        """Testing function root."""
        # Create mock row
        row = mock.Mock()
        row.idx_root = 123
        row.idx_event = 456
        row.name = b'root123'
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.root(row)
        self.assertIsInstance(result, RRoot)
        self.assertEqual(result.idx_root, 123)
        self.assertEqual(result.idx_event, 456)
        self.assertEqual(result.name, 'root123')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.enabled = False

        result = rows.root(row)
        self.assertEqual(result.enabled, 0)

    def test_event(self):
        """Testing function event."""
        # Create mock row
        row = mock.Mock()
        row.idx_event = 123
        row.name = b'event123'
        row.epoch_utc = 456
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.event(row)
        self.assertIsInstance(result, REvent)
        self.assertEqual(result.idx_event, 123)
        self.assertEqual(result.name, 'event123')
        self.assertEqual(result.epoch_utc, 456)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.enabled = False

        result = rows.event(row)
        self.assertEqual(result.enabled, 0)

    def test_l1interface(self):
        """Testing function l1interface."""
        # Create mock row
        row = mock.Mock()
        row.idx_l1interface = 123
        row.idx_device = 456
        row.ifindex = 789
        row.duplex = 1
        row.ethernet = 2
        row.nativevlan = 3
        row.trunk = 4
        row.iftype = 5
        row.ifspeed = 6
        row.ifalias = b'alias123'
        row.ifname = b'name123'
        row.ifdescr = b'descr123'
        row.ifadminstatus = 7
        row.ifoperstatus = 8
        row.ts_idle = 9
        row.cdpcachedeviceid = b'cdpdevice123'
        row.cdpcachedeviceport = b'cdpport123'
        row.cdpcacheplatform = b'cdpplatform123'
        row.lldpremportdesc = b'lldpportdesc123'
        row.lldpremsyscapenabled = b'lldpsyscap123'
        row.lldpremsysdesc = b'lldpsysdesc123'
        row.lldpremsysname = b'lldpsysname123'
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.l1interface(row)
        self.assertIsInstance(result, RL1Interface)
        self.assertEqual(result.idx_l1interface, 123)
        self.assertEqual(result.idx_device, 456)
        self.assertEqual(result.ifindex, 789)
        self.assertEqual(result.duplex, 1)
        self.assertEqual(result.ethernet, 2)
        self.assertEqual(result.nativevlan, 3)
        self.assertEqual(result.trunk, 4)
        self.assertEqual(result.iftype, 5)
        self.assertEqual(result.ifspeed, 6)
        self.assertEqual(result.ifalias, 'alias123')
        self.assertEqual(result.ifname, 'name123')
        self.assertEqual(result.ifdescr, 'descr123')
        self.assertEqual(result.ifadminstatus, 7)
        self.assertEqual(result.ifoperstatus, 8)
        self.assertEqual(result.ts_idle, 9)
        self.assertEqual(result.cdpcachedeviceid, 'cdpdevice123')
        self.assertEqual(result.cdpcachedeviceport, 'cdpport123')
        self.assertEqual(result.cdpcacheplatform, 'cdpplatform123')
        self.assertEqual(result.lldpremportdesc, 'lldpportdesc123')
        self.assertEqual(result.lldpremsyscapenabled, 'lldpsyscap123')
        self.assertEqual(result.lldpremsysdesc, 'lldpsysdesc123')
        self.assertEqual(result.lldpremsysname, 'lldpsysname123')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with None/False values
        row.ifalias = None
        row.ifname = None
        row.ifdescr = None
        row.cdpcachedeviceid = None
        row.cdpcachedeviceport = None
        row.cdpcacheplatform = None
        row.lldpremportdesc = None
        row.lldpremsyscapenabled = None
        row.lldpremsysdesc = None
        row.lldpremsysname = None
        row.enabled = False

        result = rows.l1interface(row)
        self.assertEqual(result.ifalias, None)
        self.assertEqual(result.ifname, None)
        self.assertEqual(result.ifdescr, None)
        self.assertEqual(result.cdpcachedeviceid, None)
        self.assertEqual(result.cdpcachedeviceport, None)
        self.assertEqual(result.cdpcacheplatform, None)
        self.assertEqual(result.lldpremportdesc, None)
        self.assertEqual(result.lldpremsyscapenabled, None)
        self.assertEqual(result.lldpremsysdesc, None)
        self.assertEqual(result.lldpremsysname, None)
        self.assertEqual(result.enabled, 0)

    def test_mac(self):
        """Testing function mac."""
        # Create mock row
        row = mock.Mock()
        row.idx_mac = 123
        row.idx_oui = 456
        row.idx_zone = 789
        row.mac = b'mac123'
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.mac(row)
        self.assertIsInstance(result, RMac)
        self.assertEqual(result.idx_mac, 123)
        self.assertEqual(result.idx_oui, 456)
        self.assertEqual(result.idx_zone, 789)
        self.assertEqual(result.mac, 'mac123')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.mac = False
        row.enabled = False

        result = rows.mac(row)
        self.assertEqual(result.mac, None)
        self.assertEqual(result.enabled, 0)

    def test_macip(self):
        """Testing function macip."""
        # Create mock row
        row = mock.Mock()
        row.idx_macip = 123
        row.idx_ip = 456
        row.idx_mac = 789
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.macip(row)
        self.assertIsInstance(result, RMacIp)
        self.assertEqual(result.idx_macip, 123)
        self.assertEqual(result.idx_ip, 456)
        self.assertEqual(result.idx_mac, 789)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.enabled = False

        result = rows.macip(row)
        self.assertEqual(result.enabled, 0)

    def test_macport(self):
        """Testing function macport."""
        # Create mock row
        row = mock.Mock()
        row.idx_macport = 123
        row.idx_l1interface = 456
        row.idx_mac = 789
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.macport(row)
        self.assertIsInstance(result, RMacPort)
        self.assertEqual(result.idx_macport, 123)
        self.assertEqual(result.idx_l1interface, 456)
        self.assertEqual(result.idx_mac, 789)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.enabled = False

        result = rows.macport(row)
        self.assertEqual(result.enabled, 0)

    def test_oui(self):
        """Testing function oui."""
        # Create mock row
        row = mock.Mock()
        row.idx_oui = 123
        row.oui = b'oui123'
        row.organization = b'org123'
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.oui(row)
        self.assertIsInstance(result, ROui)
        self.assertEqual(result.idx_oui, 123)
        self.assertEqual(result.oui, 'oui123')
        self.assertEqual(result.organization, 'org123')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.oui = False
        row.organization = False
        row.enabled = False

        result = rows.oui(row)
        self.assertEqual(result.oui, None)
        self.assertEqual(result.organization, None)
        self.assertEqual(result.enabled, 0)

    def test_vlan(self):
        """Testing function vlan."""
        # Create mock row
        row = mock.Mock()
        row.idx_vlan = 123
        row.idx_device = 456
        row.vlan = 789
        row.name = b'vlan123'
        row.state = 1
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.vlan(row)
        self.assertIsInstance(result, RVlan)
        self.assertEqual(result.idx_vlan, 123)
        self.assertEqual(result.idx_device, 456)
        self.assertEqual(result.vlan, 789)
        self.assertEqual(result.name, 'vlan123')
        self.assertEqual(result.state, 1)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.name = False
        row.enabled = False

        result = rows.vlan(row)
        self.assertEqual(result.name, None)
        self.assertEqual(result.enabled, 0)

    def test_vlanport(self):
        """Testing function vlanport."""
        # Create mock row
        row = mock.Mock()
        row.idx_vlanport = 123
        row.idx_l1interface = 456
        row.idx_vlan = 789
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.vlanport(row)
        self.assertIsInstance(result, RVlanPort)
        self.assertEqual(result.idx_vlanport, 123)
        self.assertEqual(result.idx_l1interface, 456)
        self.assertEqual(result.idx_vlan, 789)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.enabled = False

        result = rows.vlanport(row)
        self.assertEqual(result.enabled, 0)

    def test_zone(self):
        """Testing function zone."""
        # Create mock row
        row = mock.Mock()
        row.idx_zone = 123
        row.idx_event = 456
        row.name = b'zone123'
        row.notes = b'notes123'
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.zone(row)
        self.assertIsInstance(result, RZone)
        self.assertEqual(result.idx_zone, 123)
        self.assertEqual(result.idx_event, 456)
        self.assertEqual(result.name, 'zone123')
        self.assertEqual(result.notes, 'notes123')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with None values
        row.name = None
        row.notes = None
        row.enabled = False

        result = rows.zone(row)
        self.assertEqual(result.name, None)
        self.assertEqual(result.notes, None)
        self.assertEqual(result.enabled, 0)

    def test_ip(self):
        """Testing function ip."""
        # Create mock row
        row = mock.Mock()
        row.idx_ip = 123
        row.idx_zone = 456
        row.address = b'192.168.1.1'
        row.hostname = b'host123'
        row.version = 4
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.ip(row)
        self.assertIsInstance(result, RIp)
        self.assertEqual(result.idx_ip, 123)
        self.assertEqual(result.idx_zone, 456)
        self.assertEqual(result.address, '192.168.1.1')
        self.assertEqual(result.hostname, 'host123')
        self.assertEqual(result.version, 4)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.address = False
        row.hostname = False
        row.enabled = False

        result = rows.ip(row)
        self.assertEqual(result.address, None)
        self.assertEqual(result.hostname, None)
        self.assertEqual(result.enabled, 0)

    def test_ipport(self):
        """Testing function ipport."""
        # Create mock row
        row = mock.Mock()
        row.idx_ipport = 123
        row.idx_l1interface = 456
        row.idx_ip = 789
        row.enabled = True
        row.ts_created = 1234567890
        row.ts_modified = 1234567891

        # Run test
        result = rows.ipport(row)
        self.assertIsInstance(result, RIpPort)
        self.assertEqual(result.idx_ipport, 123)
        self.assertEqual(result.idx_l1interface, 456)
        self.assertEqual(result.idx_ip, 789)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 1234567890)
        self.assertEqual(result.ts_modified, 1234567891)

        # Test with False values
        row.enabled = False

        result = rows.ipport(row)
        self.assertEqual(result.enabled, 0)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()