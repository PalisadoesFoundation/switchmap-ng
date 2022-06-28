#!/usr/bin/env python3
"""Test the mib_qbridge module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                os.path.abspath(os.path.join(
                    os.path.abspath(os.path.join(
                        EXEC_DIR,
                        os.pardir)), os.pardir)), os.pardir)), os.pardir)),
        os.pardir)), os.pardir))
_EXPECTED = '''\
{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}snmp{0}mib{0}generic\
'''.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Create the necessary configuration to load the module
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

# Import other required libraries


class Query():
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


class TestMibQBridgeFunctions(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Steps to execute before tests start."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test_get_query(self):
        """Testing function get_query."""
        pass

    def test_init_query(self):
        """Testing function init_query."""
        pass


class TestMibQBridge(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Steps to execute before tests start."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_layer1(self):
        """Testing function layer1."""
        pass

    def test_layer2(self):
        """Testing function layer2."""
        pass

    def test_dot1qpvid(self):
        """Testing function dot1qpvid."""
        pass

    def test_dot1qvlanstaticname(self):
        """Testing function dot1qvlanstaticname."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
