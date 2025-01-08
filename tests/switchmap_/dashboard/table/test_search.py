#!/usr/bin/env python3
"""
Unit tests for the Search class in the switchmap.dashboard.table module.

This script verifies the functionality of the Search class, focusing on
its `interfaces` method under various conditions.
"""

import os
import sys
import unittest
from unittest.mock import patch

# Set up paths for correct module imports
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(EXEC_DIR, os.pardir, os.pardir, os.pardir, os.pardir)
)
_EXPECTED = (
    f"{os.sep}switchmap-ng{os.sep}tests{os.sep}switchmap_{os.sep}"
    f"dashboard{os.sep}table"
)

print(f"EXEC_DIR: {EXEC_DIR}")
print(f"ROOT_DIR: {ROOT_DIR}")

if EXEC_DIR.endswith(_EXPECTED):
    # Prepend path to ensure correct import paths
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        f"This script is not installed in the '{_EXPECTED}' directory. "
        "Please fix."
    )
    sys.exit(2)

# Import the module to test
from switchmap.dashboard.table import search


class TestSearch(unittest.TestCase):
    """
    Unit tests for the Search class.

    This class tests the behavior of the `interfaces` method under
    different input conditions, such as valid data, empty data, and None.
    """

    maxDiff = None  # Allow full diffs in test output

    @classmethod
    def setUpClass(cls):
        """Set up the test class environment."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        pass

    @patch("switchmap.dashboard.table.interfaces.table")
    def test_interfaces_with_valid_data(self, mock_table):
        """
        Test the interfaces method with valid data.

        Verify that the method calls the `table` function correctly 
        and returns the expected value.
        """
        mock_table.return_value = "Mocked Table"

        test_data = {"interface1": "data1", "interface2": "data2"}
        search_instance = search.Search(test_data)
        result = search_instance.interfaces()

        mock_table.assert_called_once_with(test_data)
        self.assertEqual(result, "Mocked Table")

    @patch("switchmap.dashboard.table.interfaces.table")
    def test_interfaces_with_empty_data(self, mock_table):
        """
        Test the interfaces method with empty data.

        Verify that the method does not call the `table` function 
        and returns None.
        """
        test_data = {}
        search_instance = search.Search(test_data)
        result = search_instance.interfaces()

        mock_table.assert_not_called()
        self.assertIsNone(result)

    @patch("switchmap.dashboard.table.interfaces.table")
    def test_interfaces_with_none_data(self, mock_table):
        """
        Test the interfaces method with None as data.

        Verify that the method does not call the `table` function 
        and returns None.
        """
        test_data = None
        search_instance = search.Search(test_data)
        result = search_instance.interfaces()

        mock_table.assert_not_called()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
