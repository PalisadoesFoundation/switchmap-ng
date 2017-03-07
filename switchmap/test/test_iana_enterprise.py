#!/usr/bin/env python3
"""Test the iana_enterprise module."""

import unittest
import os
import sys

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

from switchmap.snmp import iana_enterprise as test_class


class KnownValues(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    def test_enterprise(self):
        """Testing method / function enterprise."""
        # Initializing key variables
        testobj = test_class.Query(sysobjectid='.1.2.3.4.5.6.100.101.102')
        result = testobj.enterprise()
        self.assertEqual(result, 100)

    def test_is_cisco(self):
        """Testing method / function is_cisco."""
        # Test for Cisco sysObjectID
        testobj = test_class.Query(sysobjectid='.1.2.3.4.5.6.9.101.102')
        result = testobj.is_cisco()
        self.assertEqual(result, True)

        # Test for fake vendor
        testobj = test_class.Query(
            sysobjectid='.1.2.3.4.5.6.100000000000000.101.102')
        result = testobj.is_cisco()
        self.assertEqual(result, False)

    def test_is_juniper(self):
        """Testing method / function is_juniper."""
        # Test for Juniper sysObjectID
        testobj = test_class.Query(sysobjectid='.1.2.3.4.5.6.2636.101.102')
        result = testobj.is_juniper()
        self.assertEqual(result, True)

        # Test for fake vendor
        testobj = test_class.Query(
            sysobjectid='.1.2.3.4.5.6.100000000000000.101.102')
        result = testobj.is_juniper()
        self.assertEqual(result, False)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
