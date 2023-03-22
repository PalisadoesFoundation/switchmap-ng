#!/usr/bin/env python3
"""Test the configuration module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}dashboard".format(os.sep)
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


from switchmap.dashboard import uri as test_module


class TestFunctions(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_dashboard(self):
        """Testing function dashboard."""
        # Initialize key variables
        expected = "/switchmap/api/dashboard"
        result = test_module.dashboard()

        # Test
        self.assertEqual(result, expected)

    def test_historical_dashboard(self):
        """Testing function historical_dashboard."""
        # Initialize key variables
        root = 25
        expected = "/switchmap/api/dashboard/{}".format(root)
        result = test_module.historical_dashboard(root)

        # Test
        self.assertEqual(result, expected)

    def test_devices(self):
        """Testing function devices."""
        # Initialize key variables
        expected = "/switchmap/api/devices/1"
        result = test_module.devices(1)

        # Test
        self.assertEqual(result, expected)

    def test_events(self):
        """Testing function event."""
        # Initialize key variables
        expected = "/switchmap/api/events"
        result = test_module.events()

        # Test
        self.assertEqual(result, expected)

    def test_search_api_server(self):
        """Testing function search_api_server."""
        # Initialize key variables
        expected = "/post/search"
        result = test_module.search_api_server()

        # Test
        self.assertEqual(result, expected)

    def test_search_dashboard_server(self):
        """Testing function search_dashboard_server."""
        # Initialize key variables
        expected = "/search"

        # Test
        result = test_module.search_dashboard_server()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
