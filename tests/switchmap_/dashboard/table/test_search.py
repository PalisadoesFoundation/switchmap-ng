#!/usr/bin/env python3
"""Test the Search class."""

import os
import sys
import unittest
from flask_table import Table
from unittest.mock import patch

# Add the project root directory to sys.path
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../")
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
        self.valid_data = {
            "interfaces": [
                {"id": 1, "name": "eth0", "status": "up"},
                {"id": 2, "name": "eth1", "status": "down"},
            ]
        }
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
            """Mock the table generation function."""
            return f"<table>{''.join(f'<tr><td>{iface['name']}</td><td>{iface['status']}</td></tr>' for iface in data['interfaces'])}</table>"

        interfaces_.table = mock_table
        search_instance = search.Search(self.valid_data)
        result = search_instance.interfaces()
        interfaces_.table = original_table_function

        expected_html = (
            "<table>"
            "<tr><td>eth0</td><td>up</td></tr>"
            "<tr><td>eth1</td><td>down</td></tr>"
            "</table>"
        )
        self.assertEqual(
            result,
            expected_html,
            "Generated HTML does not match expected output",
        )


if __name__ == "__main__":
    unittest.main()
