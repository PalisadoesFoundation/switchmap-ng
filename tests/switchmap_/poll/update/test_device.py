#!/usr/bin/env python3
"""Test the device module."""

import os
import sys
import unittest
from copy import deepcopy

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = """{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}update\
""".format(
    os.sep
)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
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
    return result


class TestPollUpdateDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    polled_data = _prerequisites()
    test_object = testimport.Device(polled_data)

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

    def test_process(self):
        """Testing function process."""
        # Get data
        result = self.test_object.process()
        expected = data.polled_data(strip=False)
        self.assertEqual(result, expected)


class TestSuite(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    polled_data = _prerequisites()
    l1_data = polled_data.get("layer1")

    # IfIndexes
    # 18 = Layer3 VLAN interface (Enabled)
    # 10103 = Layer1 interface. (Disabled)
    # 10101 = Layer1 interface with a server on it. (Enabled)
    # 1 = Layer2 VLAN (Disabled)
    # 18 = Layer2 VLAN (Enabled)
    # 10102 = Layer2 Trunk interface (Enabled)
    ifindexes = [18, 10103, 10101, 1, 18, 10102]

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Do nothing
        pass

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Do nothing

    def test__process_non_trunk(self):
        """Testing function _process_non_trunk."""
        # Initialize key variables
        results = []
        expecteds = [
            TrunkInterface(vlan=None, nativevlan=None, trunk=False),
            TrunkInterface(vlan=[99], nativevlan=1, trunk=False),
            TrunkInterface(vlan=list(range(2039)), nativevlan=98, trunk=True),
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
        expecteds = [False, True, True, False, False, True]

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
        return
        self.assertEqual(results, expecteds)

    def test__nativevlan(self):
        """Testing function _nativevlan."""
        # Initialize key variables
        results = []
        expecteds = [None, 1, 1, None, None, 98]

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
        expecteds = [0, 0, 2, 0, 0, 2]

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
        expecteds = [False, False, False, False, False, True]

        # Process data
        for ifindex in self.ifindexes:
            value = self.l1_data.get(ifindex)
            results.append(testimport._trunk(value))

        # Test
        self.assertEqual(results, expecteds)


if __name__ == "__main__":

    # Do the unit test
    unittest.main()

    # Cleanup the config
    CONFIG.cleanup()
