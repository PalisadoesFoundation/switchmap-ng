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
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}core".format(os.sep)
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

from switchmap.core import configuration as test_module


class Test_ConfigCore(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    _config = setup.Config(data.configtester(), randomizer=True)
    _config.save()
    config = test_module.ConfigCore()

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
        expected = "{0}{1}{0}log".format(
            os.sep, self._config.metadata.system_directory
        )
        result = self.config.log_directory()
        self.assertEqual(result, expected)

    def test_log_file(self):
        """Testing function log_file."""
        # Run test
        expected = "{0}{1}{0}log{0}switchmap-ng.log".format(
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
