#!/usr/bin/env python3
"""Test the topology module."""

import unittest
from unittest.mock import patch, MagicMock
from switchmap.dashboard.table.system import (
    _RawCol,
    SystemTable,
    SystemRow,
    table,
)
from switchmap.dashboard.data.system import System


class TestRawCol(unittest.TestCase):
    """Unit tests for _RawCol."""

    def test_td_format(self):
        """Test td_format method."""
        content = "<b>Unescaped Content</b>"
        col = _RawCol("Test")
        self.assertEqual(col.td_format(content), content)


class TestSystemTable(unittest.TestCase):
    """Unit tests for SystemTable."""

    def test_initialization(self):
        """Test table initialization."""
        items = []  # Provide mock or empty items for initialization
        table = SystemTable(items)
        self.assertEqual(table.parameter.name, "Parameter")
        self.assertEqual(table.value.name, "Value")
        self.assertIn("tblHead", table.thead_classes)
        self.assertIn("table", table.classes)


class TestSystemRow(unittest.TestCase):
    """Unit tests for SystemRow."""

    def test_initialization(self):
        """Test row initialization."""
        row_data = {
            "parameter": "Test Parameter",
            "value": "Test Value",
        }  # Adjust structure
        row = SystemRow(row_data)
        self.assertEqual(row.parameter, "Test Parameter")
        self.assertEqual(row.value, "Test Value")

    def test_invalid_row_data_length(self):
        """Test row initialization with invalid data length."""
        row_data = {"parameter": "Test Parameter"}  # Missing "value"
        with self.assertRaises(ValueError):
            SystemRow(
                row_data
            )  # Expecting a ValueError due to missing "value"

    def test_none_values_in_row_data(self):
        """Test row initialization with None values."""
        row_data = {
            "parameter": None,
            "value": "Test Value",
        }  # "parameter" is None
        with self.assertRaises(ValueError):
            SystemRow(row_data)  # Expecting a ValueError due to None value

    def test_invalid_type_in_row_data(self):
        """Test row initialization with invalid type."""
        row_data = {
            "parameter": "Test Parameter",
            "value": 12345,
        }  # "value" should be a string
        with self.assertRaises(ValueError):
            SystemRow(row_data)  # Expecting a ValueError due to invalid type

    def test_empty_row_data(self):
        """Test row initialization with empty row data."""
        row_data = {}
        with self.assertRaises(ValueError):
            SystemRow(row_data)  # Expecting a ValueError due to missing data


class TestTableFunction(unittest.TestCase):
    """Unit tests for the table function."""

    @patch("switchmap.dashboard.table.system.System")
    def test_table_with_rows(self, mock_system):
        """Test table function with valid rows."""
        # Mock data
        mock_rows = [
            MagicMock(parameter="Parameter1", value="Value1"),
            MagicMock(parameter="Parameter2", value="Value2"),
        ]
        mock_system_instance = MagicMock()
        mock_system_instance.rows.return_value = mock_rows
        mock_system.return_value = mock_system_instance

        # Call the function
        result = table({"key": "value"})

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(len(result.items), len(mock_rows))
        self.assertEqual(result.items[0].parameter, "Parameter1")
        self.assertEqual(result.items[0].value, "Value1")

    @patch("switchmap.dashboard.table.system.System")
    def test_table_without_rows(self, mock_system):
        """Test table function with no rows."""
        # Mock data
        mock_system_instance = MagicMock()
        mock_system_instance.rows.return_value = []
        mock_system.return_value = mock_system_instance

        # Call the function
        result = table({"key": "value"})

        # Assertions
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
