#!/usr/bin/env python3
"""Test the db module."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import select, update, delete

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
            )
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db\
""".format(
    os.sep
)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)

# Create the necessary configuration to load the module
from tests.testlib_ import setup

# CONFIG = setup.config()
# CONFIG.save()

# Import module to test
from switchmap.server.db import db as testimport
from switchmap.server.db import models


class TestDbSelect(unittest.TestCase):
    """Test db_select function."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        cls.CONFIG = setup.config()
        cls.CONFIG.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        cls.CONFIG.cleanup()

    def test_db_select_wrong_type(self):
        """Test db_select with wrong statement type."""
        wrong_statement = "SELECT * FROM table"

        with self.assertRaises(SystemExit):
            testimport.db_select(9001, wrong_statement)

    def test_db_select_exception(self):
        """Test db_select when database operation fails."""
        statement = select(models.Zone.idx_zone)

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.side_effect = Exception("DB error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_select(9002, statement)


class TestDbSelectRow(unittest.TestCase):
    """Test db_select_row function."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        cls.CONFIG = setup.config()
        cls.CONFIG.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        cls.CONFIG.cleanup()

    def test_db_select_row_wrong_type(self):
        """Test db_select_row with wrong statement type."""
        wrong_statement = "SELECT * FROM table"

        with self.assertRaises(SystemExit):
            testimport.db_select_row(9003, wrong_statement)

    def test_db_select_row_exception(self):
        """Test db_select_row when database operation fails."""
        statement = select(models.Zone)

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_scalars = MagicMock()
            mock_scalars.all.side_effect = Exception("DB error")
            mock_session.execute.return_value.scalars.return_value = (
                mock_scalars
            )
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_select_row(9004, statement)


class TestDbUpdate(unittest.TestCase):
    """Test db_update function."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        cls.CONFIG = setup.config()
        cls.CONFIG.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        cls.CONFIG.cleanup()

    def test_db_update_wrong_type(self):
        """Test db_update with wrong statement type."""
        wrong_statement = "UPDATE table SET column = value"

        with self.assertRaises(SystemExit):
            testimport.db_update(9005, wrong_statement)

    def test_db_update_execute_exception(self):
        """Test db_update when execute fails."""
        statement = (
            update(models.Zone)
            .where(models.Zone.idx_zone == 1)
            .values(name="test")
        )

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.side_effect = Exception("Execute error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_update(9006, statement)

    def test_db_update_commit_exception(self):
        """Test db_update when commit fails."""
        statement = (
            update(models.Zone)
            .where(models.Zone.idx_zone == 1)
            .values(name="test")
        )

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.return_value = None
            mock_session.commit.side_effect = Exception("Commit error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_update(9007, statement)

    def test_db_update_with_values(self):
        """Test db_update with values parameter."""
        statement = update(models.Zone)
        values = [{"idx_zone": 1, "name": "test"}]

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                result = testimport.db_update(9008, statement, values)
                self.assertTrue(result)
                mock_session.execute.assert_called_once_with(statement, values)


class TestDbDelete(unittest.TestCase):
    """Test db_delete function."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        cls.CONFIG = setup.config()
        cls.CONFIG.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        cls.CONFIG.cleanup()

    def test_db_delete_wrong_type(self):
        """Test db_delete with wrong statement type."""
        wrong_statement = "DELETE FROM table"

        with self.assertRaises(SystemExit):
            testimport.db_delete(1123, wrong_statement)

    def test_db_delete_execute_exception(self):
        """Test db_delete when execute fails."""
        statement = delete(models.Zone).where(models.Zone.idx_zone == 999)

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.side_effect = Exception("Delete error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_delete(1100, statement)

    def test_db_delete_commit_exception(self):
        """Test db_delete when commit fails."""
        statement = delete(models.Zone).where(models.Zone.idx_zone == 999)

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_result = MagicMock()
            mock_result.rowcount = 1
            mock_session.execute.return_value = mock_result
            mock_session.commit.side_effect = Exception("Commit error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_delete(1116, statement)


class TestDbDeleteRow(unittest.TestCase):
    """Test db_delete_row function."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        cls.CONFIG = setup.config()
        cls.CONFIG.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        cls.CONFIG.cleanup()

    def test_db_delete_row_wrong_type(self):
        """Test db_delete_row with wrong statement type."""
        wrong_statement = "DELETE FROM table"

        with self.assertRaises(SystemExit):
            testimport.db_delete_row(1094, wrong_statement)

    def test_db_delete_row_execute_exception(self):
        """Test db_delete_row when execute fails."""
        statement = delete(models.Zone).where(models.Zone.idx_zone == 999)

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_scalars = MagicMock()
            mock_scalars.all.side_effect = Exception("Execute error")
            execute_return = mock_session.execute.return_value
            execute_return.scalars.return_value = mock_scalars
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_delete_row(1093, statement)

    def test_db_delete_row_commit_exception(self):
        """Test db_delete_row when commit fails."""
        statement = delete(models.Zone).where(models.Zone.idx_zone == 999)

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = []
            execute_return = mock_session.execute.return_value
            execute_return.scalars.return_value = mock_scalars
            mock_session.commit.side_effect = Exception("Commit error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_delete_row(1119, statement)


class TestDbInsertRow(unittest.TestCase):
    """Test db_insert_row function."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        cls.CONFIG = setup.config()
        cls.CONFIG.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        cls.CONFIG.cleanup()

    def test_db_insert_row_execute_exception_die(self):
        """Test db_insert_row when execute fails and die=True."""
        mappings = [{"name": "test"}]

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.side_effect = Exception("Insert error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_insert_row(
                        1015, models.Zone, mappings, die=True
                    )

    def test_db_insert_row_execute_exception_no_die(self):
        """Test db_insert_row when execute fails and die=False."""
        mappings = [{"name": "test"}]

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.side_effect = Exception("Insert error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                result = testimport.db_insert_row(
                    1016, models.Zone, mappings, die=False
                )
                # Commit still succeeds, so result is True
                self.assertTrue(result)

    def test_db_insert_row_commit_exception_die(self):
        """Test db_insert_row when commit fails and die=True."""
        mappings = [{"name": "test"}]

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.return_value = None
            mock_session.commit.side_effect = Exception("Commit error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                with self.assertRaises(Exception):
                    testimport.db_insert_row(
                        1017, models.Zone, mappings, die=True
                    )

    def test_db_insert_row_commit_exception_no_die(self):
        """Test db_insert_row when commit fails and die=False."""
        mappings = [{"name": "test"}]

        with patch("switchmap.server.db.db.ENGINE") as mock_engine:
            mock_connection = MagicMock()
            mock_session = MagicMock()
            mock_session.execute.return_value = None
            mock_session.commit.side_effect = Exception("Commit error")
            mock_connection.__enter__.return_value = mock_connection
            mock_session.__enter__.return_value = mock_session
            mock_engine.connect.return_value = mock_connection

            patch_path = "switchmap.server.db.db.Session"
            with patch(patch_path, return_value=mock_session):
                result = testimport.db_insert_row(
                    1018, models.Zone, mappings, die=False
                )
                self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
