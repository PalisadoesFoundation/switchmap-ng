#!/usr/bin/env python3
"""Test the switchmap-ng interface table module."""

# Standard imports
import unittest
from collections import namedtuple

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
        # Use _RawCol instead of Col
        self.column = _RawCol("testcol")

    def test_td_format(self):
        """Testing method td_format."""
        html_content = '<a href="#">Link</a>'
        result = self.column.td_format(html_content)
        self.assertEqual(
            Markup(result), Markup(html_content)
        )  # Compare as Markup objects

        # Testing with HTML content
        html_content = '<a href="#">Link</a>'
        result = self.column.td_format(html_content)
        self.assertEqual(result, html_content)  # No Markup wrapping

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

        # Create mock item with proper enabled/active methods
        class MockItem:
            def __init__(self, is_enabled, is_active):
                self._enabled = is_enabled
                self._active = is_active

            def enabled(self):
                return self._enabled

            def active(self):
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
        # Create sample row data
        self.row_data = [
            "Gi1/0/1",  # port
            "10",  # vlan
            "Active",  # state
            "5",  # days_inactive
            "1000",  # speed
            "full",  # duplex
            "Server Port",  # label
            "No",  # trunk
            "Switch-A",  # cdp
            "Switch-B",  # lldp
            "00:11:22:33:44:55",  # mac_address
            "Cisco",  # organization
            "192.168.1.1",  # ip_address
            "switch.local",  # hostname
        ]
        self.interface_row = InterfaceRow(self.row_data)

    def test___init__(self):
        """Testing function __init__."""
        # Test all attributes are properly set
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
        # Test active state
        self.interface_row.state = "Active"
        self.assertTrue(self.interface_row.active())

        # Test inactive state
        self.interface_row.state = "Inactive"
        self.assertFalse(self.interface_row.active())

        # Test other states
        self.interface_row.state = "Disabled"
        self.assertFalse(self.interface_row.active())

    def test_enabled(self):
        """Testing method enabled."""
        # Test enabled state
        self.interface_row.state = "Active"
        self.assertTrue(self.interface_row.enabled())

        # Test another enabled state
        self.interface_row.state = "Inactive"
        self.assertTrue(self.interface_row.enabled())

        # Test disabled state
        self.interface_row.state = "Disabled"
        self.assertFalse(self.interface_row.enabled())


class TestTable(unittest.TestCase):
    def setUp(self):
        class MockInterface:
            def __init__(self, data=None):
                self._interface = data or {}

            def row(self):
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
                    port=self._interface["port"],
                    vlan=self._interface["vlan"],
                    state=self._interface["state"],
                    days_inactive=self._interface["days_inactive"],
                    speed=self._interface["speed"],
                    duplex=self._interface["duplex"],
                    label=self._interface["label"],
                    trunk=self._interface["trunk"],
                    cdp=self._interface["cdp"],
                    lldp=self._interface["lldp"],
                    mac_address=self._interface["mac_address"],
                    organization=self._interface["organization"],
                    ip_address=self._interface["ip_address"],
                    hostname=self._interface["hostname"],
                )

        self.MockInterface = MockInterface

        def test_table_valid(self):
            """Testing function table with valid data."""
            # Create a mock interface instance with valid data
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
            mock_interface = self.MockInterface(interface_data)

            # Test with single interface
            result = table([mock_interface])
            self.assertIsInstance(result, InterfaceTable)
            self.assertEqual(len(result.items), 1)

            # Verify the row data
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

        def test_table_multiple_interfaces(self):
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

            mock_interface1 = self.MockInterface(interface_data1)
            mock_interface2 = self.MockInterface(interface_data2)

            result = table([mock_interface1, mock_interface2])
            self.assertIsInstance(result, InterfaceTable)
            self.assertEqual(len(result.items), 2)

            # Verify both rows
            self.assertEqual(result.items[0].port, "Gi1/0/1")
            self.assertEqual(result.items[1].port, "Gi1/0/2")
            self.assertEqual(result.items[0].state, "Active")
            self.assertEqual(result.items[1].state, "Inactive")


if __name__ == "__main__":
    # Make this test suite runnable
    unittest.main()
