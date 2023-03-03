#!/usr/bin/env python3
"""Test the configuration module."""

import unittest
import os
import sys

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
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}server".format(os.sep)
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

from tests.testlib_ import data, setup

setup.setenv()

from switchmap.server import configuration as test_module


class Test_ConfigServer(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    _config = setup.Config(data.configtester(), randomizer=True)
    _config.save()
    config = test_module.ConfigServer()

    # Required
    maxDiff = None

    @classmethod
    def tearDownClass(cls):
        """Remove any extraneous directories."""
        # Cleanup
        cls._config.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_api_bind_port(self):
        """Testing function api_bind_port."""
        # Run test
        expected = 7027
        result = self.config.api_bind_port()
        self.assertEqual(result, expected)

    def test_cache_directory(self):
        """Testing function cache_directory."""
        # Run test
        expected = "{}{}cache".format(self.config.system_directory(), os.sep)
        result = self.config.cache_directory()
        self.assertEqual(result, expected)

    def test_api_log_file(self):
        """Testing function api_log_file."""
        # Run test
        expected = "{1}{0}log{0}switchmap-server.log".format(
            os.sep, self._config.metadata.system_directory
        )
        result = self.config.api_log_file()
        self.assertEqual(result, expected)

    def test_db_host(self):
        """Testing function db_host."""
        # Run test
        expected = "Mwxu7gnv29AbLGyz"
        result = self.config.db_host()
        self.assertEqual(result, expected)

    def test_db_name(self):
        """Testing function db_name."""
        # Run test
        expected = "JkfSJnhZTh55wJy4"
        result = self.config.db_name()
        self.assertEqual(result, expected)

    def test_db_max_overflow(self):
        """Testing function db_max_overflow."""
        # Run test
        expected = 30
        result = self.config.db_max_overflow()
        self.assertEqual(result, expected)

    def test_db_pass(self):
        """Testing function db_pass."""
        # Run test
        expected = "nhZThsh4gPMwxu75"
        result = self.config.db_pass()
        self.assertEqual(result, expected)

    def test_db_pool_size(self):
        """Testing function db_pool_size."""
        # Run test
        expected = 30
        result = self.config.db_pool_size()
        self.assertEqual(result, expected)

    def test_db_user(self):
        """Testing function db_user."""
        # Run test
        expected = "7MKG2dstsh4gPe2X"
        result = self.config.db_user()
        self.assertEqual(result, expected)

    def test_ingest_directory(self):
        """Testing function ingest_directory."""
        # Run test
        expected = "{0}{1}cache{1}ingest".format(
            self.config.system_directory(), os.sep
        )
        result = self.config.ingest_directory()
        self.assertEqual(result, expected)

    def test_ingest_interval(self):
        """Testing function ingest_interval."""
        # Run test
        expected = 98712
        result = self.config.ingest_interval()
        self.assertEqual(result, expected)

    def test_purge_after_ingest(self):
        """Testing function purge_after_ingest."""
        # Run test
        expected = False
        result = self.config.purge_after_ingest()
        self.assertEqual(result, expected)

    def test_username(self):
        """Testing function username."""
        # Run test
        expected = "7gnv2Mwxu9AbLGyz"
        result = self.config.username()
        self.assertEqual(result, expected)

    ######################################################################
    ######################################################################
    # All ConfigAPI configuration file parameters must pass. Tests below
    ######################################################################
    ######################################################################

    def test_api_listen_address(self):
        """Testing function api_listen_address."""
        # Run test
        expected = "MKG2dst7sh4gPe2X"
        result = self.config.api_listen_address()
        self.assertEqual(result, expected)

    def test_api_https(self):
        """Testing function api_https."""
        # Run test
        expected = False
        result = self.config.api_https()
        self.assertEqual(result, expected)

    def test_api_password(self):
        """Testing function api_password."""
        # Run test
        expected = "z2vucEsOP3s1Rep6LSwe"
        result = self.config.api_password()
        self.assertEqual(result, expected)

    def test_api_url_root(self):
        """Testing function api_url_root."""
        # Run test
        expected = "http://MKG2dst7sh4gPe2X:7027"
        result = self.config.api_url_root()
        self.assertEqual(result, expected)

    def test_api_username(self):
        """Testing function api_username."""
        # Run test
        expected = "Baprat9udri2wed5LzUB"
        result = self.config.api_username()
        self.assertEqual(result, expected)

    ######################################################################
    ######################################################################
    # All 'core:' configuration file parameters must pass. Tests below
    ######################################################################
    ######################################################################

    def test_agent_subprocesses(self):
        """Testing function agent_subprocesses."""
        # Pass, this varies according to the number CPU cores on the system
        pass

    def test_system_directory(self):
        """Testing function system_directory."""
        # Run test
        expected = self._config.metadata.system_directory
        result = self.config.system_directory()
        self.assertEqual(result, expected)

    def test_log_directory(self):
        """Testing function log_directory."""
        # Run test
        expected = "{1}{0}log".format(
            os.sep, self._config.metadata.system_directory
        )
        result = self.config.log_directory()
        self.assertEqual(result, expected)

    def test_log_file(self):
        """Testing function log_file."""
        # Run test
        expected = "{1}{0}log{0}switchmap.log".format(
            os.sep, self._config.metadata.system_directory
        )
        result = self.config.log_file()
        self.assertEqual(result, expected)

    def test_log_level(self):
        """Testing function log_level."""
        # Run test
        expected = "info"
        result = self.config.log_level()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
