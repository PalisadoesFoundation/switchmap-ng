#!/usr/bin/env python3
"""Additional test cases for OUI database update functionality."""

import os
import sys
import unittest
import tempfile
import pandas as pd

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

# Application imports
from tests.testlib_ import setup
from tests.testlib_ import db

# Import the module to test
from switchmap.server.db.misc import oui as testimport
from switchmap.server.db.table import oui as oui_table
from switchmap.server.db.models import Oui
from switchmap.server.db import SCOPED_SESSION


class TestOuiUpdate(unittest.TestCase):
    """Extended test suite for OUI database update functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment before running tests."""
        # Load the configuration
        config = setup.config()
        config.save()

        # Drop and recreate database tables
        database = db.Database()
        database.drop()
        database.create()

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after tests."""
        # Drop database tables
        database = db.Database()
        database.drop()

        # Cleanup configuration
        CONFIG = setup.config()
        CONFIG.cleanup()

    def setUp(self):
        """Prepare for each test case."""
        # Clear existing OUI data before each test
        SCOPED_SESSION.query(Oui).delete()
        SCOPED_SESSION.commit()

    def _create_test_oui_file(self, data):
        """Create a temporary CSV file with OUI data.

        Args:
            data (list): List of tuples containing OUI and organization

        Returns:
            str: Path to the temporary CSV file
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as temp_file:
            # Write CSV header
            temp_file.write("oui:organization\n")

            # Write data rows
            for oui, org in data:
                temp_file.write(f"{oui}:{org}\n")

        return temp_file.name

    def test_update_db_oui_empty_file(self):
        """Test handling of an empty CSV file."""
        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as temp_file:
            pass  # Create an empty file without writing anything

        try:
            # Call the function and expect a ValueError
            with self.assertRaises(ValueError) as context:
                testimport.update_db_oui(temp_file.name)

            # Verify the exception message
            self.assertEqual(str(context.exception), "The CSV file is empty")

        finally:
            # Remove temporary file
            os.unlink(temp_file.name)

    def test_update_db_oui_with_duplicates(self):
        """Test handling of input files with duplicate OUIs."""
        # Prepare test data with duplicates
        duplicate_data = [
            ("001122", "Organization A"),
            ("001122", "Organization B"),  # Duplicate OUI
        ]
        temp_file_path = self._create_test_oui_file(duplicate_data)

        try:
            # Call the function and expect a ValueError
            with self.assertRaises(ValueError) as context:
                testimport.update_db_oui(temp_file_path)

            self.assertEqual(
                str(context.exception),
                "The input file contains duplicate OUIs.",
            )

        finally:
            # Remove temporary file
            os.unlink(temp_file_path)

    def test_update_db_oui_existing_database(self):
        """Test updating OUI records in a non-empty database."""
        # First, add an initial record
        initial_data = [("001122", "Original Organization")]
        initial_file_path = self._create_test_oui_file(initial_data)
        testimport.update_db_oui(initial_file_path)
        os.unlink(initial_file_path)

        # Prepare updated data
        updated_data = [
            ("001122", "Updated Organization"),  # Same OUI, different org
            ("334455", "New Organization"),  # New OUI
        ]
        updated_file_path = self._create_test_oui_file(updated_data)

        try:
            # Call the function with updated records
            testimport.update_db_oui(updated_file_path)

            # Verify the records
            oui_records = SCOPED_SESSION.query(Oui).order_by(Oui.oui).all()
            self.assertEqual(len(oui_records), 3)

            # Check first record (updated)
            self.assertEqual(oui_records[0].oui, b"001122")
            self.assertEqual(
                oui_records[0].organization, b"Updated Organization"
            )

            # Check second record (new)
            self.assertEqual(oui_records[1].oui, b"334455")
            self.assertEqual(oui_records[1].organization, b"New Organization")

        finally:
            # Remove temporary file
            os.unlink(updated_file_path)
            # Ensure session is clean
            SCOPED_SESSION.rollback()

    def test_update_db_oui_malformed_data(self):
        """Test handling of malformed or inconsistent OUI data."""
        # Prepare malformed data (incorrect delimiter)
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as temp_file:
            # Write malformed data
            temp_file.write("oui,organization\n")  # Different delimiter
            temp_file.write("001122,Test Organization\n")

        try:
            # This should raise a pandas parsing error
            with self.assertRaises(ValueError):
                testimport.update_db_oui(temp_file.name)

        finally:
            # Remove temporary file
            os.unlink(temp_file.name)
            # Ensure session is clean
            SCOPED_SESSION.rollback()


if __name__ == "__main__":
    # Run the unit tests
    unittest.main()
