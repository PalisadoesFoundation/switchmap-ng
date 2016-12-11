#!/usr/bin/env python3
"""Test the mib_essswitch module."""

import unittest
from mock import Mock

from switchmap.snmp import mib_essswitch as testimport


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

    # Normalized walk returning integers
    nwalk_results_integer = {
        100: 1234,
        200: 5678
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
            100: {'swPortDuplexStatus': 1234},
            200: {'swPortDuplexStatus': 5678}
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

    def test_swportduplexstatus(self):
        """Testing method / function swportduplexstatus."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.nwalk_results_integer}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.swportduplexstatus()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.swportduplexstatus(oidonly=True)
        self.assertEqual(results, '.1.3.6.1.4.1.437.1.1.3.3.1.1.30')


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
