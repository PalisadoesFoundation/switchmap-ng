#!/usr/bin/env python3
"""Test the mib_essswitch module."""

import os
import sys
import unittest
from mock import Mock

# Try to create a working PYTHONPATH
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SWITCHMAP_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, os.pardir))
ROOT_DIRECTORY = os.path.abspath(os.path.join(SWITCHMAP_DIRECTORY, os.pardir))
if TEST_DIRECTORY.endswith('/switchmap-ng/switchmap/test') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

from switchmap.snmp import mib_if_64 as testimport


class Query(object):
    """Class for snmp_manager.Query mock.

    A detailed tutorial about Python mocks can be found here:
    http://www.drdobbs.com/testing/using-mocks-in-python/240168251

    """

    def query(self):
        """Do an SNMP query."""
        pass

    def oid_exists(self):
        """Determine existence of OID on device."""
        pass

    def swalk(self):
        """Do a failsafe SNMPwalk."""
        pass

    def walk(self):
        """Do a failable SNMPwalk."""
        pass


class KnownValues(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Normalized walk returning integers
    nwalk_results_integer = {
        100: 1234,
        200: 5678
    }

    # Set the stage for SNMPwalk for integer results
    snmpobj_integer = Mock(spec=Query)
    mock_spec_integer = {
        'swalk.return_value': nwalk_results_integer,
        'walk.return_value': nwalk_results_integer,
        }
    snmpobj_integer.configure_mock(**mock_spec_integer)

    # Initializing key variables
    expected_dict = {
        100: {
            'ifHCOutBroadcastPkts': 1234,
            'ifHCOutMulticastPkts': 1234,
            'ifHCOutUcastPkts': 1234,
            'ifHCOutOctets': 1234,
            'ifHCInBroadcastPkts': 1234,
            'ifHCInMulticastPkts': 1234,
            'ifHCInUcastPkts': 1234,
            'ifHCInOctets': 1234,
            'ifHighSpeed': 1234
        },
        200: {
            'ifHCOutBroadcastPkts': 5678,
            'ifHCOutMulticastPkts': 5678,
            'ifHCOutUcastPkts': 5678,
            'ifHCOutOctets': 5678,
            'ifHCInBroadcastPkts': 5678,
            'ifHCInMulticastPkts': 5678,
            'ifHCInUcastPkts': 5678,
            'ifHCInOctets': 5678,
            'ifHighSpeed': 5678
        }
    }

    def test_get_query(self):
        """Testing method / function get_query."""
        # Initializing key variables
        pass

    def test_init_query(self):
        """Testing method / function init_query."""
        # Initializing key variables
        pass

    def test_system(self):
        """Testing method / function system."""
        # Initializing key variables
        pass

    def test_layer1(self):
        """Testing method / function layer1."""
        # Initializing key variables
        pass

    def test_ifhighspeed(self):
        """Testing method / function ifhighspeed."""
        # Initialize key variables
        oid_key = 'ifHighSpeed'
        oid = '.1.3.6.1.2.1.31.1.1.1.15'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhighspeed()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhighspeed(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcinucastpkts(self):
        """Testing method / function ifhcinucastpkts."""
        # Initialize key variables
        oid_key = 'ifHCInUcastPkts'
        oid = '.1.3.6.1.2.1.31.1.1.1.7'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcinucastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcinucastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcoutucastpkts(self):
        """Testing method / function ifhcoutucastpkts."""
        # Initialize key variables
        oid_key = 'ifHCOutUcastPkts'
        oid = '.1.3.6.1.2.1.31.1.1.1.11'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcoutucastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcoutucastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcinmulticastpkts(self):
        """Testing method / function ifhcinmulticastpkts."""
        # Initialize key variables
        oid_key = 'ifHCInMulticastPkts'
        oid = '.1.3.6.1.2.1.31.1.1.1.8'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcinmulticastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcinmulticastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcoutmulticastpkts(self):
        """Testing method / function ifhcoutmulticastpkts."""
        # Initialize key variables
        oid_key = 'ifHCOutMulticastPkts'
        oid = '.1.3.6.1.2.1.31.1.1.1.12'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcoutmulticastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcoutmulticastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcinbroadcastpkts(self):
        """Testing method / function ifhcinbroadcastpkts."""
        # Initialize key variables
        oid_key = 'ifHCInBroadcastPkts'
        oid = '.1.3.6.1.2.1.31.1.1.1.9'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcinbroadcastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcinbroadcastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcoutbroadcastpkts(self):
        """Testing method / function ifhcoutbroadcastpkts."""
        # Initialize key variables
        oid_key = 'ifHCOutBroadcastPkts'
        oid = '.1.3.6.1.2.1.31.1.1.1.13'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcoutbroadcastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcoutbroadcastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcinoctets(self):
        """Testing method / function ifhcinoctets."""
        # Initialize key variables
        oid_key = 'ifHCInOctets'
        oid = '.1.3.6.1.2.1.31.1.1.1.6'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcinoctets()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcinoctets(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifhcoutoctets(self):
        """Testing method / function ifhcoutoctets."""
        # Initialize key variables
        oid_key = 'ifHCOutOctets'
        oid = '.1.3.6.1.2.1.31.1.1.1.10'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifhcoutoctets()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifhcoutoctets(oidonly=True)
        self.assertEqual(results, oid)

    def test__get_data(self):
        """Testing method / function _get_data."""
        # Initializing key variables
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
