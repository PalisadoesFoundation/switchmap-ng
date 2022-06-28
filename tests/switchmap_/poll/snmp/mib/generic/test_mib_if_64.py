#!/usr/bin/env python3
"""Test the mib_if_64 module."""

import os
import sys
import unittest
from mock import Mock

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                os.path.abspath(os.path.join(
                    os.path.abspath(os.path.join(
                        EXEC_DIR,
                        os.pardir)), os.pardir)), os.pardir)), os.pardir)),
        os.pardir)), os.pardir))
_EXPECTED = '''\
{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}snmp{0}mib{0}generic\
'''.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Create the necessary configuration to load the module
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

# Import other required libraries
from switchmap.poll.snmp.mib.generic import mib_if_64 as testimport


class Query():
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


class TestMibIf64Functions(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Steps to execute before tests start."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test_get_query(self):
        """Testing function get_query."""
        pass

    def test_init_query(self):
        """Testing function init_query."""
        pass


class TestMibIf64(unittest.TestCase):
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

    @classmethod
    def setUpClass(cls):
        """Steps to execute before tests start."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

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
        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.layer1()

        # Basic testing of results
        for primary in results.keys():
            for secondary in results[primary].keys():
                self.assertEqual(
                    results[primary][secondary],
                    self.expected_dict[primary][secondary])

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
