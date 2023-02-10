#!/usr/bin/env python3
"""Test the snmp_manager module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp".format(
    os.sep)
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

# Import other required libraries


class TestSnmpManagerValidate(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

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

    def test_credentials(self):
        """Testing function credentials."""
        pass

    def test__credentials(self):
        """Testing function _credentials."""
        pass


class TestSnmpManagerInteract(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

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

    def test_enterprise_number(self):
        """Testing function enterprise_number."""
        pass

    def test_hostname(self):
        """Testing function hostname."""
        pass

    def test_contactable(self):
        """Testing function contactable."""
        pass

    def test_sysobjectid(self):
        """Testing function sysobjectid."""
        pass

    def test_oid_exists(self):
        """Testing function oid_exists."""
        pass

    def test__oid_exists_get(self):
        """Testing function _oid_exists_get."""
        pass

    def test__oid_exists_walk(self):
        """Testing function _oid_exists_walk."""
        pass

    def test_swalk(self):
        """Testing function swalk."""
        pass

    def test_walk(self):
        """Testing function walk."""
        pass

    def test_get(self):
        """Testing function get."""
        pass

    def test_query(self):
        """Testing function query."""
        pass


class TestSnmpManagerSession(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

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

    def test__session(self):
        """Testing function _session."""
        pass

    def test__security_level(self):
        """Testing function _security_level."""
        pass

    def test__auth_protocol(self):
        """Testing function _auth_protocol."""
        pass

    def test__priv_protocol(self):
        """Testing function _priv_protocol."""
        pass


class TestSnmpManagerFunctions(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

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

    def test__process_error(self):
        """Testing function _process_error."""
        pass

    def test__format_results(self):
        """Testing function _format_results."""
        pass

    def test__convert(self):
        """Testing function _convert."""
        pass

    def test__oid_valid_format(self):
        """Testing function _oid_valid_format."""
        pass

    def test__update_cache(self):
        """Testing function _update_cache."""
        pass


if __name__ == "__main__":

    # Do the unit test
    unittest.main()
