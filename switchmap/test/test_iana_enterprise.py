#!/usr/bin/env python3
"""Test the iana_enterprise module."""

import unittest

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
