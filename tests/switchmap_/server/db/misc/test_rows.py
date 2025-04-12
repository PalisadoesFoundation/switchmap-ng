#!/usr/bin/env python3
"""Test the rows module.

This module contains unit tests for the functions in the `rows.py` file.
The tests ensure that the following functions correctly convert
database rows to tuples:

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

Additionally, edge cases where the input is None are tested to ensure that
each function properly raises AttributeErrors when provided with invalid input.

The tests verify the following:
- Correct tuple conversion for each function.
- Correct tuple length and data type.
- Correct value in the tuple for each entry in the row
- Handling of invalid (None) inputs with appropriate AttributeErrors.
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
        """This script is not installed in the
        "{0}" directory. Please fix.""".format(
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

    def compare_row_to_expected(self, row, expected_dict):
        """Compare the attributes of a row with expected values.

        Iterates through the `expected_dict`, comparing each value with the
        corresponding attribute of the `row` object, handling byte string
        normalization, and reporting mismatches using assertions.

        Args:
            row: The database row object.
            expected_dict: A dictionary of expected attribute values.

        Raises:
            AttributeError: If an attribute is missing in the row.
            AssertionError: If an attribute value does not match.

        Returns:
            None
        """
        for key, expected_value in expected_dict.items():
            actual_value = getattr(row, key)

            # Normalize byte strings
            if isinstance(actual_value, bytes):
                actual_value = actual_value.decode()
            if isinstance(expected_value, bytes):
                expected_value = expected_value.decode()

            with self.subTest(attribute=key):
                self.assertEqual(
                    actual_value,
                    expected_value,
                    f"Mismatch for attribute '{key}'",
                )

    def test_device(self):
        """Test the device() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 12
        when given a Device row from the database.
        """
        row = self.session.query(Device).first()
        self.assertIsNotNone(row, "No Device row found in the test database.")
        result = rows.device(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 12)

        self.compare_row_to_expected(row, result._asdict())

    def test_root(self):
        """Test the root() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a Root row from the database.
        """
        row = self.session.query(Root).first()
        self.assertIsNotNone(row, "No Root row found in the test database.")
        result = rows.root(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    def test_event(self):
        """Test the event() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given an Event row from the database.
        """
        row = self.session.query(Event).first()
        self.assertIsNotNone(row, "No Event row found in the test database.")
        result = rows.event(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    def test_l1interface(self):
        """Test the l1interface() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 25
        when given an L1Interface row from the database.
        """
        try:
            # Try to query the first row
            row = self.session.query(L1Interface).first()

            # If no row is found, manually insert data
            if row is None:
                # Insert a sample row into the L1Interface table
                row = L1Interface(
                    idx_device=1,
                    ifindex=1,
                    duplex=1,
                    ethernet=0,
                    nativevlan=1,
                    trunk=0,
                    ifspeed=1000,
                    iftype=1,
                    ifname="eth0".encode(),
                    ifalias="Alias0".encode(),
                    ifdescr="Interface Description".encode(),
                    ifadminstatus=1,
                    ifoperstatus=1,
                    ts_idle=0,
                    cdpcachedeviceid="some_device_id".encode(),
                    cdpcachedeviceport="some_port".encode(),
                    cdpcacheplatform="platform".encode(),
                    lldpremportdesc="port_desc".encode(),
                    lldpremsyscapenabled="enabled".encode(),
                    lldpremsysdesc="system_desc".encode(),
                    lldpremsysname="system_name".encode(),
                    enabled=1,
                )
                self.session.add(row)
                self.session.commit()

                row = self.session.query(L1Interface).first()

        except Exception as e:
            self.fail(
                f"Error while querying or inserting into L1Interface: {str(e)}"
            )

        # Proceed with the rest of the test
        self.assertIsNotNone(row, "No Event row found in the test database.")

        # Convert row to a tuple using the function under test
        result = rows.l1interface(row)

        # Validate the result
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 25)

        self.compare_row_to_expected(row, result._asdict())

    def test_mac(self):
        """Test the mac() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 7
        when given a Mac row from the database.
        """
        row = self.session.query(Mac).first()
        self.assertIsNotNone(row, "No Mac row found in the test database.")
        result = rows.mac(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 7)

        self.compare_row_to_expected(row, result._asdict())

    def test_macip(self):
        """Test the macip() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a MacIp row from the database.
        """
        row = self.session.query(MacIp).first()
        self.assertIsNotNone(row, "No MacIp row found in the test database.")
        result = rows.macip(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    def test_macport(self):
        """Test the macport() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a MacPort row from the database.
        """
        row = self.session.query(MacPort).first()
        self.assertIsNotNone(row, "No MacPort row found in the test database.")
        result = rows.macport(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    def test_oui(self):
        """Test the oui() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a Oui row from the database.
        """
        row = self.session.query(Oui).first()
        self.assertIsNotNone(row, "No Oui row found in the test database.")
        result = rows.oui(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    def test_vlan(self):
        """Test the vlan() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 8
        when given a Vlan row from the database.
        """
        row = self.session.query(Vlan).first()
        self.assertIsNotNone(row, "No Vlan row found in the test database.")
        result = rows.vlan(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 8)

        self.compare_row_to_expected(row, result._asdict())

    def test_vlanport(self):
        """Test the vlanport() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a VlanPort row from the database.
        """
        row = self.session.query(VlanPort).first()
        self.assertIsNotNone(row, "No VlanPort row found in the test database.")
        result = rows.vlanport(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    def test_zone(self):
        """Test the zone() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 7
        when given a Zone row from the database.
        """
        row = self.session.query(Zone).first()
        self.assertIsNotNone(row, "No Zone row found in the test database.")
        result = rows.zone(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 7)

        self.compare_row_to_expected(row, result._asdict())

    def test_ip(self):
        """Test the ip() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 8
        when given a Ip row from the database.
        """
        row = self.session.query(Ip).first()
        self.assertIsNotNone(row, "No Ip row found in the test database.")
        result = rows.ip(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 8)

        self.compare_row_to_expected(row, result._asdict())

    def test_ipport(self):
        """Test the ipport() function for correct tuple conversion.

        Verifies that the function returns a tuple of length 6
        when given a IpPort row from the database.
        """
        row = self.session.query(IpPort).first()
        self.assertIsNotNone(row, "No IpPort row found in the test database.")
        result = rows.ipport(row)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)

        self.compare_row_to_expected(row, result._asdict())

    # ----------------------------------------------------------------------
    # --- Edge case: None input tests ---
    # ----------------------------------------------------------------------

    def test_device_edge_none(self):
        """Edge Case: Test device() with None input."""
        with self.assertRaises(AttributeError):
            rows.device(None)

    def test_root_edge_none(self):
        """Edge Case: Test root() with None input."""
        with self.assertRaises(AttributeError):
            rows.root(None)

    def test_event_edge_none(self):
        """Edge Case: Test event() with None input."""
        with self.assertRaises(AttributeError):
            rows.event(None)

    def test_l1interface_edge_none(self):
        """Edge Case: Test l1interface() with None input."""
        with self.assertRaises(AttributeError):
            rows.l1interface(None)

    def test_mac_edge_none(self):
        """Edge Case: Test mac() with None input."""
        with self.assertRaises(AttributeError):
            rows.mac(None)

    def test_macip_edge_none(self):
        """Edge Case: Test macip() with None input."""
        with self.assertRaises(AttributeError):
            rows.macip(None)

    def test_macport_edge_none(self):
        """Edge Case: Test macport() with None input."""
        with self.assertRaises(AttributeError):
            rows.macport(None)

    def test_oui_edge_none(self):
        """Edge Case: Test oui() with None input."""
        with self.assertRaises(AttributeError):
            rows.oui(None)

    def test_vlan_edge_none(self):
        """Edge Case: Test vlan() with None input."""
        with self.assertRaises(AttributeError):
            rows.vlan(None)

    def test_vlanport_edge_none(self):
        """Edge Case: Test vlanport() with None input."""
        with self.assertRaises(AttributeError):
            rows.vlanport(None)

    def test_zone_edge_none(self):
        """Edge Case: Test zone() with None input."""
        with self.assertRaises(AttributeError):
            rows.zone(None)

    def test_ip_edge_none(self):
        """Edge Case: Test ip() with None input."""
        with self.assertRaises(AttributeError):
            rows.ip(None)

    def test_ipport_edge_none(self):
        """Edge Case: Test ipport() with None input."""
        with self.assertRaises(AttributeError):
            rows.ipport(None)


if __name__ == "__main__":
    unittest.main()
