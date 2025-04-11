#!/usr/bin/env python3
"""Test the rows module.

This module contains unit tests for the functions in the `rows.py` file.
The tests ensure that the following functions correctly convert database rows to tuples:

- device()
- root()
- event()
- l1interface()
- mac()
- macip()
- macport()
- oui()
- vlan()
- vlanport()
- zone()
- ip()
- ipport()

Additionally, edge cases where the input is None are tested to ensure that each function properly raises exceptions when provided with invalid input.

The tests verify the following:
- Correct tuple conversion for each function.
- Correct tuple length and data type.
- Correct value in the tuple for each entry in the row
- Handling of invalid (None) inputs with appropriate exceptions.
"""

import os
import sys

import unittest
from switchmap.server.db.misc import rows
from switchmap.server.db.models import (
    Device,
    Event,
    Ip,
    IpPort,
    L1Interface,
    Mac,
    MacIp,
    MacPort,
    Oui,
    Root,
    Vlan,
    VlanPort,
    Zone,
)
from switchmap.server.db import SCOPED_SESSION
from tests.testlib_ import setup
from tests.testlib_ import db

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
        """This script is not installed in the "{0}" directory. Please fix.""".format(
            _EXPECTED
        )
    )
    sys.exit(2)


class TestRowsMethods(unittest.TestCase):
    """Test suite for functions in rows.py."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment before running tests."""
        # Load the configuration
        cls.config = setup.config()
        cls.config.save()
        # Drop tables
        cls.database = db.Database()
        cls.database.drop()
        cls.database.create()
        # Populate the database
        db.populate()
        cls.session = SCOPED_SESSION()

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after tests."""
        if cls.session:
            cls.session.close()
        cls.database.drop()
        cls.config.cleanup()

    # ----------------------------------------------------------------------
    # Standard conversion tests
    # ----------------------------------------------------------------------

    def test_device(self):
        """Test the device() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 12
        when given a Device row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_device",
            "idx_zone",
            "sys_name",
            "hostname",
            "name",
            "sys_description",
            "sys_objectid",
            "sys_uptime",
            "last_polled",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Device).first()
        result = rows.device(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 12)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_root(self):
        """Test the root() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a Root row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_root",
            "idx_event",
            "name",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Root).first()
        result = rows.root(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_event(self):
        """Test the event() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given an Event row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_event",
            "name",
            "epoch_utc",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Event).first()
        result = rows.event(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_l1interface(self):
        """Test the l1interface() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 25
        when given a L1Interface row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_l1interface",
            "idx_device",
            "ifindex",
            "duplex",
            "ethernet",
            "nativevlan",
            "trunk",
            "ifspeed",
            "iftype",
            "ifalias",
            "ifdescr",
            "ifname",
            "ifadminstatus",
            "ifoperstatus",
            "ts_idle",
            "cdpcachedeviceid",
            "cdpcachedeviceport",
            "cdpcacheplatform",
            "lldpremportdesc",
            "lldpremsyscapenabled",
            "lldpremsysdesc",
            "lldpremsysname",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(L1Interface).first()
        result = rows.l1interface(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 25)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_mac(self):
        """Test the mac() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 7
        when given a Mac row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_mac",
            "idx_oui",
            "idx_zone",
            "mac",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Mac).first()
        result = rows.mac(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 7)

        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_macip(self):
        """Test the macip() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a MacIp row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_macip",
            "idx_ip",
            "idx_mac",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(MacIp).first()
        result = rows.macip(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_macport(self):
        """Test the macport() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a MacPort row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_macport",
            "idx_l1interface",
            "idx_mac",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(MacPort).first()
        result = rows.macport(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_oui(self):
        """Test the oui() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a Oui row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_oui",
            "oui",
            "organization",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Oui).first()
        result = rows.oui(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_vlan(self):
        """Test the vlan() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 8
        when given a Vlan row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_vlan",
            "idx_device",
            "vlan",
            "name",
            "state",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Vlan).first()
        result = rows.vlan(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 8)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_vlanport(self):
        """Test the vlanport() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a VlanPort row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_vlanport",
            "idx_l1interface",
            "idx_vlan",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(VlanPort).first()
        result = rows.vlanport(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_zone(self):
        """Test the zone() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 7
        when given a Zone row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_zone",
            "idx_event",
            "name",
            "notes",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Zone).first()
        result = rows.zone(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 7)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_ip(self):
        """Test the ip() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 8
        when given a Ip row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_ip",
            "idx_zone",
            "address",
            "version",
            "hostname",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(Ip).first()
        result = rows.ip(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 8)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    def test_ipport(self):
        """Test the ipport() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a IpPort row from the database.
        """
        # List of row attributes to match with the tuple values
        row_attributes = [
            "idx_ipport",
            "idx_l1interface",
            "idx_ip",
            "enabled",
            "ts_modified",
            "ts_created",
        ]
        row = self.session.query(IpPort).first()
        result = rows.ipport(row)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        # Check each values in the tuple
        for i, attr in enumerate(row_attributes):
            row_value = getattr(row, attr)

            # Decode byte string if necessary
            if isinstance(row_value, bytes):
                row_value = row_value.decode()

            self.assertEqual(
                row_value,
                result[i],
                f"Mismatch at index {i} for attribute '{attr}'",
            )

    # ----------------------------------------------------------------------
    # --- Edge case: None input tests ---
    # ----------------------------------------------------------------------

    def test_device_edge_none(self):
        """Edge Case: Test device() with None input."""
        with self.assertRaises(Exception):
            rows.device(None)

    def test_root_edge_none(self):
        """Edge Case: Test root() with None input."""
        with self.assertRaises(Exception):
            rows.root(None)

    def test_event_edge_none(self):
        """Edge Case: Test event() with None input."""
        with self.assertRaises(Exception):
            rows.event(None)

    def test_l1interface_edge_none(self):
        """Edge Case: Test l1interface() with None input."""
        with self.assertRaises(Exception):
            rows.l1interface(None)

    def test_mac_edge_none(self):
        """Edge Case: Test mac() with None input."""
        with self.assertRaises(Exception):
            rows.mac(None)

    def test_macip_edge_none(self):
        """Edge Case: Test macip() with None input."""
        with self.assertRaises(Exception):
            rows.macip(None)

    def test_macport_edge_none(self):
        """Edge Case: Test macport() with None input."""
        with self.assertRaises(Exception):
            rows.macport(None)

    def test_oui_edge_none(self):
        """Edge Case: Test oui() with None input."""
        with self.assertRaises(Exception):
            rows.oui(None)

    def test_vlan_edge_none(self):
        """Edge Case: Test vlan() with None input."""
        with self.assertRaises(Exception):
            rows.vlan(None)

    def test_vlanport_edge_none(self):
        """Edge Case: Test vlanport() with None input."""
        with self.assertRaises(Exception):
            rows.vlanport(None)

    def test_zone_edge_none(self):
        """Edge Case: Test zone() with None input."""
        with self.assertRaises(Exception):
            rows.zone(None)

    def test_ip_edge_none(self):
        """Edge Case: Test ip() with None input."""
        with self.assertRaises(Exception):
            rows.ip(None)

    def test_ipport_edge_none(self):
        """Edge Case: Test ipport() with None input."""
        with self.assertRaises(Exception):
            rows.ipport(None)


if __name__ == "__main__":
    unittest.main()
