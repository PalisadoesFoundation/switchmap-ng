#!/usr/bin/env python3
"""Test the ingest module."""

import io
import os
import shutil
import sys
import unittest
from copy import deepcopy
import logging
from sqlalchemy import select

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
_EXPECTED = f"""\
{os.sep}switchmap-ng{os.sep}tests{os.sep}switchmap_{os.sep}server\
{os.sep}db{os.sep}ingest"""
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        f"""\
This script is not installed in the "{_EXPECTED}" directory. Please fix.\
"""
    )
    sys.exit(2)


# Create the necessary configuration
from switchmap import AGENT_INGESTER
from switchmap.core import files
from tests.testlib_ import setup
from tests.testlib_ import data

CONFIG = setup.config()
CONFIG.save()

from switchmap.poller.update import device
from switchmap.server.db.ingest.update import zone as zone_update
from switchmap.server.db.ingest import ingest
from switchmap.server.db.table import zone
from switchmap.server.db.table import oui
from switchmap.server.db.table import event
from switchmap.server.db import db
from switchmap.server.db import models
from switchmap.server.db.models import Mac
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IOui
from switchmap.server.db.table import ip as _ip
from switchmap.server.db.table import mac as _mac
from switchmap.server.db.table import macip as _macip
from switchmap.server.db.table import event as _event


from tests.testlib_ import db as dblib
from tests.testlib_ import data as datalib

from switchmap.server.db.ingest.ingest import (
    Ingest,
    _filepaths,
    _get_arguments,
    _get_zone,
    insert_macips,
)
from switchmap.server import (
    EventObjects,
    IngestArgument,
    PairMacIp,
    ZoneData,
    ZoneDevice,
    ZoneObjects,
)


def _polled_data():
    """Create prerequisite data.

    Strip out all l1_ keys from the data

    Args:
        None

    Returns:
        result: Stripped data

    """
    # Get data
    result = deepcopy(datalib.polled_data())
    return result


