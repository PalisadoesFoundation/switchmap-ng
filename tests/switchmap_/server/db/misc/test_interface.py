#!/usr/bin/env python3
"""Test the interface module."""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(
                            os.path.join(
                                os.path.abspath(
                                    os.path.join(EXEC_DIR, os.pardir)
                                ),
                                os.pardir,
                            )
                        ),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)

_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}misc""".format(
    os.sep
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

# Import test dependencies
from tests.testlib_ import setup
from tests.testlib_ import db
from tests.testlib_ import data

# Import modules to test
from switchmap.server.db.misc import interface as testimport
from switchmap.server.db.table import zone, event, device, l1interface


class TestInterface(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def setUp(self):
        """Execute these steps before each test."""
        # Create mock objects
        self.mock_rdevice = Mock()
        self.mock_rdevice.idx_zone = 1
        self.mock_rdevice.hostname = "test_device"
        self.mock_rdevice.idx_device = 1

        # Create mock zone
        self.mock_zone = Mock()
        self.mock_zone.idx_event = 2

        # Create mock event
        self.mock_event = Mock()

        # Create mock device
        self.mock_device = Mock()
        self.mock_device.idx_device = 1

        # Create mock interfaces
        self.mock_interfaces = [Mock()]
        self.mock_interfaces[0].idx_device = 1

    def tearDown(self):
        """Execute these steps after each test."""
        pass

    @patch("switchmap.server.db.table.zone.idx_exists")
    @patch("switchmap.server.db.table.event.idx_exists")
    @patch("switchmap.server.db.table.zone.zones")
    @patch("switchmap.server.db.table.device.exists")
    @patch("switchmap.server.db.table.l1interface.ifindexes")
    def test_interfaces_with_existing_zone_and_device(
        self,
        mock_ifindexes,
        mock_device_exists,
        mock_zones,
        mock_event_exists,
        mock_zone_exists,
    ):
        """Testing function interfaces with existing zone and device."""
        # Set up mocks
        mock_zone_exists.return_value = self.mock_zone
        mock_event_exists.return_value = self.mock_event
        mock_zones.return_value = [self.mock_zone]
        mock_device_exists.return_value = self.mock_device
        mock_ifindexes.return_value = self.mock_interfaces

        # Get interfaces
        result = testimport.interfaces(self.mock_rdevice)

        # Verify results
        self.assertEqual(result, self.mock_interfaces)
        mock_zone_exists.assert_called_once_with(self.mock_rdevice.idx_zone)
        mock_event_exists.assert_called_once_with(1)  # idx_event - 1
        mock_zones.assert_called_once_with(1)
        mock_device_exists.assert_called_once_with(
            self.mock_zone.idx_zone, self.mock_rdevice.hostname
        )
        mock_ifindexes.assert_called_once_with(self.mock_device.idx_device)

    @patch("switchmap.server.db.table.zone.idx_exists")
    def test_interfaces_with_nonexistent_zone(self, mock_zone_exists):
        """Testing function interfaces with non-existent zone."""
        # Set up mock
        mock_zone_exists.return_value = None

        # Get interfaces
        result = testimport.interfaces(self.mock_rdevice)

        # Verify results
        self.assertEqual(result, [])
        mock_zone_exists.assert_called_once_with(self.mock_rdevice.idx_zone)

    @patch("switchmap.server.db.table.zone.idx_exists")
    @patch("switchmap.server.db.table.event.idx_exists")
    @patch("switchmap.server.db.table.zone.zones")
    @patch("switchmap.server.db.table.device.exists")
    def test_interfaces_with_nonexistent_device(
        self,
        mock_device_exists,
        mock_zones,
        mock_event_exists,
        mock_zone_exists,
    ):
        """Testing function interfaces with non-existent device."""
        # Set up mocks
        mock_zone_exists.return_value = self.mock_zone
        mock_event_exists.return_value = self.mock_event
        mock_zones.return_value = [self.mock_zone]
        mock_device_exists.return_value = None

        # Get interfaces
        result = testimport.interfaces(self.mock_rdevice)

        # Verify results
        self.assertEqual(result, [])
        mock_device_exists.assert_called_once_with(
            self.mock_zone.idx_zone, self.mock_rdevice.hostname
        )

    @patch("switchmap.server.db.table.zone.idx_exists")
    @patch("switchmap.server.db.table.event.idx_exists")
    def test_interfaces_with_no_previous_event(
        self, mock_event_exists, mock_zone_exists
    ):
        """Testing function interfaces with no previous event."""
        # Set up mocks
        mock_zone_exists.return_value = self.mock_zone
        mock_event_exists.return_value = None

        # Get interfaces
        result = testimport.interfaces(self.mock_rdevice)

        # Verify results
        self.assertEqual(result, [])
        mock_event_exists.assert_called_once_with(1)  # idx_event - 1


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
