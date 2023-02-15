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
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}poller".format(os.sep)
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

from switchmap.poller import configuration as test_module


class Test_ConfigPoller(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    _config = setup.Config(data.configtester(), randomizer=True)
    _config.save()
    config = test_module.ConfigPoller()

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

    def test_hostnames(self):
        """Testing function hostnames."""
        # Run test
        expected = ["unittest.example.org"]
        result = self.config.hostnames()
        self.assertEqual(result, expected)

    def test_polling_interval(self):
        """Testing function polling_interval."""
        # Run test
        expected = 21600
        result = self.config.polling_interval()
        self.assertEqual(result, expected)

    def test_daemon_log_file(self):
        """Testing function daemon_log_file."""
        # Run test
        expected = "{1}{0}log{0}switchmap-poller.log".format(
            os.sep, self._config.metadata.system_directory
        )
        result = self.config.daemon_log_file()
        self.assertEqual(result, expected)

    def test_snmp_auth(self):
        """Testing function snmp_auth."""
        # Run test
        expected = [
            {
                "enabled": True,
                "group_name": "zg8rcJPmAygbwSeA",
                "snmp_authpassword": "Gnn5999YqCMbre9W",
                "snmp_authprotocol": "sha",
                "snmp_community": None,
                "snmp_port": 161,
                "snmp_privpassword": "Jgt8MFTEhyh9s2ju",
                "snmp_privprotocol": "aes",
                "snmp_secname": "NT9degJu9NBWbxRK",
                "snmp_version": 3,
            }
        ]
        result = self.config.snmp_auth()
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

    def test_username(self):
        """Testing function username."""
        # Run test
        expected = "7gnv2Mwxu9AbLGyz"
        result = self.config.username()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
