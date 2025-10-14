#!/usr/bin/env python3
"""Test the poller module."""

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
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from switchmap.poller.snmp import poller as test_module
from switchmap.poller import SNMP


class TestSnmpPollerFunctions(unittest.TestCase):
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

    def test__do_poll_with_valid_snmp(self):
        """Testing function _do_poll with valid SNMP authorization."""
        # Create a mock SNMP object
        mock_auth = SNMP(
            enabled=True,
            group="test_group",
            authpassword=None,
            authprotocol=None,
            community="test_community",
            port=161,
            privpassword=None,
            privprotocol=None,
            secname="test_sec",
            version=2,
        )

        # Test with enabled authorization
        result = test_module._do_poll(mock_auth)
        self.assertTrue(result)

    def test__do_poll_with_disabled_snmp(self):
        """Testing function _do_poll with disabled SNMP authorization."""
        # Create a mock SNMP object with disabled flag
        mock_auth = SNMP(
            enabled=False,
            group="test_group",
            authpassword=None,
            authprotocol=None,
            community="test_community",
            port=161,
            privpassword=None,
            privprotocol=None,
            secname="test_sec",
            version=2,
        )

        # Test with disabled authorization
        result = test_module._do_poll(mock_auth)
        self.assertFalse(result)

    def test__do_poll_with_none(self):
        """Testing function _do_poll with None authorization."""
        result = test_module._do_poll(None)
        self.assertFalse(result)

    def test__do_poll_with_invalid_type(self):
        """Testing function _do_poll with invalid authorization type."""
        result = test_module._do_poll("invalid_type")
        self.assertFalse(result)


class TestSnmpPoller(unittest.TestCase):
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
        # Test initialization
        hostname = "test_device.example.com"
        poller = test_module.Poll(hostname)

        # Check that instance variables are set correctly
        self.assertEqual(poller._hostname, hostname)
        self.assertIsNotNone(poller._server_config)
        self.assertIsNone(poller.snmp_object)

    @patch("switchmap.poller.snmp.poller.snmp_manager.Validate")
    @patch("switchmap.poller.snmp.poller.snmp_manager.Interact")
    def test_initialize_snmp_success(self, mock_interact, mock_validate):
        """Testing function initialize_snmp with successful connection."""
        # Setup mocks
        mock_validate_instance = AsyncMock()
        mock_auth = SNMP(
            enabled=True,
            group="test_group",
            authpassword=None,
            authprotocol=None,
            community="test_community",
            port=161,
            privpassword=None,
            privprotocol=None,
            secname="test_sec",
            version=2,
        )
        mock_validate_instance.credentials.return_value = mock_auth
        mock_validate.return_value = mock_validate_instance

        mock_interact_instance = MagicMock()
        mock_interact.return_value = mock_interact_instance

        # Test successful initialization
        poller = test_module.Poll("test_host")

        async def run_test():
            result = await poller.initialize_snmp()
            self.assertTrue(result)
            self.assertIsNotNone(poller.snmp_object)
            mock_validate.assert_called_once()
            mock_interact.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.poller.snmp_manager.Validate")
    @patch("switchmap.poller.snmp.poller.log.log2info")
    def test_initialize_snmp_failure(self, mock_log, mock_validate):
        """Testing function initialize_snmp with failed connection."""
        # Setup mocks for failure case
        mock_validate_instance = AsyncMock()
        mock_auth = SNMP(
            enabled=False,
            group="test_group",
            authpassword=None,
            authprotocol=None,
            community="test_community",
            port=161,
            privpassword=None,
            privprotocol=None,
            secname="test_sec",
            version=2,
        )
        mock_validate_instance.credentials.return_value = mock_auth
        mock_validate.return_value = mock_validate_instance

        # Test failed initialization
        poller = test_module.Poll("test_host")

        async def run_test():
            result = await poller.initialize_snmp()
            self.assertFalse(result)
            self.assertIsNone(poller.snmp_object)
            mock_log.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.poller.snmp_info.Query")
    @patch("switchmap.poller.snmp.poller.log.log2info")
    def test_query_success(self, mock_log_info, mock_query):
        """Testing function query with successful data retrieval."""
        # Setup mocks
        mock_snmp_object = MagicMock()
        mock_query_instance = AsyncMock()
        expected_data = {"device": "test_data", "interfaces": []}
        mock_query_instance.everything.return_value = expected_data
        mock_query.return_value = mock_query_instance

        poller = test_module.Poll("test_host")
        poller.snmp_object = mock_snmp_object

        async def run_test():
            result = await poller.query()
            self.assertEqual(result, expected_data)
            mock_log_info.assert_called_once()
            mock_query.assert_called_once_with(snmp_object=mock_snmp_object)
            mock_query_instance.everything.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.poller.log.log2warning")
    def test_query_no_snmp_object(self, mock_log_warning):
        """Testing function query with no SNMP object."""
        # Test query without SNMP object
        poller = test_module.Poll("test_host")
        poller.snmp_object = None

        async def run_test():
            result = await poller.query()
            self.assertIsNone(result)
            mock_log_warning.assert_called_once()

        asyncio.run(run_test())

    def test_close_with_snmp_object(self):
        """Testing function close with SNMP object."""
        # Setup mock SNMP object with close method
        mock_snmp_object = MagicMock()
        mock_snmp_object.close = MagicMock()

        poller = test_module.Poll("test_host")
        poller.snmp_object = mock_snmp_object

        # Test close method
        poller.close()
        mock_snmp_object.close.assert_called_once()

    def test_close_without_snmp_object(self):
        """Testing function close without SNMP object."""
        poller = test_module.Poll("test_host")
        poller.snmp_object = None

        poller.close()

    def test_close_without_close_method(self):
        """Testing function close when SNMP object has no close method."""
        # Setup mock SNMP object without close method
        poller = test_module.Poll("test_host")
        poller.snmp_object = object()

        poller.close()


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
