#!/usr/bin/env python3
"""Test the Search class."""

import os
import sys
import unittest
import json
from unittest.mock import patch

# Add the project root directory to sys.path
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, os.pardir
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the module to test
from switchmap.dashboard.table import search
from switchmap.dashboard.table import interfaces as interfaces_


class TestSearch(unittest.TestCase):
    """Unit tests for the Search class."""

    def setUp(self):
        """Set up test data for each test case."""
        # Load realistic interface data from the JSON file
        test_data_path = os.path.join(
            ROOT_DIR, "tests/testdata_/device-01.json"
        )
        with open(test_data_path) as file:
            self.valid_data = json.load(file)

        # Extract l1interfaces data for testing
        self.valid_data["interfaces"] = [
            {
                "ifname": iface["ifname"],
                "status": "up" if iface["ifoperstatus"] == 1 else "down",
            }
            for iface in self.valid_data.get("l1interfaces", [])
        ]
        self.empty_data = {}
        self.none_data = None

    def test_interfaces_with_empty_data(self):
        """Test interfaces method with empty data."""
        search_instance = search.Search(self.empty_data)
        result = search_instance.interfaces()
        self.assertIsNone(result, "Expected None for empty data")

    def test_interfaces_with_none_data(self):
        """Test interfaces method with None data."""
        search_instance = search.Search(self.none_data)
        result = search_instance.interfaces()
        self.assertIsNone(result, "Expected None for None data")

    def test_interfaces_with_valid_data(self):
        """Test interfaces method with valid data."""
        original_table_function = interfaces_.table

        def mock_table(data):
            """Mock the table generation function.

            Args:
                data (dict): The data containing interface details.

            Returns:
                str: A string containing the generated HTML table.
            """
            rows = "".join(
                f"<tr><td>{iface['ifname']}</td><td>{iface['status']}</td></tr>"
                for iface in data["interfaces"]
            )
            return f"<table>{rows}</table>"

        interfaces_.table = mock_table
        search_instance = search.Search(self.valid_data)
        result = search_instance.interfaces()
        interfaces_.table = original_table_function

        # Build the expected HTML dynamically
        expected_rows = "".join(
            f"<tr><td>{iface['ifname']}</td><td>{iface['status']}</td></tr>"
            for iface in self.valid_data["interfaces"]
        )
        expected_html = f"<table>{expected_rows}</table>"

        self.assertEqual(
            result,
            expected_html,
            "Generated HTML does not match expected output",
        )


if __name__ == "__main__":
    unittest.main()
