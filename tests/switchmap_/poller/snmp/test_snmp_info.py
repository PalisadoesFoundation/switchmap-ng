#!/usr/bin/env python3
"""Test the snmp_info module."""

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
from collections import defaultdict
import time

from switchmap.poller.snmp import snmp_info as test_module


class TestSnmpInfo(unittest.TestCase):
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
        mock_snmp_object = MagicMock()
        query = test_module.Query(mock_snmp_object)

        # Check that instance variable is set correctly
        self.assertEqual(query.snmp_object, mock_snmp_object)

    def test_everything_success(self):
        """Testing function everything with successful results."""
        # Setup mock SNMP object
        mock_snmp_object = MagicMock()
        query = test_module.Query(mock_snmp_object)

        # Mock the individual methods instead of asyncio.gather
        query.misc = AsyncMock(
            return_value={"timestamp": 12345, "host": "test_host"}
        )
        query.system = AsyncMock(return_value={"sysName": "test_system"})
        query.layer1 = AsyncMock(
            return_value={"interface": {"1": {"ifIndex": 1}}}
        )
        query.layer2 = AsyncMock(
            return_value={"vlan": {"1": {"name": "default"}}}
        )
        query.layer3 = AsyncMock(
            return_value={"arp": {"192.168.1.1": {"mac": "aa:bb:cc"}}}
        )

        async def run_test():
            result = await query.everything()

            # Should have all sections
            self.assertIn("misc", result)
            self.assertIn("system", result)
            self.assertIn("layer1", result)
            self.assertIn("layer2", result)
            self.assertIn("layer3", result)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test_everything_with_exceptions(self, mock_log):
        """Testing function everything with some exceptions."""
        mock_snmp_object = MagicMock()
        query = test_module.Query(mock_snmp_object)

        # Mock methods with exceptions and empty results
        query.misc = AsyncMock(return_value={"timestamp": 12345})
        query.system = AsyncMock(side_effect=Exception("System failed"))
        query.layer1 = AsyncMock(return_value={"interface": {}})
        query.layer2 = AsyncMock(return_value=None)
        query.layer3 = AsyncMock(return_value={"arp": {}})

        async def run_test():
            result = await query.everything()

            # Should have successful sections only
            self.assertIn("misc", result)
            self.assertNotIn("system", result)
            self.assertIn("layer1", result)
            self.assertNotIn("layer2", result)
            self.assertIn("layer3", result)

            # Should log the exception
            mock_log.assert_called()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.iana_enterprise.Query")
    @patch("switchmap.poller.snmp.snmp_info.time.time")
    def test_misc_success(self, mock_time, mock_iana):
        """Testing function misc with successful data."""
        # Setup mocks
        mock_time.return_value = 1234567890
        mock_snmp_object = MagicMock()
        mock_snmp_object.hostname.return_value = "test_device"
        mock_snmp_object.sysobjectid = AsyncMock(
            return_value="1.3.6.1.4.1.9.1.1"
        )

        mock_vendor = MagicMock()
        mock_vendor.enterprise.return_value = 9
        mock_iana.return_value = mock_vendor

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.misc()

            # Check expected data
            self.assertEqual(result["timestamp"], 1234567890)
            self.assertEqual(result["host"], "test_device")
            self.assertEqual(result["IANAEnterpriseNumber"], 9)

            # Verify method calls
            mock_snmp_object.hostname.assert_called_once()
            mock_snmp_object.sysobjectid.assert_called_once()
            mock_iana.assert_called_once_with(sysobjectid="1.3.6.1.4.1.9.1.1")

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.time.time")
    def test_misc_no_sysobjectid(self, mock_time):
        """Testing function misc when sysobjectid is None."""
        mock_time.return_value = 1234567890
        mock_snmp_object = MagicMock()
        mock_snmp_object.hostname.return_value = "test_device"
        mock_snmp_object.sysobjectid = AsyncMock(return_value=None)

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.misc()

            # Check expected data
            self.assertEqual(result["timestamp"], 1234567890)
            self.assertEqual(result["host"], "test_device")
            self.assertIsNone(result["IANAEnterpriseNumber"])

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    @patch("switchmap.poller.snmp.snmp_info.asyncio.gather")
    def test_system_success(self, mock_gather, mock_get_queries):
        """Testing function system with successful results."""
        # Setup mocks
        mock_snmp_object = MagicMock()

        # Mock query classes
        mock_query_class = MagicMock()
        mock_query_instance = MagicMock()
        mock_query_instance.supported = AsyncMock(return_value=True)
        mock_query_class.return_value = mock_query_instance
        mock_query_class.__name__ = "TestSystemQuery"
        mock_get_queries.return_value = [mock_query_class]

        # Mock support check and results
        async def async_gather_side_effect(*args, **kwargs):
            if mock_gather.call_count == 1:
                return [True]
            else:
                return [{"device": {"info": {"sysName": "test"}}}]

        mock_gather.side_effect = async_gather_side_effect

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.system()

            # Check that we got data back
            self.assertIsNotNone(result)
            self.assertIn("device", result)

            # Verify method calls
            mock_get_queries.assert_called_once_with("system")
            self.assertEqual(mock_gather.call_count, 2)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    def test_system_no_supported_queries(self, mock_get_queries):
        """Testing function system with no supported queries."""
        mock_snmp_object = MagicMock()
        mock_get_queries.return_value = []

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.system()
            self.assertIsNone(result)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    @patch("switchmap.poller.snmp.snmp_info.asyncio.gather")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test_layer1_with_exceptions(
        self, mock_log, mock_gather, mock_get_queries
    ):
        """Testing function layer1 with exceptions in processing."""
        mock_snmp_object = MagicMock()

        # Mock query classes
        mock_query_class1 = MagicMock()
        mock_query_class1.__name__ = "TestLayer1Query1"
        mock_query_instance1 = MagicMock()
        mock_query_instance1.supported = AsyncMock(return_value=True)
        mock_query_class1.return_value = mock_query_instance1

        mock_query_class2 = MagicMock()
        mock_query_class2.__name__ = "TestLayer1Query2"
        mock_query_instance2 = MagicMock()
        mock_query_instance2.supported = AsyncMock(return_value=True)
        mock_query_class2.return_value = mock_query_instance2

        mock_get_queries.return_value = [mock_query_class1, mock_query_class2]

        # Mock support check and results
        async def async_gather_side_effect(*args, **kwargs):
            if mock_gather.call_count == 1:
                return [True, True]
            else:
                return [
                    {"interface": {"1": {"data": "test"}}},
                    Exception("Layer1 failed"),
                ]

        mock_gather.side_effect = async_gather_side_effect

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.layer1()

            # Should return data with successful results, not None
            self.assertIsNotNone(result)
            self.assertIn("interface", result)
            self.assertEqual(result["interface"]["1"]["data"], "test")
            mock_log.assert_called()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    @patch("switchmap.poller.snmp.snmp_info.asyncio.gather")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test_layer2_with_exceptions(
        self, mock_log, mock_gather, mock_get_queries
    ):
        """Testing function layer2 with exceptions in processing."""
        mock_snmp_object = MagicMock()
        mock_query_class = MagicMock()
        mock_query_class.__name__ = "TestLayer2Query"
        mock_query_instance = MagicMock()
        mock_query_instance.supported = AsyncMock(return_value=True)
        mock_query_class.return_value = mock_query_instance
        mock_get_queries.return_value = [mock_query_class]

        # Mock support and exception in processing
        async def async_gather_side_effect(*args, **kwargs):
            if mock_gather.call_count == 1:
                return [True]
            else:
                return [Exception("Layer2 processing failed")]

        mock_gather.side_effect = async_gather_side_effect

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.layer2()

            # Should return empty defaultdict, not None (when all queries fail)
            self.assertIsNotNone(result)
            # Result should be empty defaultdict since no successful data
            self.assertEqual(len(result), 0)
            mock_log.assert_called()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    @patch("switchmap.poller.snmp.snmp_info.asyncio.gather")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test_layer3_with_exceptions(
        self, mock_log, mock_gather, mock_get_queries
    ):
        """Testing function layer3 with exceptions in processing."""
        mock_snmp_object = MagicMock()
        mock_query_class = MagicMock()
        mock_query_class.__name__ = "TestLayer3Query"
        mock_query_instance = MagicMock()
        mock_query_instance.supported = AsyncMock(return_value=True)
        mock_query_class.return_value = mock_query_instance
        mock_get_queries.return_value = [mock_query_class]

        # Mock support and exception in processing
        async def async_gather_side_effect(*args, **kwargs):
            if mock_gather.call_count == 1:
                return [True]
            else:
                return [Exception("Layer3 processing failed")]

        mock_gather.side_effect = async_gather_side_effect

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.layer3()

            # Should return empty defaultdict, not None (when all queries fail)
            self.assertIsNotNone(result)
            # Result should be empty defaultdict since no successful data
            self.assertEqual(len(result), 0)
            mock_log.assert_called()

        asyncio.run(run_test())

    def test__add_data_simple(self):
        """Testing function _add_data with simple data structures."""
        source = {
            "primary1": {"secondary1": "value1", "secondary2": "value2"},
            "primary2": {"secondary3": "value3"},
        }
        target = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_data(source, target)

            # Check data was copied correctly
            self.assertEqual(result["primary1"]["secondary1"], "value1")
            self.assertEqual(result["primary1"]["secondary2"], "value2")
            self.assertEqual(result["primary2"]["secondary3"], "value3")

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test__add_system_async_success(self, mock_log, mock_iscoroutine):
        """Testing function _add_system with async query method."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.system = AsyncMock(
            return_value={"device": {"info": {"sysName": "test_device"}}}
        )

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_system(mock_query, data)

            # Check data was added correctly
            self.assertEqual(result["device"]["info"]["sysName"], "test_device")
            mock_query.system.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.asyncio.get_event_loop")
    def test__add_system_sync_success(self, mock_get_loop, mock_iscoroutine):
        """Testing function _add_system with sync query method."""
        mock_iscoroutine.return_value = False

        mock_loop = AsyncMock()
        mock_get_loop.return_value = mock_loop
        mock_loop.run_in_executor = AsyncMock(
            return_value={"device": {"info": {"sysName": "test_device"}}}
        )

        mock_query = MagicMock()
        mock_query.system = MagicMock()

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_system(mock_query, data)

            # Check data was added correctly
            self.assertEqual(result["device"]["info"]["sysName"], "test_device")
            mock_loop.run_in_executor.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test__add_system_exception(self, mock_log, mock_iscoroutine):
        """Testing function _add_system with exception."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.system = AsyncMock(
            side_effect=Exception("System query failed")
        )

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_system(mock_query, data)

            # Should return original data and log warning
            self.assertEqual(result, data)
            mock_log.assert_called()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info._add_data")
    @patch("switchmap.poller.snmp.snmp_info.log.log2debug")
    def test__add_layer1_success(
        self, mock_log_debug, mock_add_data, mock_iscoroutine
    ):
        """Testing function _add_layer1 with successful result."""
        mock_iscoroutine.return_value = True
        mock_add_data.return_value = AsyncMock(
            return_value={"interface": {"1": {"data": "test"}}}
        )

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer1Query"
        mock_query.layer1 = AsyncMock(
            return_value={"interface": {"1": {"data": "test"}}}
        )

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            await test_module._add_layer1(mock_query, data)

            # Should call _add_data
            mock_add_data.assert_called_once()
            mock_query.layer1.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2debug")
    def test__add_layer1_no_result(self, mock_log_debug, mock_iscoroutine):
        """Testing function _add_layer1 with no result."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer1Query"
        mock_query.layer1 = AsyncMock(return_value=None)

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_layer1(mock_query, data)

            # Should log debug message for no data
            mock_log_debug.assert_called()
            self.assertEqual(result, data)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test__add_layer2_exception(self, mock_log_warning, mock_iscoroutine):
        """Testing function _add_layer2 with exception."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer2Query"
        mock_query.layer2 = AsyncMock(side_effect=Exception("Layer2 failed"))

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_layer2(mock_query, data)

            # Should log warning and return original data
            mock_log_warning.assert_called()
            self.assertEqual(result, data)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2warning")
    def test__add_layer3_exception(self, mock_log_warning, mock_iscoroutine):
        """Testing function _add_layer3 with exception."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer3Query"
        mock_query.layer3 = AsyncMock(side_effect=Exception("Layer3 failed"))

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_layer3(mock_query, data)

            # Should log warning and return original data
            mock_log_warning.assert_called()
            self.assertEqual(result, data)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.asyncio.get_event_loop")
    @patch("switchmap.poller.snmp.snmp_info._add_data")
    def test__add_layer2_sync_success(
        self, mock_add_data, mock_get_loop, mock_iscoroutine
    ):
        """Testing function _add_layer2 with sync query method."""
        mock_iscoroutine.return_value = False
        mock_add_data.return_value = AsyncMock(
            return_value={"vlan": {"1": {"name": "default"}}}
        )

        mock_loop = AsyncMock()
        mock_get_loop.return_value = mock_loop
        mock_loop.run_in_executor = AsyncMock(
            return_value={"vlan": {"1": {"name": "default"}}}
        )

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer2Query"
        mock_query.layer2 = MagicMock()

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            await test_module._add_layer2(mock_query, data)

            # Should call _add_data
            mock_add_data.assert_called_once()
            mock_loop.run_in_executor.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2debug")
    def test__add_layer2_no_result(self, mock_log_debug, mock_iscoroutine):
        """Testing function _add_layer2 with no result."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer2Query"
        mock_query.layer2 = AsyncMock(return_value=None)

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_layer2(mock_query, data)

            # Should log debug message and return original data
            mock_log_debug.assert_called()
            self.assertEqual(result, data)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info._add_data")
    def test__add_layer3_success(self, mock_add_data, mock_iscoroutine):
        """Testing function _add_layer3 with successful result."""
        mock_iscoroutine.return_value = True
        mock_add_data.return_value = AsyncMock(
            return_value={"arp": {"192.168.1.1": {"mac": "aa:bb:cc"}}}
        )

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer3Query"
        mock_query.layer3 = AsyncMock(
            return_value={"arp": {"192.168.1.1": {"mac": "aa:bb:cc"}}}
        )

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            await test_module._add_layer3(mock_query, data)

            # Should call _add_data
            mock_add_data.assert_called_once()
            mock_query.layer3.assert_called_once()

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    @patch("switchmap.poller.snmp.snmp_info.log.log2debug")
    def test__add_layer3_no_result(self, mock_log_debug, mock_iscoroutine):
        """Testing function _add_layer3 with no result."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.__class__.__name__ = "TestLayer3Query"
        mock_query.layer3 = AsyncMock(return_value=None)

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_layer3(mock_query, data)

            # Should log debug message and return original data
            mock_log_debug.assert_called()
            self.assertEqual(result, data)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    def test__add_system_no_result(self, mock_iscoroutine):
        """Testing function _add_system with no result."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.system = AsyncMock(return_value=None)

        data = defaultdict(lambda: defaultdict(dict))
        original_data = dict(data)

        async def run_test():
            result = await test_module._add_system(mock_query, data)

            # Should return original data when no result
            self.assertEqual(result, original_data)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.asyncio.iscoroutinefunction")
    def test__add_system_complex_nested_data(self, mock_iscoroutine):
        """Testing function _add_system with complex nested data structure."""
        mock_iscoroutine.return_value = True

        mock_query = MagicMock()
        mock_query.system = AsyncMock(
            return_value={
                "device": {
                    "info": {
                        "sysName": "test_device",
                        "sysDescr": "test description",
                    },
                    "simple": "value",
                },
                "simple_primary": "direct_value",
            }
        )

        data = defaultdict(lambda: defaultdict(dict))

        async def run_test():
            result = await test_module._add_system(mock_query, data)

            # Check complex nested structure is handled
            self.assertEqual(result["device"]["info"]["sysName"], "test_device")
            self.assertEqual(
                result["device"]["info"]["sysDescr"], "test description"
            )
            self.assertEqual(result["device"]["simple"], "value")
            self.assertEqual(result["simple_primary"], "direct_value")

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    def test_system_no_supported_items_after_check(self, mock_get_queries):
        """Test system() method when queries don't pass support check.

        This test verifies that when queries exist but fail the
        supported() check,
        the system() method returns None instead of attempting to execute them.

        Args:
            mock_get_queries: Mock for get_queries function that returns
                query classes that will fail the support check.
        """
        mock_snmp_object = MagicMock()

        # Mock query class
        mock_query_class = MagicMock()
        mock_query_instance = MagicMock()
        mock_query_instance.supported = AsyncMock(return_value=False)
        mock_query_class.return_value = mock_query_instance
        mock_query_class.__name__ = "TestSystemQuery"
        mock_get_queries.return_value = [mock_query_class]

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.system()

            # Should return None when no queries are supported
            self.assertIsNone(result)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    def test_layer1_no_supported_queries(self, mock_get_queries):
        """Testing function layer1 with no queries available."""
        mock_snmp_object = MagicMock()
        mock_get_queries.return_value = []

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.layer1()
            self.assertIsNone(result)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    def test_layer2_no_supported_queries(self, mock_get_queries):
        """Testing function layer2 with no queries available."""
        mock_snmp_object = MagicMock()
        mock_get_queries.return_value = []

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.layer2()
            self.assertIsNone(result)

        asyncio.run(run_test())

    @patch("switchmap.poller.snmp.snmp_info.get_queries")
    def test_layer3_no_supported_queries(self, mock_get_queries):
        """Testing function layer3 with no queries available."""
        mock_snmp_object = MagicMock()
        mock_get_queries.return_value = []

        query = test_module.Query(mock_snmp_object)

        async def run_test():
            result = await query.layer3()
            self.assertIsNone(result)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
