#!/usr/bin/env python3
"""Test the mib_lldp module."""

import unittest
from mock import Mock
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

    def test_supported(self):
        """Testing method / function supported."""
        # Don't know how to test this.
        return

    def test_layer1(self):
        """Testing method / function layer1."""
        # Don't know how to test this.
        return

    def test_lldpremsysname(self):
        """Testing method / function lldpremsysname."""
        # Don't know how to test this.
        return

    def test_lldpremsyscapenabled(self):
        """Testing method / function lldpremsyscapenabled."""
        # Don't know how to test this.
        return

    def test_lldpremsysdesc(self):
        """Testing method / function lldpremsysdesc."""
        # Don't know how to test this.
        return

    def test_lldpremportdesc(self):
        """Testing method / function lldpremportdesc."""
        # Set the stage for SNMPwalk
        # Don't know how to test this.
        return

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
