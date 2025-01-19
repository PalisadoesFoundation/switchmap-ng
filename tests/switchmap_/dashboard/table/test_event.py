"""Unit tests for the event table functionalities.

This module contains tests for the `table`, `EventTable`, and `EventsRow`
classes from the `switchmap.dashboard.table.events` module.
"""

import os
import sys
import unittest
from switchmap.dashboard.table.events import table, EventTable
from switchmap.dashboard import EventMeta
from switchmap import SITE_PREFIX

EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}" "dashboard{0}table".format(os.sep)
)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)


class TestEventTable(unittest.TestCase):
    """Test cases for the event table functionalities."""

    def test_table_with_valid_events(self):
        """Test the table function with a list of EventMeta objects."""
        # Arrange: Create a list of EventMeta objects
        events = [
            EventMeta(date="2025-01-01", idx_root=1),
            EventMeta(date="2025-01-02", idx_root=2),
            EventMeta(date="2025-01-03", idx_root=3),
            EventMeta(date="2025-01-04", idx_root=4),
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
            first_row.col0, f'<a href="{SITE_PREFIX}/4">2025-01-04</a>'
        )
        self.assertEqual(
            first_row.col1, f'<a href="{SITE_PREFIX}/3">2025-01-03</a>'
        )
        self.assertEqual(
            first_row.col2, f'<a href="{SITE_PREFIX}/2">2025-01-02</a>'
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
        events = [EventMeta(date="2025-01-01", idx_root=1)]
        result = table(events)

        # Update expectation to verify the EventTable behavior
        self.assertIsInstance(result, EventTable)
        self.assertEqual(
            len(result.items), 1
        )  # Ensure the single event is processed

        first_row = result.items[0]
        self.assertEqual(
            first_row.col0, f'<a href="{SITE_PREFIX}/1">2025-01-01</a>'
        )


if __name__ == "__main__":
    unittest.main()
