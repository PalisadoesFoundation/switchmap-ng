#!/usr/bin/env python3
"""Test the mib_ip module."""

import os
import sys
import unittest
import binascii
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

from switchmap.snmp import mib_ip as testimport
from switchmap.test import unittest_setup



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

    # Normalized walk returning binary data
    walk_results_ipv4_binary = {
        '.1.3.6.1.2.1.4.22.1.2.0.10.10.10.10': b'\x00\x16\xc2\x9c\x15P\x00',
        '.1.3.6.1.2.1.4.22.1.2.0.200.200.200.200': b'\xc2\x98\xc3\xae\xc3\x8bV%\xc2\xb6'
    }

    # OID with IPv6 appended in decimal format
    walk_results_ipv6_binary = {
        '.1.3.6.1.2.1.4.35.1.4.3.2.16.254.128.0.0.0.0.0.0'
        '.53.111.109.168.125.42.84.88': b'\xc3\x94\xc2\x85d\xc2\x9f\xc3\x9c\x7f',
        '.1.3.6.1.2.1.4.35.1.4.3.2.16.254.128.0.0.0.0.0.0'
        '.2.30.201.255.254.172.62.123': b'\xc3\x80|\xc3\x91\xc2\xa0\xc3\x82\xc2\x85'
    }

    # Set the stage for SNMPwalk for binary results
    snmpobj_ipv4_binary = Mock(spec=Query)
    mock_spec_ipv4_binary = {
        'swalk.return_value': walk_results_ipv4_binary,
        'walk.return_value': walk_results_ipv4_binary,
        }
    snmpobj_ipv4_binary.configure_mock(**mock_spec_ipv4_binary)

    snmpobj_ipv6_binary = Mock(spec=Query)
    mock_spec_ipv6_binary = {
        'swalk.return_value': walk_results_ipv6_binary,
        'walk.return_value': walk_results_ipv6_binary,
        }
    snmpobj_ipv6_binary.configure_mock(**mock_spec_ipv6_binary)

    # Initialize expected results
    ipv4_expected_dict = {
        '10.10.10.10': '00169c155000',
        '200.200.200.200': '98eecb5625b6'
    }

    ipv6_expected_dict = {
        'fe80:0000:0000:0000:356f:6da8:7d2a:5458': 'd485649fdc7f',
        'fe80:0000:0000:0000:021e:c9ff:feac:3e7b': 'c07cd1a0c285'
    }

    def test_get_query(self):
        """Testing method / function get_query."""
        # Initializing key variables
        pass

    def test_init_query(self):
        """Testing method / function init_query."""
        # Initializing key variables
        pass

    def test_supported(self):
        """Testing method / function supported."""
        # Initializing key variables
        pass

    def test_layer3(self):
        """Testing method / function layer3."""
        # Initializing key variables
        pass

    def test_ipnettomediatable(self):
        """Testing method / function ipnettomediatable."""
        # Initialize key variables
        oid = '.1.3.6.1.2.1.4.22.1.2'

        # Get results
        testobj = testimport.init_query(self.snmpobj_ipv4_binary)
        results = testobj.ipnettomediatable()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, str), True)
            self.assertEqual(value, self.ipv4_expected_dict[key])

        # Test that we are getting the correct OID
        results = testobj.ipnettomediatable(oidonly=True)
        self.assertEqual(results, oid)

    def test_ipnettophysicalphysaddress(self):
        """Testing method / function ipnettophysicalphysaddress."""
        # Initialize key variables
        oid = '.1.3.6.1.2.1.4.35.1.4'

        # Get results
        testobj = testimport.init_query(self.snmpobj_ipv6_binary)
        results = testobj.ipnettophysicalphysaddress()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, str), True)
            self.assertEqual(value, self.ipv6_expected_dict[key])

        # Test that we are getting the correct OID
        results = testobj.ipnettophysicalphysaddress(oidonly=True)
        self.assertEqual(results, oid)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
