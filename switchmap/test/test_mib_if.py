#!/usr/bin/env python3
"""Test the mib_essswitch module."""

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

from switchmap.snmp import mib_if as testimport


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

    def test_get_query(self):
        """Testing function get_query."""
        pass

    def test_init_query(self):
        """Testing function init_query."""
        pass

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_system(self):
        """Testing function system."""
        pass

    def test_layer1(self):
        """Testing function layer1."""
        pass

    def test_iflastchange(self):
        """Testing function iflastchange."""
        pass

    def test_ifinoctets(self):
        """Testing function ifinoctets."""
        pass

    def test_ifoutoctets(self):
        """Testing function ifoutoctets."""
        pass

    def test_ifdescr(self):
        """Testing function ifdescr."""
        pass

    def test_iftype(self):
        """Testing function iftype."""
        pass

    def test_ifspeed(self):
        """Testing function ifspeed."""
        pass

    def test_ifadminstatus(self):
        """Testing function ifadminstatus."""
        pass

    def test_ifoperstatus(self):
        """Testing function ifoperstatus."""
        pass

    def test_ifalias(self):
        """Testing function ifalias."""
        pass

    def test_ifname(self):
        """Testing function ifname."""
        pass

    def test_ifindex(self):
        """Testing function ifindex."""
        pass

    def test_ifphysaddress(self):
        """Testing function ifphysaddress."""
        pass

    def test_ifinmulticastpkts(self):
        """Testing function ifinmulticastpkts."""
        pass

    def test_ifoutmulticastpkts(self):
        """Testing function ifoutmulticastpkts."""
        pass

    def test_ifinbroadcastpkts(self):
        """Testing function ifinbroadcastpkts."""
        pass

    def test_ifoutbroadcastpkts(self):
        """Testing function ifoutbroadcastpkts."""
        pass

    def test_ifstackstatus(self):
        """Testing function ifstackstatus."""
        pass

    def test__get_data(self):
        """Testing function _get_data."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
