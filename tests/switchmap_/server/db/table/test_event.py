#!/usr/bin/env python3
"""Test the event module."""

import os
import sys
import unittest
import time


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
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}table""".format(
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


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.server.db.table import event as testimport
from switchmap.server.db.table import IEvent
from switchmap.server.db.table import root
from switchmap.server.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestDbTableEvent(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

        # Create database tables
        models.create_all_tables()

        # Pollinate db with prerequisites
        db.populate()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_idx_exists(self):
        """Testing function idx_exists."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        nonexistent = testimport.exists(row.name)
        self.assertFalse(nonexistent)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        preliminary_result = testimport.exists(row.name)
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test idx_index function
        result = testimport.idx_exists(preliminary_result.idx_event)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(preliminary_result))

    def test_exists(self):
        """Testing function exists."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.name)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_insert_row(self):
        """Testing function insert_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.name)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

    def test_update_row(self):
        """Testing function update_row."""
        # Create record
        row = _row()

        # Test before insertion of an initial row
        result = testimport.exists(row.name)
        self.assertFalse(result)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        result = testimport.exists(row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(row))

        # Do an update
        idx = result.idx_event
        updated_row = IEvent(
            name=data.random_string(),
            epoch_utc=int(time.time()) * 1000,
            enabled=row.enabled,
        )
        testimport.update_row(idx, updated_row)

        # Test the update
        result = testimport.exists(updated_row.name)
        self.assertTrue(result)
        self.assertEqual(_convert(result), _convert(updated_row))

    def test_events(self):
        """Testing function events."""
        # Initialize key variables
        inserts = testimport.events()
        maximum = 10
        start = len(inserts)
        stop = start + maximum

        # Insert `maximum` values
        for _ in range(stop - start):
            # Create record
            row = _row()

            # Test before insertion of an initial row
            result = testimport.exists(row.name)
            self.assertFalse(result)

            # Test after insertion of an initial row
            testimport.insert_row(row)
            result = testimport.exists(row.name)
            self.assertTrue(result)

            # Update list of values inserted
            inserts.append(result)

        # Test
        results = testimport.events()
        results.sort(key=lambda x: (x.name))
        inserts.sort(key=lambda x: (x.name))

        # Test the length of the results
        self.assertEqual(len(results), stop)
        self.assertEqual(len(inserts), stop)

        for key, result in enumerate(results):
            self.assertEqual(_convert(result), _convert(inserts[key]))

    def test_delete(self):
        """Testing function delete."""
        # Initialize key variables
        first = 1

        ####################################################################
        # Test deletion of event on a brand new database
        ####################################################################

        # Get the database state before
        before = testimport.events()

        # Get the most recent event
        recent_idx_event = max([_.idx_event for _ in before])

        # Attempt deletion of the first event. Nothing should change
        testimport.delete(first)

        result = testimport.idx_exists(first)
        self.assertTrue(result)

        result = root.idx_exists(first)
        self.assertTrue(result)

        # Delete the most recent
        testimport.delete(recent_idx_event)

        # Test that the original is not there
        result = testimport.idx_exists(recent_idx_event)
        self.assertFalse(result)

        # Test that the most recent one is not there
        after = testimport.events()
        self.assertEqual(len(after) + 1, len(before))
        self.assertEqual(after, before[:-1])

        ####################################################################
        # Create a brand new record and test deletion
        ####################################################################

        # Create record
        row = _row()

        # Test before insertion of an initial row
        nonexistent = testimport.exists(row.name)
        self.assertFalse(nonexistent)

        # Test after insertion of an initial row
        testimport.insert_row(row)
        preliminary_result = testimport.exists(row.name)
        self.assertTrue(preliminary_result)
        self.assertEqual(_convert(preliminary_result), _convert(row))

        # Test delete function
        testimport.delete(preliminary_result.idx_event)
        result = testimport.exists(row.name)
        self.assertFalse(result)

    def test_create(self):
        """Testing function create."""
        # Get the state before
        before = testimport.events()

        # Create event
        _event = testimport.create()

        # Get the state before
        after = testimport.events()

        # Test Event entries
        expected = before
        expected.append(_event)
        expected.sort(key=lambda x: (x.idx_event))
        after.sort(key=lambda x: (x.idx_event))
        self.assertEqual(after, expected)

        # Test Root entries
        roots = root.roots()
        self.assertEqual(len(roots), len(after) + 2)

        for item in roots:
            if item.idx_root != 1:
                result = testimport.idx_exists(item.idx_event)
                self.assertTrue(result)

    def test_purge(self):
        """Testing function purge."""
        # Create additional events
        for _ in range(10):
            testimport.create()

        # Get the state before
        before = testimport.events()

        # Purge events
        testimport.purge()

        # Get the after state
        after = testimport.events()

        # Test
        self.assertTrue(len(after) == 3)
        indexes_before = [_.idx_event for _ in before]
        indexes_after = [_.idx_event for _ in before]
        for index in [0, -1, -2]:
            self.assertEqual(indexes_before[index], indexes_after[index])

    def test__row(self):
        """Testing function _row."""
        # This function is tested by all the other tests
        pass


def _convert(row):
    """Convert REvent to IEvent record.

    Args:
        row: REvent/IEvent record

    Returns:
        result: IEvent result

    """
    # Do conversion
    result = IEvent(
        name=row.name, epoch_utc=row.epoch_utc, enabled=row.enabled
    )
    return result


def _row():
    """Create an IEvent record.

    Args:
        None

    Returns:
        result: IEvent object

    """
    # Create result
    result = IEvent(
        name=data.random_string(), epoch_utc=int(time.time()) * 1000, enabled=1
    )
    return result


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
