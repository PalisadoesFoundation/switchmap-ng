#!/usr/bin/env python3

import unittest
import os
import sys
from unittest.mock import patch

# Add the project root directory to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print(sys.path)  # Debugging: Check if the correct path is included

# Import the module to test
from switchmap.dashboard.table import device


class TestDevice(unittest.TestCase):
    """Unit tests for the Device class."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        pass  # No special setup needed for this class

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        pass  # No special teardown needed for this class

    @patch('switchmap.dashboard.table.interfaces.table')
    def test_interfaces_with_valid_data(self, mock_table):
        """Test the interfaces method with valid data."""
        # Mock return value
        mock_table.return_value = "Mocked Interface Table"

        # Test input
        test_data = {"l1interfaces": {"interface1": "data1", "interface2": "data2"}}

        # Create an instance of Device
        device_instance = device.Device(test_data)

        # Call the interfaces method
        result = device_instance.interfaces()

        # Assertions
        mock_table.assert_called_once_with(test_data["l1interfaces"])
        self.assertEqual(result, "Mocked Interface Table")

    @patch('switchmap.dashboard.table.interfaces.table')
    def test_interfaces_with_empty_data(self, mock_table):
        """Test the interfaces method with empty data."""
        # Test input
        test_data = {"l1interfaces": {}}

        # Create an instance of Device
        device_instance = device.Device(test_data)

        # Call the interfaces method
        result = device_instance.interfaces()

        # Assertions
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch('switchmap.dashboard.table.interfaces.table')
    def test_interfaces_with_none_data(self, mock_table):
        """Test the interfaces method with None as data."""
        # Test input
        test_data = {"l1interfaces": None}

        # Create an instance of Device
        device_instance = device.Device(test_data)

        # Call the interfaces method
        result = device_instance.interfaces()

        # Assertions
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch('switchmap.dashboard.table.system.table')
    def test_system_with_valid_data(self, mock_table):
        """Test the system method with valid data."""
        # Mock return value
        mock_table.return_value = "Mocked System Table"

        # Test input
        test_data = {"key1": "value1", "key2": "value2"}

        # Create an instance of Device
        device_instance = device.Device(test_data)

        # Call the system method
        result = device_instance.system()

        # Assertions
        mock_table.assert_called_once_with(test_data)
        self.assertEqual(result, "Mocked System Table")

    @patch('switchmap.dashboard.table.system.table')
    def test_system_with_empty_data(self, mock_table):
        """Test the system method with empty data."""
        # Test input
        test_data = {}

        # Create an instance of Device
        device_instance = device.Device(test_data)

        # Call the system method
        result = device_instance.system()

        # Assertions
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch('switchmap.dashboard.table.system.table')
    def test_system_with_none_data(self, mock_table):
        """Test the system method with None as data."""
        # Test input
        test_data = None

        # Create an instance of Device
        device_instance = device.Device(test_data)

        # Call the system method
        result = device_instance.system()

        # Assertions
        mock_table.assert_not_called()
        self.assertIsNone(result)


if __name__ == "__main__":
    # Run the unit tests
    unittest.main()