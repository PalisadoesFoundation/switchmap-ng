#!/usr/bin/env python3
"""Test the switchmap-ng interface table module."""

# Standard imports
import unittest
from collections import namedtuple
from unittest.mock import patch

# PIP imports
from flask_table import Col
from markupsafe import Markup

# Switchmap-NG imports
from switchmap.dashboard.table.interfaces import (
    InterfaceTable,
    InterfaceRow,
    table,
    _RawCol,
)


class TestRawCol(unittest.TestCase):
    """Unittest for RawCol class."""

    def setUp(self):
        """Setup the environment prior to testing."""
        self.column = _RawCol("testcol")

    def test_td_format(self):
        """Testing method td_format."""
        html_content = '<a href="#">Link</a>'
        result = self.column.td_format(html_content)
        self.assertEqual(Markup(result), Markup(html_content))

        # Testing with None
        result = self.column.td_format(None)
        self.assertIsNone(result)


class TestInterfaceTable(unittest.TestCase):
    """Unittest for InterfaceTable class."""

    def setUp(self):
        """Setup the environment prior to testing."""
        self.table = InterfaceTable([])

    def test___init__(self):
        """Testing function __init__."""
        # Test column types
        self.assertIsInstance(self.table.port, Col)
        self.assertIsInstance(self.table.vlan, Col)
        self.assertIsInstance(self.table.state, Col)
        self.assertIsInstance(self.table.trunk, _RawCol)
        self.assertIsInstance(self.table.cdp, _RawCol)
        self.assertIsInstance(self.table.lldp, _RawCol)

        # Test column headers
        self.assertEqual(self.table.port.name, "Port")
        self.assertEqual(self.table.vlan.name, "VLAN")
        self.assertEqual(self.table.organization.name, "Manufacturer")

        # Test CSS class
        self.assertEqual(self.table.classes, ["table"])

    def test_get_tr_attrs(self):
        """Testing method get_tr_attrs."""

        class MockItem:
            """Mock item class for testing interface table row attributes.

            This class simulates interface items with enabled and active states
            for testing the get_tr_attrs method of InterfaceTable.
            """

            def __init__(self, is_enabled, is_active):
                """Initialize the mock item with enabled and active states.

                Args:
                    is_enabled (bool): The enabled state of the interface
                    is_active (bool): The active state of the interface
                """
                self._enabled = is_enabled
                self._active = is_active

            def enabled(self):
                """Return enabled status.

                Returns:
                    bool: True if interface is enabled, False otherwise
                """
                return self._enabled

            def active(self):
                """Return active status.

                Returns:
                    bool: True if interface is active, False otherwise
                """
                return self._active

        # Test cases
        item = MockItem(True, True)
        result = self.table.get_tr_attrs(item)
        self.assertEqual(result, {"class": "success"})

        # Test enabled but inactive port
        item = MockItem(True, False)
        result = self.table.get_tr_attrs(item)
        self.assertEqual(result, {"class": "info"})

        # Test disabled port
        item = MockItem(False, False)
        result = self.table.get_tr_attrs(item)
        self.assertEqual(result, {"class": "warning"})


class TestInterfaceRow(unittest.TestCase):
    """Unittest for InterfaceRow class."""

    def setUp(self):
        """Setup the environment prior to testing."""
        self.row_data = [
            "Gi1/0/1",
            "10",
            "Active",
            "5",
            "1000",
            "full",
            "Server Port",
            "No",
            "Switch-A",
            "Switch-B",
            "00:11:22:33:44:55",
            "Cisco",
            "192.168.1.1",
            "switch.local",
        ]
        self.interface_row = InterfaceRow(self.row_data)

    def test___init__(self):
        """Testing function __init__."""
        self.assertEqual(self.interface_row.port, "Gi1/0/1")
        self.assertEqual(self.interface_row.vlan, "10")
        self.assertEqual(self.interface_row.state, "Active")
        self.assertEqual(self.interface_row.days_inactive, "5")
        self.assertEqual(self.interface_row.speed, "1000")
        self.assertEqual(self.interface_row.duplex, "full")
        self.assertEqual(self.interface_row.label, "Server Port")
        self.assertEqual(self.interface_row.trunk, "No")
        self.assertEqual(self.interface_row.cdp, "Switch-A")
        self.assertEqual(self.interface_row.lldp, "Switch-B")
        self.assertEqual(self.interface_row.mac_address, "00:11:22:33:44:55")
        self.assertEqual(self.interface_row.organization, "Cisco")
        self.assertEqual(self.interface_row.ip_address, "192.168.1.1")
        self.assertEqual(self.interface_row.hostname, "switch.local")

    def test_active(self):
        """Testing method active."""
        self.interface_row.state = "Active"
        self.assertTrue(self.interface_row.active())

        self.interface_row.state = "Inactive"
        self.assertFalse(self.interface_row.active())

        self.interface_row.state = "Disabled"
        self.assertFalse(self.interface_row.active())

    def test_enabled(self):
        """Testing method enabled."""
        self.interface_row.state = "Active"
        self.assertTrue(self.interface_row.enabled())

        self.interface_row.state = "Inactive"
        self.assertTrue(self.interface_row.enabled())

        self.interface_row.state = "Disabled"
        self.assertFalse(self.interface_row.enabled())


