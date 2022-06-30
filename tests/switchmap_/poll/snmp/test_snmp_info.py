#!/usr/bin/env python3
"""Test the snmp_info module."""

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

# Create the necessary configuration to load the module
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

# Import other required libraries


class TestSnmpInfo(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_everything(self):
        """Testing function everything."""
        pass

    def test_misc(self):
        """Testing function misc."""
        pass

    def test_system(self):
        """Testing function system."""
        pass

    def test_layer1(self):
        """Testing function layer1."""
        pass

    def test_layer2(self):
        """Testing function layer2."""
        pass

    def test_layer3(self):
        """Testing function layer3."""
        pass

    def test__add_data(self):
        """Testing function _add_data."""
        pass

    def test__add_layer1(self):
        """Testing function _add_layer1."""
        pass

    def test__add_layer2(self):
        """Testing function _add_layer2."""
        pass

    def test__add_layer3(self):
        """Testing function _add_layer3."""
        pass

    def test__add_system(self):
        """Testing function _add_system."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
