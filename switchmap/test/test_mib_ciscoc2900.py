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

from switchmap.snmp.cisco import mib_ciscoc2900 as testimport


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
            'c2900PortLinkbeatStatus': 1234,
            'c2900PortDuplexStatus': 1234,
        },
        200: {
            'c2900PortLinkbeatStatus': 5678,
            'c2900PortDuplexStatus': 5678,
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

    def test_layer1(self):
        """Testing function layer1."""
        # Initializing key variables
        expected_dict = {
            100: {
                'c2900PortLinkbeatStatus': 1234,
                'c2900PortDuplexStatus': 1234,
            },
            200: {
                'c2900PortLinkbeatStatus': 5678,
                'c2900PortDuplexStatus': 5678,
            }
        }

        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'walk.return_value': self.nwalk_results_integer}
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

    def test_c2900portlinkbeatstatus(self):
        """Testing function c2900portlinkbeatstatus."""
        # Initialize key variables
        oid_key = 'c2900PortLinkbeatStatus'
        oid = '.1.3.6.1.4.1.9.9.87.1.4.1.1.18'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.c2900portlinkbeatstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.c2900portlinkbeatstatus(oidonly=True)
        self.assertEqual(results, oid)

    def test_c2900portduplexstatus(self):
        """Testing function c2900portduplexstatus."""
        # Initialize key variables
        oid_key = 'c2900PortLinkbeatStatus'
        oid = '.1.3.6.1.4.1.9.9.87.1.4.1.1.32'

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.c2900portduplexstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.c2900portduplexstatus(oidonly=True)
        self.assertEqual(results, oid)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
