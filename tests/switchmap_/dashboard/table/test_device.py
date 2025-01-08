#!/usr/bin/env python3
"""Test the Device class."""

import os
import sys
import unittest
from unittest.mock import patch

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}"
    "dashboard{0}table".format(os.sep)
)
if EXEC_DIR.endswith(_EXPECTED):
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        f'This script is not installed in the "{_EXPECTED}" directory. '
        "Please fix."
    )
    sys.exit(2)

# Import the module to test
from switchmap.dashboard.table import device


class TestDevice(unittest.TestCase):
    """Unit tests for the Device class."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        pass

    @patch("switchmap.dashboard.table.interfaces.table")
    def test_interfaces_with_valid_data(self, mock_table):
        """Test the interfaces method with valid data."""
        mock_table.return_value = "Mocked Interface Table"
        test_data = {
            "l1interfaces": {"interface1": "data1", "interface2": "data2"}
        }
        device_instance = device.Device(test_data)
        result = device_instance.interfaces()
        mock_table.assert_called_once_with(test_data["l1interfaces"])
        self.assertEqual(result, "Mocked Interface Table")

    @patch("switchmap.dashboard.table.interfaces.table")
    def test_interfaces_with_empty_data(self, mock_table):
        """Test the interfaces method with empty data."""
        test_data = {"l1interfaces": {}}
        device_instance = device.Device(test_data)
        result = device_instance.interfaces()
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch("switchmap.dashboard.table.interfaces.table")
    def test_interfaces_with_none_data(self, mock_table):
        """Test the interfaces method with None as data."""
        test_data = {"l1interfaces": None}
        device_instance = device.Device(test_data)
        result = device_instance.interfaces()
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch("switchmap.dashboard.table.system.table")
    def test_system_with_valid_data(self, mock_table):
        """Test the system method with valid data."""
        mock_table.return_value = "Mocked System Table"
        test_data = {"key1": "value1", "key2": "value2"}
        device_instance = device.Device(test_data)
        result = device_instance.system()
        mock_table.assert_called_once_with(test_data)
        self.assertEqual(result, "Mocked System Table")

    @patch("switchmap.dashboard.table.system.table")
    def test_system_with_empty_data(self, mock_table):
        """Test the system method with empty data."""
        test_data = {}
        device_instance = device.Device(test_data)
        result = device_instance.system()
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch("switchmap.dashboard.table.system.table")
    def test_system_with_none_data(self, mock_table):
        """Test the system method with None as data."""
        test_data = None
        device_instance = device.Device(test_data)
        result = device_instance.system()
        mock_table.assert_not_called()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
