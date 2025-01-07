#!/usr/bin/env python3
"""Test the Search class."""

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
from switchmap.dashboard.table import search


class TestSearch(unittest.TestCase):
    """Unit tests for the Search class."""

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
        mock_table.return_value = "Mocked Table"

        # Test input
        test_data = {"interface1": "data1", "interface2": "data2"}

        # Create an instance of Search
        search_instance = search.Search(test_data)

        # Call the interfaces method
        result = search_instance.interfaces()

        # Assertions
        mock_table.assert_called_once_with(test_data)
        self.assertEqual(result, "Mocked Table")

    @patch('switchmap.dashboard.table.interfaces.table')
    def test_interfaces_with_empty_data(self, mock_table):
        """Test the interfaces method with empty data."""
        # Test input
        test_data = {}

        # Create an instance of Search
        search_instance = search.Search(test_data)

        # Call the interfaces method
        result = search_instance.interfaces()

        # Assertions
        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch('switchmap.dashboard.table.interfaces.table')
    def test_interfaces_with_none_data(self, mock_table):
        """Test the interfaces method with None as data."""
        # Test input
        test_data = None

        # Create an instance of Search
        search_instance = search.Search(test_data)

        # Call the interfaces method
        result = search_instance.interfaces()

        # Assertions
        mock_table.assert_not_called()
        self.assertIsNone(result)


if __name__ == "__main__":
    # Run the unit tests
    unittest.main()