class TestTable(unittest.TestCase):
    """Unittest for table function."""

    def setUp(self):
        """Setup the environment prior to testing."""

        class MockInterface:
            """Mock interface class for testing.

            This class simulates the Interface class behavior for testing purposes,
            providing mock implementations of get() and row() methods.
            """

            def __init__(self, data=None):
                """Initialize the mock interface with optional data.

                Args:
                    data (dict, optional): Dictionary containing interface data.
                        Defaults to None.
                """
                self._interface = data or {}

            def get(self, key, default=None):
                """Mock the get method to match the interface behavior.

                Args:
                    key (str): Dictionary key to retrieve
                    default (Any, optional): Default value if key not found.
                        Defaults to None.

                Returns:
                    Any: Value associated with key or default if not found
                """
                return self._interface.get(key, default)

            def row(self):
                """Return a row of interface data.

                Returns:
                    namedtuple: Row containing interface data, or None if no data
                """
                if not self._interface:
                    return None

                Row = namedtuple(
                    "Row",
                    [
                        "port",
                        "vlan",
                        "state",
                        "days_inactive",
                        "speed",
                        "duplex",
                        "label",
                        "trunk",
                        "cdp",
                        "lldp",
                        "mac_address",
                        "organization",
                        "ip_address",
                        "hostname",
                    ],
                )
                return Row(
                    port=self._interface.get("port"),
                    vlan=self._interface.get("vlan"),
                    state=self._interface.get("state"),
                    days_inactive=self._interface.get("days_inactive"),
                    speed=self._interface.get("speed"),
                    duplex=self._interface.get("duplex"),
                    label=self._interface.get("label"),
                    trunk=self._interface.get("trunk"),
                    cdp=self._interface.get("cdp"),
                    lldp=self._interface.get("lldp"),
                    mac_address=self._interface.get("mac_address"),
                    organization=self._interface.get("organization"),
                    ip_address=self._interface.get("ip_address"),
                    hostname=self._interface.get("hostname"),
                )

        self.MockInterface = MockInterface

    @patch("switchmap.dashboard.table.interfaces.Interface")
    def test_table_valid(self, mock_interface_class):
        """Testing function table with valid data."""
        interface_data = {
            "port": "Gi1/0/1",
            "vlan": "10",
            "state": "Active",
            "days_inactive": "0",
            "speed": "1000",
            "duplex": "full",
            "label": "Server1",
            "trunk": "No",
            "cdp": "Switch1",
            "lldp": "Switch1",
            "mac_address": "00:11:22:33:44:55",
            "organization": "Cisco",
            "ip_address": "192.168.1.1",
            "hostname": "switch1.example.com",
        }

        # Setup the mock to return our MockInterface instance
        mock_interface = self.MockInterface(interface_data)
        mock_interface_class.return_value = mock_interface

        result = table([interface_data])
        self.assertIsInstance(result, InterfaceTable)
        self.assertEqual(len(result.items), 1)

        row = result.items[0]
        self.assertEqual(row.port, "Gi1/0/1")
        self.assertEqual(row.vlan, "10")
        self.assertEqual(row.state, "Active")

    def test_table_empty(self):
        """Testing function table with empty data."""
        result = table([])
        self.assertIsNone(result)

    def test_table_none_row(self):
        """Testing function table with interface returning None row."""
        mock_interface = self.MockInterface(None)
        result = table([mock_interface])
        self.assertIsNone(result)

    @patch("switchmap.dashboard.table.interfaces.Interface")
    def test_table_multiple_interfaces(self, mock_interface_class):
        """Testing function table with multiple interfaces."""
        interface_data1 = {
            "port": "Gi1/0/1",
            "vlan": "10",
            "state": "Active",
            "days_inactive": "0",
            "speed": "1000",
            "duplex": "full",
            "label": "Server1",
            "trunk": "No",
            "cdp": "Switch1",
            "lldp": "Switch1",
            "mac_address": "00:11:22:33:44:55",
            "organization": "Cisco",
            "ip_address": "192.168.1.1",
            "hostname": "switch1.example.com",
        }

        interface_data2 = {
            "port": "Gi1/0/2",
            "vlan": "20",
            "state": "Inactive",
            "days_inactive": "5",
            "speed": "100",
            "duplex": "half",
            "label": "Server2",
            "trunk": "Yes",
            "cdp": "Switch2",
            "lldp": "Switch2",
            "mac_address": "00:11:22:33:44:66",
            "organization": "Cisco",
            "ip_address": "192.168.1.2",
            "hostname": "switch2.example.com",
        }

        # Create mock interfaces
        mock_interface1 = self.MockInterface(interface_data1)
        mock_interface2 = self.MockInterface(interface_data2)

        # Setup the mock to return our MockInterface instances in sequence
        mock_interface_class.side_effect = [mock_interface1, mock_interface2]

        result = table([interface_data1, interface_data2])
        self.assertIsInstance(result, InterfaceTable)
        self.assertEqual(len(result.items), 2)

        self.assertEqual(result.items[0].port, "Gi1/0/1")
        self.assertEqual(result.items[1].port, "Gi1/0/2")
        self.assertEqual(result.items[0].state, "Active")
        self.assertEqual(result.items[1].state, "Inactive")


if __name__ == "__main__":
    unittest.main()
