#!/usr/bin/env python3
"""Test the mib_lldp module."""

import unittest
from mock import Mock

from switchmap.snmp import mib_lldp as testimport


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

        #####################################################################
        # Test supported fails because of mib_bridge depenency of __init__
        # Need to figure out how to fix
        #####################################################################
        # testobj = testimport.init_query(snmpobj)
        # self.assertEqual(testobj.supported(), True)
        #####################################################################

        # Set the stage for oid_exists returning False
        mock_spec = {'oid_exists.return_value': False}
        snmpobj.configure_mock(**mock_spec)

        # Test unsupported
        testobj = testimport.init_query(snmpobj)
        self.assertEqual(testobj.supported(), False)

    def test_layer1(self):
        """Testing method / function layer1."""
        # Initializing key variables
        length_in_bits = 16
        base = 16
        expected_dict = {
            199: {'lldpRemSysName': 'byte_string_1',
                  'lldpRemSysDesc': 'byte_string_1',
                  'lldpRemPortDesc': 'byte_string_1',
                  'lldpRemSysCapEnabled': 'byte_string_1'},
            299: {'lldpRemSysName': 'byte_string_2',
                  'lldpRemSysDesc': 'byte_string_2',
                  'lldpRemPortDesc': 'byte_string_2',
                  'lldpRemSysCapEnabled': 'byte_string_2'}
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
                # Test binary results separately from string results
                if secondary != 'lldpRemSysCapEnabled':
                    self.assertEqual(
                        results[primary][secondary],
                        expected_dict[primary][secondary])
                else:
                    # Convert results to binary string
                    original_string = expected_dict[primary][secondary]
                    hex_string = ''.join(
                        [hex(ord(character))[
                            2:] for character in original_string])
                    binary_string = bin(int(
                        hex_string, base))[2:].zfill(length_in_bits)

                    # Test
                    self.assertEqual(
                        results[primary][secondary], binary_string)

    def test_lldpremsysname(self):
        """Testing method / function lldpremsysname."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.lldpremsysname()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.lldpremsysname(oidonly=True)
        self.assertEqual(results, '.1.0.8802.1.1.2.1.4.1.1.9')

    def test_lldpremsyscapenabled(self):
        """Testing method / function lldpremsyscapenabled."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.lldpremsyscapenabled()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.lldpremsyscapenabled(oidonly=True)
        self.assertEqual(results, '.1.0.8802.1.1.2.1.4.1.1.12')

    def test_lldpremsysdesc(self):
        """Testing method / function lldpremsysdesc."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.lldpremsysdesc()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.lldpremsysdesc(oidonly=True)
        self.assertEqual(results, '.1.0.8802.1.1.2.1.4.1.1.10')

    def test_lldpremportdesc(self):
        """Testing method / function lldpremportdesc."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        mock_spec = {'swalk.return_value': self.walk_results_string}
        snmpobj.configure_mock(**mock_spec)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = testobj.lldpremportdesc()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = testobj.lldpremportdesc(oidonly=True)
        self.assertEqual(results, '.1.0.8802.1.1.2.1.4.1.1.8')

    def test__penultimate_node(self):
        """Testing method / function _penultimate_node."""
        # Initializing key variables
        oid = '.1.2.3.4.5.6.7.8.9.10'

        # Do test. Should return penultimate OID node.
        result = testimport._penultimate_node(oid)
        self.assertEqual(result, 9)

if __name__ == '__main__':

    # Do the unit test
    unittest.main()
