#!/usr/bin/env python3
"""Test the mib_ciscovlanmembership module."""

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

from switchmap.snmp.cisco import mib_ciscovlanmembership as testimport


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
        """Do a SNMPwalk."""
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
        200: 4567
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
            'vmPortStatus': 1234,
            'vmVlan': 1234
        },
        200: {
            'vmPortStatus': 4567,
            'vmVlan': 4567
        }
    }

    def test_get_query(self):
        """Testing function get_query."""
        pass

    def test_init_query(self):
        """Testing function init_query."""
        pass

    def test___init__(self):
        """Testing function __init__."""
        pass

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
        """Testing function layer1."""
        # Initializing key variables
        expected_dict = {
            100: {'vmPortStatus': 1234,
                  'vmVlan': 1234},
            200: {'vmPortStatus': 4567,
                  'vmVlan': 4567}
        }

        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.nwalk_results_integer}
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

    def test_vmvlan(self):
        """Testing function vmvlan."""
        oid_key = 'vmVlan'
        oid = '.1.3.6.1.4.1.9.9.68.1.2.2.1.2'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.vmvlan()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.vmvlan(oidonly=True)
        self.assertEqual(results, oid)

    def test_vmportstatus(self):
        """Testing function vmportstatus."""
        # Initialize key variables
        oid_key = 'vmPortStatus'
        oid = '.1.3.6.1.4.1.9.9.68.1.2.2.1.3'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.vmportstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.vmportstatus(oidonly=True)
        self.assertEqual(results, oid)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