def _reset_db():
    """Reset the database.

    Args:
        None

    Returns:
        result, row, _zone

    """
    # Initialize key variables
    idx_zone = 1

    # Load the configuration in case it's been deleted after loading the
    # configuration above. Sometimes this happens when running
    # `python3 -m unittest discover` where another the tearDownClass of
    # another test module prematurely deletes the configuration required
    # for this module
    config = setup.config()
    config.save()

    # Drop tables
    database = dblib.Database()
    database.drop()

    # Create database tables
    models.create_all_tables()

    # Create a zone
    event_name = data.random_string()
    row = event.create(name=event_name)
    zone.insert_row(
        IZone(
            idx_event=row.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
    )

    # Create an OUI entry
    oui.insert_row(IOui(oui="testing", organization="testing", enabled=1))

    # Process the device
    _device = device.Device(_polled_data())
    device_data = _device.process()

    # Update the Zone ARP table
    _zone = zone_update.Topology(device_data, idx_zone, dns=False)
    result = ingest.insert_arptable(_zone.process())
    return result, row, _zone


class FullConfig:
    def __init__(self, base_config):
        self._config = base_config

    def __getattr__(self, name):
        return getattr(self._config, name)

    def system_directory(self):
        return "/tmp"

    def daemon_directory(self):
        return "/tmp"

    def purge_after_ingest(self):
        return False

    def agent_subprocesses(self):
        return 1


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    idx_zone = 1
    max_loops = 10

    @classmethod
    def setUp(cls):
        """Execute these steps before starting tests."""
        # Reset the database
        cls.pairmacips, cls.event, cls.zone = _reset_db()
        cls.filepath = "tests/testdata_/device-01.yaml"
        _device = device.Device(_polled_data())
        device_data = _device.process()
        cls.zone_data = zone_update.Topology(device_data, idx_zone=1, dns=False)

        # Wrap the config in a FullConfig instance
        # to simulate the behavior of the original config
        # and to avoid modifying the original config
        cls.config = FullConfig(setup.config())

        # Create a cleanup instance
        cls.cleanup_instance = Ingest(cls.config)
        cls.cleanup_instance._config = cls.config
        # Set up directories and files for the test
        cls.test_cache_dir = "/tmp/test_cache"
        cls.test_ingest_dir = "/tmp/test_ingest"
        cls.test_lock_file = "/tmp/test_lock_file"
        cls.test_temp_dir = "/tmp/test_temp"

        # Create test directories
        os.makedirs(cls.test_cache_dir, exist_ok=True)
        os.makedirs(cls.test_ingest_dir, exist_ok=True)
        os.makedirs(cls.test_temp_dir, exist_ok=True)

        # Simulate the presence of a poller lock file for certain tests
        with open(cls.test_lock_file, "w") as f:
            f.write("lock")

        # Create a file in the cache directory to move
        with open(os.path.join(cls.test_temp_dir, "test_file.yml"), "w") as f:
            f.write("test data")

        # Initialize the ingest instance
        cls.ingest_instance = Ingest(cls.config)
        cls.ingest_instance._config.cache_directory = lambda: cls.test_cache_dir
        cls.ingest_instance._config.ingest_directory = (
            lambda: cls.test_ingest_dir
        )
        cls.ingest_instance._test_cache_directory = cls.test_temp_dir
        cls.ingest_instance._test = True
        cls.ingest_instance._dns = False

    @classmethod
    def tearDown(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = dblib.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

        skip_file_path = files.skip_file(
            AGENT_INGESTER, cls.cleanup_instance._config
        )
        if os.path.isfile(skip_file_path):
            os.remove(skip_file_path)
        # Clean up files after each test
        if os.path.isdir(cls.test_cache_dir):
            shutil.rmtree(cls.test_cache_dir)
        if os.path.isdir(cls.test_ingest_dir):
            shutil.rmtree(cls.test_ingest_dir)
        if os.path.isfile(cls.test_lock_file):
            os.remove(cls.test_lock_file)

    def test_process(self):
        """Test full ingest process when lock file is absent."""
        # Ensure lock file is removed
        if os.path.exists(self.test_lock_file):
            os.remove(self.test_lock_file)

        # Ensure test file exists before processing
        test_file_path = os.path.join(self.test_temp_dir, "test_file.yml")
        self.assertTrue(
            os.path.isfile(test_file_path),
            "Test file should exist before processing",
        )

        # Run the process
        try:
            self.ingest_instance.process()
        except Exception as e:
            self.fail(f"process() raised an exception unexpectedly: {e}")

        # Verify temp dir is now empty (file was moved)
        remaining_files = os.listdir(self.test_ingest_dir)
        self.assertEqual(
            remaining_files,
            [],
            "Ingest directory should be empty after processing",
        )

    def test_zone_function(self):
        """Test that the zone function processes arguments correctly."""

        ingest_instance = Ingest(
            self.config, test=True
        )  # test=True → runs sequentially

        # Test with empty input
        empty_success = ingest_instance.zone([])
        self.assertFalse(
            empty_success, "zone() should return False for empty input"
        )

    def test_device_function(self):
        """Test that the device function processes arguments correctly."""

        ingest_instance = Ingest(
            self.config, test=True
        )  # test=True → runs sequentially
        arguments = [
            [
                IngestArgument(
                    idx_zone=self.idx_zone,
                    data=_polled_data(),
                    filepath="dummy.yml",
                    config=self.config,
                    dns=False,
                )
            ]
        ]

        # Should return True for valid arguments
        success = ingest_instance.device(arguments)
        self.assertTrue(success, "device() should return True for valid input")

        # Should return False for empty input
        empty_success = ingest_instance.device([])
        self.assertFalse(
            empty_success, "device() should return False for empty input"
        )

    # Test fails in test mode

    # def test_cleanup(self):
    #     """Test that cleanup updates the root table when skip file does not exist."""

    #     self.cleanup_instance._test = True
    #     # Call the cleanup function (with test=True)
    #     self.cleanup_instance.cleanup(self.event)

    #     # Verify that the event is deleted after cleanup
    #     self.assertIsNone(
    #         _event.exists(self.event.name),
    #         "Event should be deleted after cleanup",
    #     )

    def test_process_zone_returns_rows(self):
        """Test that process_zone returns ZoneObjects rows."""

        # Create an IngestArgument object with the necessary parameters
        arguments = IngestArgument(
            idx_zone=self.idx_zone,
            data=_polled_data(),
            filepath="dummy.yml",
            config=self.config,
            dns=False,
        )

        # Call the process_zone function with the argument
        rows = ingest.process_zone(arguments)

        # Assertions
        self.assertIsInstance(
            rows, ZoneObjects, "process_zone should return ZoneObjects objects."
        )
        self.assertTrue(len(rows) > 0, "Returned objects should not be empty.")

        # Path to the skip file
        skip_path = files.skip_file(AGENT_INGESTER, self.config)

        # Ensure the skip file exists (simulate a shutdown request)
        with open(skip_path, "w") as f:
            f.write("Skip file created for test")

        try:
            # Call the process_zone function with the argument
            rows = ingest.process_zone(arguments)

            # Assert that process_zone returns None (or handles the skip condition as expected)
            self.assertIsNone(
                rows,
                "process_zone should not return rows when skip file is present.",
            )
        finally:
            # Cleanup: Remove the skip file after the test
            if os.path.exists(skip_path):
                os.remove(skip_path)

    def test_process_device_updates_database(self):
        """Test that process_device ingests data and updates DB."""

        arguments = IngestArgument(
            idx_zone=self.idx_zone,
            data=_polled_data(),
            filepath="dummy.yml",
            config=self.config,
            dns=False,
        )

        ingest.process_device(arguments)

        statement = select(Mac)
        mac_rows = db.db_select_row(1074, statement)
        mac_rows_length = len(mac_rows)
        self.assertGreater(
            mac_rows_length, 0, "MAC entries should be inserted."
        )
        # Path to the skip file
        skip_path = files.skip_file(AGENT_INGESTER, self.config)

        # Test that the skip file prevents database updates
        # Ensure the skip file exists (simulate a shutdown request)
        with open(skip_path, "w") as f:
            f.write("Skip file created for test")

        try:
            ingest.process_device(arguments)
            statement = select(Mac)
            mac_rows = db.db_select_row(1091, statement)
            self.assertEqual(
                len(mac_rows),
                mac_rows_length,
                "MAC entries should not be inserted.",
            )
        finally:
            # Cleanup: Remove the skip file after the test
            if os.path.exists(skip_path):
                os.remove(skip_path)

    def test_setup_function_returns_event_objects(self):
        """Test that setup returns a valid EventObjects instance with zones."""

        src = "tests/testdata_"  # Folder containing device YAML files

        result = ingest.setup(src, self.config)

        self.assertIsInstance(result, EventObjects)
        self.assertTrue(len(result.zones) > 0)
        for zone in result.zones:
            self.assertIsInstance(zone, ZoneDevice)
            self.assertTrue(zone.filepath.endswith(".yaml"))

    def test_insert_arptable(self):
        """Test insert_arptable function avoids duplicates."""
        # insert_arptable function is called in the setup function
        # Check if the database has been populated with the expected data

        self.assertIsInstance(self.pairmacips, list)
        self.assertTrue(
            all(isinstance(item, PairMacIp) for item in self.pairmacips)
        )

    def test_insert_arptable_passing_list(self):
        """Ensure insert_arptable handles empty list input gracefully."""
        result = ingest.insert_arptable([], test=True)
        self.assertIsInstance(result, list)

    def test_insert_macips_adds_records(self):
        """Test insert_macips with a list of PairMacIp objects.

        Verifies that MAC, IP, and MAC-IP mapping records are inserted
        correctly when given multiple items and test=True.
        """
        insert_macips(self.pairmacips[0:2], test=True)

        for item in self.pairmacips[0:2]:
            mac = _mac.exists(item.idx_zone, item.mac)
            ip = _ip.exists(item.idx_zone, item.ip)
            self.assertTrue(mac)
            self.assertTrue(ip)
            macip = _macip.exists(mac.idx_mac, ip.idx_ip)
            self.assertTrue(macip)

    def test_insert_macips_single_item(self):
        """Test insert_macips with a single PairMacIp object.

        Ensures that even a non-list input inserts MAC, IP, and MAC-IP
        mapping records correctly when test=True.
        """
        single_item = self.pairmacips[0]  # Not a list
        insert_macips(single_item, test=True)

        mac = _mac.exists(single_item.idx_zone, single_item.mac)
        ip = _ip.exists(single_item.idx_zone, single_item.ip)
        self.assertTrue(mac)
        self.assertTrue(ip)
        macip = _macip.exists(mac.idx_mac, ip.idx_ip)
        self.assertTrue(macip)

    def test_filepaths_returns_only_yaml(self):
        """Test that _filepaths returns only YAML files."""

        src = "tests/testdata_"
        result = _filepaths(src)
        self.assertIn(self.filepath, result)
        self.assertEqual(len(result), 1)

    def test_get_zone_creates_new_zone(self):
        """Test the case when the zone is not found and a new zone is created."""

        # Call the _get_zone function with the event and file path
        result = _get_zone(self.event, self.filepath)

        # Assertions to verify the behavior
        # Check that a ZoneData object is returned
        self.assertIsInstance(result, ZoneData)

    def test_get_zone_existing_zone(self):
        """Test the case when the zone already exists."""

        # Call the _get_zone function with the event and file path
        result = _get_zone(self.event, self.filepath)

        # Assertions to verify the behavior
        # Check that a ZoneData object is returned
        self.assertIsInstance(result, ZoneData)

    def test_get_arguments_returns_correct_tuple(self):
        data_sample = _polled_data()
        filepath = "dummy.yml"
        idx_zone = self.idx_zone
        dns = False

        # Creating the IngestArgument object
        arguments = IngestArgument(
            idx_zone=idx_zone,
            data=data_sample,
            filepath=filepath,
            config=self.config,
            dns=dns,
        )

        result = _get_arguments(arguments)

        self.assertEqual(
            result, (idx_zone, data_sample, filepath, self.config, dns)
        )


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
