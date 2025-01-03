#!/usr/bin/env python3
"""Test the log module."""

import unittest
import random
import os
import sys
import string


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


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.core import log as testimport


class TestExceptionWrapper(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(9)]
    )

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

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_re_raise(self):
        """Testing function re_raise."""
        pass


class Test_GetLog(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(9)]
    )

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

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_logfile(self):
        """Testing function logfile."""
        pass

    def test_stdout(self):
        """Testing function stdout."""
        pass


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(9)]
    )

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

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test_log2console(self):
        """Testing function log2console."""
        pass

    def test_log2die_safe(self):
        """Testing function log2die_safe."""
        pass

    def test_log2warning(self):
        """Testing function log2warning."""
        pass

    def test_log2debug(self):
        """Testing function log2debug."""
        pass

    def test_log2info(self):
        """Testing function log2info."""
        pass

    def test_log2see(self):
        """Testing function log2see."""
        pass

    def test_log2die(self):
        """Testing function log2die."""
        pass

    def test_log2exception_die(self):
        """Testing function log2exception_die."""
        pass

    def test_log2exception(self):
        """Testing function log2exception."""
        pass

    def test__logit(self):
        """Testing function _logit."""
        pass

    def test__logger_file(self):
        """Testing function _logger_file."""
        pass

    def test__logger_stdout(self):
        """Testing function _logger_stdout."""
        pass

    def test__message(self):
        """Testing function _message."""
        pass

    def test_check_environment(self):
        """Testing function check_environment."""
        pass

    def test_root_directory(self):
        """Testing function root_directory."""
        # Initialize key variables
        this_directory = os.path.dirname(os.path.realpath(__file__))
        expected = os.path.dirname(
            os.path.dirname(os.path.dirname(this_directory))
        )

        # Test
        result = testimport.root_directory()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
