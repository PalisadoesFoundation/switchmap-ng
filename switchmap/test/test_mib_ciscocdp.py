#!/usr/bin/env python3
"""Test the mib_ciscocdp module."""

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

from switchmap.snmp.cisco import mib_ciscocdp as testimport


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


class KnownValues(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Regular walk returning byte strings
    walk_results_string = {
        '.0.1.2.3.4.5.6.7.8.199.100': b'byte_string_1',
        '.0.1.2.3.4.5.6.7.8.299.200': b'byte_string_2'
    }

    def test_supported(self):
        """Testing method / function supported."""
        # Set the stage for oid_exists returning True
        snmpobj = Mock(spec=Query)
        mock_spec = {'oid_exists.return_value': True}
        snmpobj.configure_mock(**mock_spec)

        # Test supported
        testobj = testimport.init_query(snmpobj)
        self.assertEqual(testobj.supported(), True)

        # Set the stage for oid_exists returning False
        mock_spec = {'oid_exists.return_value': False}
        snmpobj.configure_mock(**mock_spec)

        # Test unsupported
        testobj = testimport.init_query(snmpobj)
        self.assertEqual(testobj.supported(), False)

    def test_layer1(self):
        """Testing method / function layer1."""
        # Initializing key variables
        expected_dict = {
            199: {'cdpCacheDeviceId': 'byte_string_1',
                  'cdpCachePlatform': 'byte_string_1',
                  'cdpCacheDevicePort': 'byte_string_1'},
            299: {'cdpCacheDeviceId': 'byte_string_2',
                  'cdpCachePlatform': 'byte_string_2',
                  'cdpCacheDevicePort': 'byte_string_2'}
        }

        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.layer1()

        # Basic testing of results
        for primary in results.keys():
            for secondary in results[primary].keys():
                self.assertEqual(
                    results[primary][secondary],
                    expected_dict[primary][secondary])

    def test_cdpcachedeviceid(self):
        """Testing method / function cdpcachedeviceid."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.cdpcachedeviceid()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.cdpcachedeviceid(oidonly=True)
        self.assertEqual(results, '.1.3.6.1.4.1.9.9.23.1.2.1.1.6')

    def test_cdpcacheplatform(self):
        """Testing method / function cdpcacheplatform."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.cdpcacheplatform()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.cdpcacheplatform(oidonly=True)
        self.assertEqual(results, '.1.3.6.1.4.1.9.9.23.1.2.1.1.8')

    def test_cdpcachedeviceport(self):
        """Testing method / function cdpcachedeviceport."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.cdpcachedeviceport()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.cdpcachedeviceport(oidonly=True)
        self.assertEqual(results, '.1.3.6.1.4.1.9.9.23.1.2.1.1.7')

    def test__ifindex(self):
        """Testing method / function _ifindex."""
        # Initializing key variables
        oid = '.1.2.3.4.5.6.7.8.9.10'

        # Do test. Should return penultimate OID node.
        result = testimport._ifindex(oid)
        self.assertEqual(result, 9)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
