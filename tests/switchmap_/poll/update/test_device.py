#!/usr/bin/env python3
"""Test the device module."""

import os
import sys
import unittest
from copy import deepcopy


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '''{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}update\
'''.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


# Create the necessary configuration
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

from switchmap.poll.update import device as testimport
from switchmap.db.models import Oui
from switchmap.db.table import ROui
from switchmap.db.table import IOui
from switchmap.db import models

from tests.testlib_ import db
from tests.testlib_ import data


def _prerequisites():
    """Create prerequisite data.

    Strip out all l1_ keys from the data

    Args:
        None

    Returns:
        result: Stripped data

    """
    # Get data
    result = deepcopy(data.polled_data())
    for key, _ in result['layer1'].items():
        if key.startswith('l1_'):
            result['layer1'].pop(key)
    return result


class TestSuiteDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    polled_data = _prerequisites()
    test_object = testimport.Device(polled_data)

    @classmethod
    def setUpClass(cls):
        """Steps to execute when before tests start."""
        # Do nothing
        pass

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Do nothing
        pass

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_process(self):
        """Testing function process."""
        # Get data
        result = self.test_object.process()
        expected = data.polled_data()
        print('boo')
        self.assertEqual(result, expected)


class TestSuite(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    polled_data = _prerequisites()

    @classmethod
    def setUpClass(cls):
        """Steps to execute when before tests start."""
        # Do nothing
        pass

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Do nothing

    def test__process_non_trunk(self):
        """Testing function _process_non_trunk."""
        pass

    def test__process_trunk(self):
        """Testing function _process_trunk."""
        pass

    def test__juniper_fix(self):
        """Testing function _juniper_fix."""
        pass

    def test__is_ethernet(self):
        """Testing function _is_ethernet."""
        pass

    def test__vlan(self):
        """Testing function _vlan."""
        pass

    def test__nativevlan(self):
        """Testing function _nativevlan."""
        pass

    def test__duplex(self):
        """Testing function _duplex."""
        pass

    def test_get_duplex_value(self):
        """Testing function get_duplex_value."""
        pass

    def test__trunk(self):
        """Testing function _trunk."""
        pass

    def test__idle_since(self):
        """Testing function _idle_since."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()

    # Cleanup the config
    CONFIG.cleanup()
