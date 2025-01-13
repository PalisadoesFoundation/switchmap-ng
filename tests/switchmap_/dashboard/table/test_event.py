"""Unit tests for the event table functionalities.

This module contains tests for the `table`, `EventTable`, and `EventsRow`
classes from the `switchmap.dashboard.table.events` module.
"""

import unittest
from switchmap.dashboard.table.events import table, EventTable, EventsRow
from switchmap.dashboard import EventMeta
from switchmap import SITE_PREFIX


class TestEventTable(unittest.TestCase):
    """Test cases for the event table functionalities."""

    def test_table_with_valid_events(self):
        """Test the table function with a list of EventMeta objects."""
        # Arrange: Create a list of EventMeta objects
        events = [
            EventMeta(date="2025-01-01", idx_root="event1"),
            EventMeta(date="2025-01-02", idx_root="event2"),
            EventMeta(date="2025-01-03", idx_root="event3"),
            EventMeta(date="2025-01-04", idx_root="event4"),
        ]
        # Act: Call the table function
        result = table(events)
        # Assert: Verify the EventTable output
        self.assertIsInstance(result, EventTable)
        self.assertEqual(
            len(result.items), 1
        )  # Should have one row (6 columns per row)
        # Verify specific values in the first row
        first_row = result.items[0]
        self.assertEqual(
            first_row.col0, f'<a href="{SITE_PREFIX}/event4">2025-01-04</a>'
        )
        self.assertEqual(
            first_row.col1, f'<a href="{SITE_PREFIX}/event3">2025-01-03</a>'
        )
        self.assertEqual(
            first_row.col2, f'<a href="{SITE_PREFIX}/event2">2025-01-02</a>'
        )
        self.assertEqual(first_row.col3, "")
        self.assertEqual(first_row.col4, "")
        self.assertEqual(first_row.col5, "")

    def test_table_with_empty_events(self):
        """Test the table function with an empty list of events."""
        # Arrange: Create an empty list of events
        events = []
        # Act: Call the table function
        result = table(events)
        # Assert: Verify the result is False (no rows)
        self.assertFalse(result)

    def test_table_with_single_event(self):
        """Test the table function with a single event."""
        events = [EventMeta(date="2025-01-01", idx_root="event1")]
        result = table(events)

        # Update expectation to verify the EventTable behavior
        self.assertIsInstance(result, EventTable)
        self.assertEqual(
            len(result.items), 1
        )  # Ensure the single event is processed

        first_row = result.items[0]
        self.assertEqual(
            first_row.col0, f'<a href="{SITE_PREFIX}/event1">2025-01-01</a>'
        )


if __name__ == "__main__":
    unittest.main()
