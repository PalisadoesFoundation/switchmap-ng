#!/usr/bin/env python3
"""Test the rows module."""

import os
import sys
import unittest
from collections import namedtuple

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
from switchmap.server.db.table import RMacPort, RL1Interface, RDevice
from switchmap.server.db.table import RMac, RMacIp, RIp, ROui
from switchmap.server.db.table import RVlan, RVlanPort, RIpPort, RZone
from switchmap.server.db.table import REvent, RRoot

from tests.testlib_ import db
from tests.testlib_ import data

# Import the module to test
from switchmap.server.db.misc import rows as testimport


class TestRow(unittest.TestCase):
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

        database = db.Database()
        database.drop()

        models.create_all_tables()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps after each tests is completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_device(self):
        """Testing function device."""
        # Create a mock device row
        MockRow = namedtuple(
            'MockRow',
            ['idx_device', 'idx_zone', 'sys_name', 'hostname', 'name', 
             'sys_description', 'sys_objectid', 'sys_uptime', 'last_polled',
             'enabled', 'ts_created', 'ts_modified']
        )
        
        # Test with values present
        mock_row = MockRow(
            idx_device=1,
            idx_zone=2,
            sys_name='test_sys_name'.encode(),
            hostname='test_hostname'.encode(),
            name='test_name'.encode(),
            sys_description='test_description'.encode(),
            sys_objectid='1.3.6.1.4.1.9.1.1'.encode(),
            sys_uptime=12345,
            last_polled=54321,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.device(mock_row)
        
        # Check that result is the correct type
        self.assertIsInstance(result, RDevice)
        
        # Check all values
        self.assertEqual(result.idx_device, 1)
        self.assertEqual(result.idx_zone, 2)
        self.assertEqual(result.sys_name, 'test_sys_name')
        self.assertEqual(result.hostname, 'test_hostname')
        self.assertEqual(result.name, 'test_name')
        self.assertEqual(result.sys_description, 'test_description')
        self.assertEqual(result.sys_objectid, '1.3.6.1.4.1.9.1.1')
        self.assertEqual(result.sys_uptime, 12345)
        self.assertEqual(result.last_polled, 54321)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)
        
        # Test with None values
        mock_row = MockRow(
            idx_device=1,
            idx_zone=2,
            sys_name=None,
            hostname=None,
            name=None,
            sys_description=None,
            sys_objectid=None,
            sys_uptime=12345,
            last_polled=54321,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.device(mock_row)
        
        # Check that result is the correct type
        self.assertIsInstance(result, RDevice)
        
        # Check None values are handled correctly
        self.assertEqual(result.sys_name, None)
        self.assertEqual(result.hostname, None)
        self.assertEqual(result.name, None)
        self.assertEqual(result.sys_description, None)
        self.assertEqual(result.sys_objectid, None)
        self.assertEqual(result.enabled, 0)

    def test_root(self):
        """Testing function root."""
        # Create a mock root row
        MockRow = namedtuple(
            'MockRow',
            ['idx_root', 'idx_event', 'name', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_root=1,
            idx_event=2,
            name='test_root'.encode(),
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.root(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RRoot)
        
        # Check values
        self.assertEqual(result.idx_root, 1)
        self.assertEqual(result.idx_event, 2)
        self.assertEqual(result.name, 'test_root')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)

    def test_event(self):
        """Testing function event."""
        # Create a mock event row
        MockRow = namedtuple(
            'MockRow',
            ['idx_event', 'name', 'epoch_utc', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_event=1,
            name='test_event'.encode(),
            epoch_utc=12345678,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.event(mock_row)
        
        # Check result type
        self.assertIsInstance(result, REvent)
        
        # Check values
        self.assertEqual(result.idx_event, 1)
        self.assertEqual(result.name, 'test_event')
        self.assertEqual(result.epoch_utc, 12345678)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)

    def test_l1interface(self):
        """Testing function l1interface."""
        # Create a mock l1interface row
        MockRow = namedtuple(
            'MockRow',
            [
                'idx_l1interface', 'idx_device', 'ifindex', 'duplex', 'ethernet',
                'nativevlan', 'trunk', 'iftype', 'ifspeed', 'ifalias', 'ifname',
                'ifdescr', 'ifadminstatus', 'ifoperstatus', 'ts_idle',
                'cdpcachedeviceid', 'cdpcachedeviceport', 'cdpcacheplatform',
                'lldpremportdesc', 'lldpremsyscapenabled', 'lldpremsysdesc',
                'lldpremsysname', 'enabled', 'ts_created', 'ts_modified'
            ]
        )
        
        # Test with values present
        mock_row = MockRow(
            idx_l1interface=1,
            idx_device=2,
            ifindex=3,
            duplex=1,
            ethernet=1,
            nativevlan=10,
            trunk=1,
            iftype=6,
            ifspeed=1000000000,
            ifalias='test_alias'.encode(),
            ifname='GigabitEthernet0/1'.encode(),
            ifdescr='test_descr'.encode(),
            ifadminstatus=1,
            ifoperstatus=1,
            ts_idle=0,
            cdpcachedeviceid='SWITCH-B'.encode(),
            cdpcachedeviceport='GigabitEthernet0/24'.encode(),
            cdpcacheplatform='cisco WS-C3750'.encode(),
            lldpremportdesc='GigabitEthernet0/24'.encode(),
            lldpremsyscapenabled='Router'.encode(),
            lldpremsysdesc='Cisco IOS Software'.encode(),
            lldpremsysname='SWITCH-B'.encode(),
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.l1interface(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RL1Interface)
        
        # Check a few key values
        self.assertEqual(result.idx_l1interface, 1)
        self.assertEqual(result.idx_device, 2)
        self.assertEqual(result.ifindex, 3)
        self.assertEqual(result.ifalias, 'test_alias')
        self.assertEqual(result.ifname, 'GigabitEthernet0/1')
        self.assertEqual(result.ifdescr, 'test_descr')
        self.assertEqual(result.cdpcachedeviceid, 'SWITCH-B')
        self.assertEqual(result.cdpcachedeviceport, 'GigabitEthernet0/24')
        self.assertEqual(result.lldpremsysname, 'SWITCH-B')
        self.assertEqual(result.enabled, 1)
        
        # Test with None values
        mock_row = MockRow(
            idx_l1interface=1,
            idx_device=2,
            ifindex=3,
            duplex=1,
            ethernet=1,
            nativevlan=10,
            trunk=1,
            iftype=6,
            ifspeed=1000000000,
            ifalias=None,
            ifname=None,
            ifdescr=None,
            ifadminstatus=1,
            ifoperstatus=1,
            ts_idle=0,
            cdpcachedeviceid=None,
            cdpcachedeviceport=None,
            cdpcacheplatform=None,
            lldpremportdesc=None,
            lldpremsyscapenabled=None,
            lldpremsysdesc=None,
            lldpremsysname=None,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.l1interface(mock_row)
        
        # Check None values
        self.assertIsNone(result.ifalias)
        self.assertIsNone(result.ifname)
        self.assertIsNone(result.ifdescr)
        self.assertIsNone(result.cdpcachedeviceid)
        self.assertIsNone(result.lldpremsysname)
        self.assertEqual(result.enabled, 0)

    def test_mac(self):
        """Testing function mac."""
        # Create a mock mac row
        MockRow = namedtuple(
            'MockRow',
            ['idx_mac', 'idx_oui', 'idx_zone', 'mac', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_mac=1,
            idx_oui=2,
            idx_zone=3,
            mac='aabbccddeeff'.encode(),
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.mac(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RMac)
        
        # Check values
        self.assertEqual(result.idx_mac, 1)
        self.assertEqual(result.idx_oui, 2)
        self.assertEqual(result.idx_zone, 3)
        self.assertEqual(result.mac, 'aabbccddeeff')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)
        
        # Test with None values
        mock_row = MockRow(
            idx_mac=1,
            idx_oui=2,
            idx_zone=3,
            mac=None,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.mac(mock_row)
        self.assertIsNone(result.mac)
        self.assertEqual(result.enabled, 0)

    def test_macip(self):
        """Testing function macip."""
        # Create a mock macip row
        MockRow = namedtuple(
            'MockRow',
            ['idx_macip', 'idx_ip', 'idx_mac', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_macip=1,
            idx_ip=2,
            idx_mac=3,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.macip(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RMacIp)
        
        # Check values
        self.assertEqual(result.idx_macip, 1)
        self.assertEqual(result.idx_ip, 2)
        self.assertEqual(result.idx_mac, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)

    def test_macport(self):
        """Testing function macport."""
        # Create a mock macport row
        MockRow = namedtuple(
            'MockRow',
            ['idx_macport', 'idx_l1interface', 'idx_mac', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_macport=1,
            idx_l1interface=2,
            idx_mac=3,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.macport(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RMacPort)
        
        # Check values
        self.assertEqual(result.idx_macport, 1)
        self.assertEqual(result.idx_l1interface, 2)
        self.assertEqual(result.idx_mac, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)

    def test_oui(self):
        """Testing function oui."""
        # Create a mock oui row
        MockRow = namedtuple(
            'MockRow',
            ['idx_oui', 'oui', 'organization', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_oui=1,
            oui='aabbcc'.encode(),
            organization='Test Company Inc.'.encode(),
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.oui(mock_row)
        
        # Check result type
        self.assertIsInstance(result, ROui)
        
        # Check values
        self.assertEqual(result.idx_oui, 1)
        self.assertEqual(result.oui, 'aabbcc')
        self.assertEqual(result.organization, 'Test Company Inc.')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)
        
        # Test with None values
        mock_row = MockRow(
            idx_oui=1,
            oui=None,
            organization=None,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.oui(mock_row)
        self.assertIsNone(result.oui)
        self.assertIsNone(result.organization)
        self.assertEqual(result.enabled, 0)

    def test_vlan(self):
        """Testing function vlan."""
        # Create a mock vlan row
        MockRow = namedtuple(
            'MockRow',
            ['idx_vlan', 'idx_device', 'vlan', 'name', 'state', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_vlan=1,
            idx_device=2,
            vlan=10,
            name='VLAN10-DATA'.encode(),
            state=1,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.vlan(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RVlan)
        
        # Check values
        self.assertEqual(result.idx_vlan, 1)
        self.assertEqual(result.idx_device, 2)
        self.assertEqual(result.vlan, 10)
        self.assertEqual(result.name, 'VLAN10-DATA')
        self.assertEqual(result.state, 1)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)
        
        # Test with None values
        mock_row = MockRow(
            idx_vlan=1,
            idx_device=2,
            vlan=10,
            name=None,
            state=1,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.vlan(mock_row)
        self.assertIsNone(result.name)
        self.assertEqual(result.enabled, 0)

    def test_vlanport(self):
        """Testing function vlanport."""
        # Create a mock vlanport row
        MockRow = namedtuple(
            'MockRow',
            ['idx_vlanport', 'idx_l1interface', 'idx_vlan', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_vlanport=1,
            idx_l1interface=2,
            idx_vlan=3,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.vlanport(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RVlanPort)
        
        # Check values
        self.assertEqual(result.idx_vlanport, 1)
        self.assertEqual(result.idx_l1interface, 2)
        self.assertEqual(result.idx_vlan, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)

    def test_zone(self):
        """Testing function zone."""
        # Create a mock zone row
        MockRow = namedtuple(
            'MockRow',
            ['idx_zone', 'idx_event', 'name', 'notes', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_zone=1,
            idx_event=2,
            name='test_zone'.encode(),
            notes='test notes'.encode(),
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.zone(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RZone)
        
        # Check values
        self.assertEqual(result.idx_zone, 1)
        self.assertEqual(result.idx_event, 2)
        self.assertEqual(result.name, 'test_zone')
        self.assertEqual(result.notes, 'test notes')
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)
        
        # Test with None values
        mock_row = MockRow(
            idx_zone=1,
            idx_event=2,
            name=None,
            notes=None,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.zone(mock_row)
        self.assertIsNone(result.name)
        self.assertIsNone(result.notes)
        self.assertEqual(result.enabled, 0)

    def test_ip(self):
        """Testing function ip."""
        # Create a mock ip row
        MockRow = namedtuple(
            'MockRow',
            ['idx_ip', 'idx_zone', 'address', 'hostname', 'version', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_ip=1,
            idx_zone=2,
            address='192.168.1.1'.encode(),
            hostname='router-1.example.com'.encode(),
            version=4,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.ip(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RIp)
        
        # Check values
        self.assertEqual(result.idx_ip, 1)
        self.assertEqual(result.idx_zone, 2)
        self.assertEqual(result.address, '192.168.1.1')
        self.assertEqual(result.hostname, 'router-1.example.com')
        self.assertEqual(result.version, 4)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)
        
        # Test with None values
        mock_row = MockRow(
            idx_ip=1,
            idx_zone=2,
            address=None,
            hostname=None,
            version=4,
            enabled=0,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.ip(mock_row)
        self.assertIsNone(result.address)
        self.assertIsNone(result.hostname)
        self.assertEqual(result.enabled, 0)

    def test_ipport(self):
        """Testing function ipport."""
        # Create a mock ipport row
        MockRow = namedtuple(
            'MockRow',
            ['idx_ipport', 'idx_l1interface', 'idx_ip', 'enabled', 'ts_created', 'ts_modified']
        )
        
        mock_row = MockRow(
            idx_ipport=1,
            idx_l1interface=2,
            idx_ip=3,
            enabled=1,
            ts_created=111111,
            ts_modified=222222
        )
        
        result = testimport.ipport(mock_row)
        
        # Check result type
        self.assertIsInstance(result, RIpPort)
        
        # Check values
        self.assertEqual(result.idx_ipport, 1)
        self.assertEqual(result.idx_l1interface, 2)
        self.assertEqual(result.idx_ip, 3)
        self.assertEqual(result.enabled, 1)
        self.assertEqual(result.ts_created, 111111)
        self.assertEqual(result.ts_modified, 222222)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()