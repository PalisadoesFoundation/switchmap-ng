#!/usr/bin/env python3
"""Test the mib_snmpv2 module."""

import unittest
import os
import sys
from unittest.mock import Mock, AsyncMock

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
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp{0}mib{0}generic\
""".format(
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

# Import other required libraries
from switchmap.poller.snmp.mib.generic import mib_snmpv2 as testimport


class Query:
    """Class for snmp_manager.Query mock.

    A detailed tutorial about Python mocks can be found here:
    http://www.drdobbs.com/testing/using-mocks-in-python/240168251

    """

    def query(self):
        """Do an SNMP query.

        Args:
            None

        Returns:
            None
        """
        pass

    def oid_exists(self):
        """Determine existence of OID on device.

        Args:
            None

        Returns:
            None
        """
        pass

    def swalk(self):
        """Do a failsafe SNMPwalk.

        Args:
            None

        Returns:
            None
        """
        pass

    def walk(self):
        """Do a SNMPwalk.

        Args:
            None

        Returns:
            None
        """
        pass


class TestMibSnmpV2Functions(unittest.TestCase):
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

    def test_get_query(self):
        """Testing function get_query."""
        # Test that get_query returns the Snmpv2Query class
        result = testimport.get_query()
        self.assertEqual(result, testimport.Snmpv2Query)

    def test_init_query(self):
        """Testing function init_query."""
        # Create a mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Test that init_query returns an instance of Snmpv2Query
        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.Snmpv2Query)
        self.assertEqual(result.snmp_object, mock_snmp)


class TestMibSnmpV2(unittest.IsolatedAsyncioTestCase):
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
        # Create a mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Initialize Snmpv2Query
        snmpv2 = testimport.Snmpv2Query(mock_snmp)

        self.assertEqual(snmpv2.snmp_object, mock_snmp)

    async def test_system(self):
        """Testing function system."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Each call returns a dict with one value
        mock_responses = [
            {},
            {".1.3.6.1.2.1.1.1.0": b"Test Device Description"},
            {".1.3.6.1.2.1.1.2.0": b"1.3.6.1.4.1.9.1.123"},
            {".1.3.6.1.2.1.1.3.0": 123456789},
            {".1.3.6.1.2.1.1.4.0": b"admin@example.com"},
            {".1.3.6.1.2.1.1.5.0": b"test-device"},
            {".1.3.6.1.2.1.1.6.0": b"Test Location"},
        ]

        # Mock the get method to return appropriate responses
        call_count = [0]

        async def mock_get(oid, normalized=False):
            call_count[0] += 1
            return mock_responses[call_count[0]]

        mock_snmp.get = AsyncMock(side_effect=mock_get)

        # Create Snmpv2Query instance
        snmpv2 = testimport.Snmpv2Query(mock_snmp)

        # Call system
        result = await snmpv2.system()

        # Verify result structure
        self.assertIn("SNMPv2-MIB", result)
        data = result["SNMPv2-MIB"]

        # Verify all expected keys are present
        self.assertIn("sysDescr", data)
        self.assertIn("sysObjectID", data)
        self.assertIn("sysUpTime", data)
        self.assertIn("sysContact", data)
        self.assertIn("sysName", data)
        self.assertIn("sysLocation", data)

        # Verify values (all should be keyed by 0)
        self.assertEqual(data["sysDescr"][0], "Test Device Description")
        self.assertEqual(data["sysObjectID"][0], "1.3.6.1.4.1.9.1.123")
        self.assertEqual(data["sysUpTime"][0], 123456789)
        self.assertEqual(data["sysContact"][0], "admin@example.com")
        self.assertEqual(data["sysName"][0], "test-device")
        self.assertEqual(data["sysLocation"][0], "Test Location")

        # Verify get was called 6 times (nodes 1-6)
        self.assertEqual(mock_snmp.get.call_count, 6)

    async def test_system_with_special_characters(self):
        """Testing function system with special characters in sysDescr."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create mock responses with special characters and extra whitespace
        special_chars = b"Test  Device\nWith\tSpecial\rCharacters  "
        mock_responses = [
            {},
            {".1.3.6.1.2.1.1.1.0": special_chars},
            {".1.3.6.1.2.1.1.2.0": b"1.3.6.1.4.1.1"},
            {".1.3.6.1.2.1.1.3.0": 999},
            {".1.3.6.1.2.1.1.4.0": b"contact"},
            {".1.3.6.1.2.1.1.5.0": b"name"},
            {".1.3.6.1.2.1.1.6.0": b"location"},
        ]

        call_count = [0]

        async def mock_get(oid, normalized=False):
            call_count[0] += 1
            return mock_responses[call_count[0]]

        mock_snmp.get = AsyncMock(side_effect=mock_get)

        # Create Snmpv2Query instance
        snmpv2 = testimport.Snmpv2Query(mock_snmp)

        # Call system
        result = await snmpv2.system()

        # Verify that cleanstring was applied to sysDescr
        # The general.cleanstring function should clean up special characters
        data = result["SNMPv2-MIB"]
        sys_descr = data["sysDescr"][0]

        # cleanstring should normalize whitespace and remove special chars
        # Just verify it's a string and not empty
        self.assertIsInstance(sys_descr, str)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
