#!/usr/bin/env python3
"""Test the Device class."""
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
from switchmap.dashboard.table import device
from switchmap.dashboard.table import interfaces as interfaces_
from switchmap.dashboard.table import system as system_


class TestDevice(unittest.TestCase):
    """Unit tests for the Device class."""

    def setUp(self):
        """Set up test data for each test case."""
        # Load realistic interface data from the JSON file
        test_data_path = os.path.join(
            ROOT_DIR, "tests/testdata_/device-01.json"
        )
        with open(test_data_path) as file:
            self.valid_data = json.load(file)

        # Process interface data for testing
        for iface in self.valid_data.get("l1interfaces", []):
            iface["status"] = "up" if iface["ifoperstatus"] == 1 else "down"
            iface["admin"] = (
                "enabled" if iface["ifadminstatus"] == 1 else "disabled"
            )

        self.empty_data = {}
        self.none_data = None

    def test_interfaces_with_empty_data(self):
        """Test the interfaces method with empty data."""
        device_instance = device.Device(self.empty_data)
        result = device_instance.interfaces()
        self.assertIsNone(result, "Expected None for empty data")

    def test_interfaces_with_none_data(self):
        """Test the interfaces method with None as data."""
        device_instance = device.Device({"l1interfaces": None})
        result = device_instance.interfaces()
        self.assertIsNone(result, "Expected None for None data")

    def test_interfaces_with_valid_data(self):
        """Test the interfaces method with valid data."""
        original_table_function = interfaces_.table

        def mock_table(data):
            """Mock the table generation function.

            Args:
                data (dict): The data containing interface details.

            Returns:
                str: A string containing the generated HTML table.
            """
            rows = "".join(
                f"<tr><td>{iface['ifname']}</td>"
                f"<td>{iface['status']}</td>"
                f"<td>{iface['admin']}</td></tr>"
                for iface in data
            )
            return f"<table>{rows}</table>"

        interfaces_.table = mock_table
        device_instance = device.Device(self.valid_data)
        result = device_instance.interfaces()
        interfaces_.table = original_table_function

        # Build the expected HTML dynamically
        expected_rows = "".join(
            f"<tr><td>{iface['ifname']}</td>"
            f"<td>{iface['status']}</td>"
            f"<td>{iface['admin']}</td></tr>"
            for iface in self.valid_data["l1interfaces"]
        )
        expected_html = "<table>"
        expected_html += f"{expected_rows}</table>"

        self.assertEqual(
            result,
            expected_html,
            "Generated HTML does not match expected output",
        )

    def test_system_with_empty_data(self):
        """Test the system method with empty data."""
        device_instance = device.Device(self.empty_data)
        result = device_instance.system()
        self.assertIsNone(result, "Expected None for empty data")

    def test_system_with_none_data(self):
        """Test the system method with None as data."""
        device_instance = device.Device(None)
        result = device_instance.system()
        self.assertIsNone(result, "Expected None for None data")


def test_interfaces_with_valid_data(self):
    """Test the interfaces method with valid data."""
    original_table_function = interfaces_.table

    def mock_table(data):
        """Mock the table generation function.

        Args:
            data (dict): The data containing interface details.

        Returns:
            str: A string containing the generated HTML table.
        """
        rows = "".join(
            f"<tr>"
            f"<td>{iface['ifname']}</td>"
            f"<td>{iface['status']}</td>"
            f"<td>{iface['admin']}</td>"
            f"</tr>"
            for iface in data
        )
        return f"<table>{rows}</table>"

    interfaces_.table = mock_table
    device_instance = device.Device(self.valid_data)
    result = device_instance.interfaces()
    interfaces_.table = original_table_function

    # Build the expected HTML dynamically
    expected_rows = "".join(
        f"<tr>"
        f"<td>{iface['ifname']}</td>"
        f"<td>{iface['status']}</td>"
        f"<td>{iface['admin']}</td>"
        f"</tr>"
        for iface in self.valid_data["l1interfaces"]
    )
    expected_html = f"<table>{expected_rows}</table>"

    self.assertEqual(
        result,
        expected_html,
        "Generated HTML does not match expected output",
    )


if __name__ == "__main__":
    unittest.main()
