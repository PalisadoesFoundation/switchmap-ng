#!/usr/bin/env python3
"""Test the iana_enterprise module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}snmp'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from switchmap.poll.snmp import iana_enterprise as test_class


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
