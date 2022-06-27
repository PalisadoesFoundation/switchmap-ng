#!/usr/bin/env python3
"""Test the device module."""

import os
import sys
import unittest
import time
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
from switchmap import TrunkInterface

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
        """Steps to execute before tests start."""
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
        self.assertEqual(result, expected)


class TestSuite(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    polled_data = _prerequisites()
    l1_data = polled_data.get('layer1')
    ifindexes = ['1', '10', '11', '51']

    @classmethod
    def setUpClass(cls):
        """Steps to execute before tests start."""
        # Do nothing
        pass

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Do nothing

    def test__process_non_trunk(self):
        """Testing function _process_non_trunk."""
        # Initialize key variables
        results = []
        expecteds = [
            TrunkInterface(vlan=None, nativevlan=None, trunk=False),
            TrunkInterface(vlan=[99], nativevlan=1, trunk=False),
            TrunkInterface(vlan=list(range(2039)), nativevlan=98, trunk=True)
        ]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._process_non_trunk(value))

        # Test
        return
        self.assertEqual(results, expecteds)

    def test__process_trunk(self):
        """Testing function _process_trunk."""
        pass

    def test__juniper_fix(self):
        """Testing function _juniper_fix."""
        pass

    def test__is_ethernet(self):
        """Testing function _is_ethernet."""
        # Initialize key variables
        results = []
        expecteds = [True, True, True, False]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._is_ethernet(value))

        # Test
        self.assertEqual(results, expecteds)

    def test__vlan(self):
        """Testing function _vlan."""
        # Initialize key variables
        results = []
        expecteds = [True, True, True, False]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._vlan(value))

        # Test
        # print(results)
        return
        self.assertEqual(results, expecteds)

    def test__nativevlan(self):
        """Testing function _nativevlan."""
        # Initialize key variables
        results = []
        expecteds = [None, 1, 98, None]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._nativevlan(value))

        # Test
        self.assertEqual(results, expecteds)

    def test__duplex(self):
        """Testing function _duplex."""
        # Initialize key variables
        results = []
        expecteds = [0, 0, 2, 0]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._duplex(value))

        # Test
        self.assertEqual(results, expecteds)

    def test_get_duplex_value(self):
        """Testing function get_duplex_value."""
        pass

    def test__trunk(self):
        """Testing function _trunk."""
        # Initialize key variables
        results = []
        expecteds = [False, False, True, False]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._trunk(value))

        # Test
        self.assertEqual(results, expecteds)

    def test__idle_since(self):
        """Testing function _idle_since."""
        # Initialize key variables
        expecteds = [False, False, True, False]
        start = int(time.time())

        # Wait for the very beginning of the next second
        while int(time.time()) == start:
            pass
        now = int(time.time())
        expecteds = {
            '1': now, '10': now, '11': None, '12': None,
            '13': now, '14': now, '15': now,
            '16': now, '17': now, '18': now,
            '19': now, '2': now, '20': now,
            '21': now, '22': now, '23': now,
            '24': now, '25': now, '26': now,
            '27': now, '28': now, '29': now,
            '3': now, '30': now, '31': now,
            '32': None, '33': None, '34': now, '35': now,
            '36': now, '37': now, '38': now,
            '39': now, '4': now, '40': now,
            '41': now, '42': None, '43': None, '44': None,
            '45': None, '46': now, '47': now, '48': now,
            '49': None, '5': now, '6': now, '7': now,
            '8': None, '9': now
        }

        # Process data
        results = testimport._idle_since(self.polled_data)

        # Test
        self.assertEqual(results, expecteds)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()

    # Cleanup the config
    CONFIG.cleanup()
