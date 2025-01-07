import unittest
from unittest.mock import MagicMock
from flask_table import Table
from switchmap.dashboard.table.events import _RawCol, EventTable, EventsRow, table


class TestEventTable(unittest.TestCase):
    def test_raw_col_td_format(self):
        """Test the _RawCol td_format method."""
        raw_col = _RawCol("")
        self.assertEqual(raw_col.td_format("<b>test</b>"), "<b>test</b>")

    def test_event_row_initialization(self):
        """Test initialization of EventsRow."""
        row_data = ["data0", "data1", "data2", "data3", "data4", "data5"]
        row = EventsRow(row_data)
        self.assertEqual(row.col0, "data0")
        self.assertEqual(row.col5, "data5")

    def test_event_table_creation(self):
        """Test creation of EventTable with rows."""
        row_data = [["data0", "data1", "data2", "data3", "data4", "data5"]]
        rows = [EventsRow(data) for data in row_data]
        table = EventTable(rows)
        self.assertIsInstance(table, Table)
        self.assertEqual(len(table.items), 1)

    def test_table_function_no_events(self):
        """Test table function with no events."""
        events = []
        result = table(events)
        self.assertFalse(result)

    def test_table_function_with_events(self):
        """Test table function with mock events."""
        # Mock the general.padded_list_of_lists function
        from switchmap.core import general
        general.padded_list_of_lists = MagicMock(return_value=[
            ["<a href='test_url'>2025-01-01</a>", "", "", "", "", ""]
        ])

        # Mock events data
        class MockEvent:
            def __init__(self, idx_root, date):
                self.idx_root = idx_root
                self.date = date

        events = [
            MockEvent("event1", "2025-01-02"),
            MockEvent("event2", "2025-01-01"),
        ]

        # Call the table function
        result = table(events)
        self.assertIsInstance(result, Table)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].col0, "<a href='test_url'>2025-01-01</a>")

    def test_table_function_handles_empty_rows(self):
        """Test table function handles empty rows."""
        # Mock events
        events = []
        result = table(events)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
