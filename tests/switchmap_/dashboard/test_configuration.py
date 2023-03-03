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
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}dashboard".format(os.sep)
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

from switchmap.dashboard import configuration as test_module


class Test_ConfigDashboard(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    _config = setup.Config(data.configtester(), randomizer=True)
    _config.save()
    config = test_module.ConfigDashboard()

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
        expected = 8034
        result = self.config.api_bind_port()
        self.assertEqual(result, expected)

    def test_server_address(self):
        """Testing function server_address."""
        # Run test
        expected = "bwSeygg8rcJAzPmA"
        result = self.config.server_address()
        self.assertEqual(result, expected)

    def test_server_bind_port(self):
        """Testing function server_bind_port."""
        # Run test
        expected = 7546
        result = self.config.server_bind_port()
        self.assertEqual(result, expected)

    def test_server_https(self):
        """Testing function server_https."""
        # Run test
        expected = True
        result = self.config.server_https()
        self.assertEqual(result, expected)

    def test_server_password(self):
        """Testing function server_password."""
        # Run test
        expected = "t7sPe2XMKh4gG2ds"
        result = self.config.server_password()
        self.assertEqual(result, expected)

    def test_server_url_root(self):
        """Testing function server_url_root."""
        # Run test
        expected = "https://bwSeygg8rcJAzPmA:7546"
        result = self.config.server_url_root()
        self.assertEqual(result, expected)

    def test_server_username(self):
        """Testing function server_username."""
        # Run test
        expected = "t7sh4gG2dsPe2XMK"
        result = self.config.server_username()
        self.assertEqual(result, expected)

    def test_username(self):
        """Testing function username."""
        # Run test
        expected = "switchmap"
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
        expected = "Drobugo8u6Lchlkiwl5o"
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
        expected = None
        result = self.config.api_password()
        self.assertEqual(result, expected)

    def test_api_url_root(self):
        """Testing function api_url_root."""
        # Run test
        expected = "http://Drobugo8u6Lchlkiwl5o:8034"
        result = self.config.api_url_root()
        self.assertEqual(result, expected)

    def test_api_username(self):
        """Testing function api_username."""
        # Run test
        expected = None
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
