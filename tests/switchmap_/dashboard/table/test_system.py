#!/usr/bin/env python3
"""Test the topology module."""

import unittest
from unittest.mock import patch, MagicMock
from switchmap.dashboard.table.system import (
    _RawCol,
    SystemTable,
    SystemRow,
    table
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
        table = SystemTable()
        self.assertEqual(table.parameter.name, "Parameter")
        self.assertEqual(table.value.name, "Value")
        self.assertIn("tblHead", table.thead_classes)
        self.assertIn("table", table.classes)


class TestSystemRow(unittest.TestCase):
    """Unit tests for SystemRow."""

    def test_initialization(self):
        """Test row initialization."""
        row_data = ["Test Parameter", "Test Value"]
        row = SystemRow(row_data)
        self.assertEqual(row.parameter, "Test Parameter")
        self.assertEqual(row.value, "Test Value")


class TestTableFunction(unittest.TestCase):
    """Unit tests for the table function."""

    @patch("switchmap.dashboard.table.system.System")
    def test_table_with_rows(self, mock_system):
        """Test table function with valid rows."""
        # Mock data
        mock_rows = [["Parameter1", "Value1"], ["Parameter2", "Value2"]]
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
